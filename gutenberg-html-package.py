#!/usr/bin/env python3
"""
Gutenberg HTML to Markdown Chapters Converter
Downloads HTML from Project Gutenberg and splits it into markdown files per chapter.
"""

import re
import os
import sys
import argparse
from pathlib import Path
from urllib.request import urlopen
from urllib.error import URLError
from html.parser import HTMLParser
import html


class GutenbergHTMLParser(HTMLParser):
    """Parse Project Gutenberg HTML to extract chapters and front matter."""

    # Known front matter section IDs (case-insensitive)
    FRONT_MATTER_IDS = {'dedication', 'preface', 'introduction', 'prologue',
                        'foreword', 'contents', 'acknowledgments', 'acknowledgements'}
    # Known back matter section IDs
    BACK_MATTER_IDS = {'epilogue', 'afterword', 'appendix', 'notes', 'index', 'glossary',
                       'footnotes', 'bibliography', 'endnotes'}

    def __init__(self):
        super().__init__()
        self.chapters = []
        self.front_matter = []
        self.current_section = None
        self.current_content = []
        self.in_body = False
        self.in_boilerplate = False
        self.boilerplate_depth = 0  # Track nested depth in boilerplate
        self.chapter_id = None
        self.skip_content = False
        self.in_chapter_div = False
        self.in_toc = False  # Track if we're inside TOC
        self.in_pagenum = False  # Track if we're inside a pageNum span
        self.pending_section_id = None
        self.pending_chapter_id = None  # For div-based chapter detection

    def _is_chapter_start(self, tag, attrs_dict):
        """Check if this tag marks the start of a chapter/section."""
        # Strategy 1: div with id="chapter-X"
        if tag == 'div' and 'id' in attrs_dict:
            div_id = attrs_dict['id'].lower()
            if div_id.startswith('chapter-'):
                return True, attrs_dict['id'], 'chapter'
            if div_id in self.FRONT_MATTER_IDS:
                return True, attrs_dict['id'], 'front_matter'
            if div_id in self.BACK_MATTER_IDS:
                return True, attrs_dict['id'], 'back_matter'

        # Strategy 2: div with class="chapter" (common in newer Gutenberg HTML)
        if tag == 'div' and 'class' in attrs_dict:
            classes = attrs_dict['class'].lower().split()
            if 'chapter' in classes:
                self.in_chapter_div = True
                return False, None, None  # Wait for h2/h3 to get the ID

        # Strategy 3: h2/h3 with id inside a chapter div (or standalone)
        if tag in ('h2', 'h3') and 'id' in attrs_dict:
            heading_id = attrs_dict['id']
            heading_id_lower = heading_id.lower()

            # Skip Gutenberg boilerplate sections
            if 'gutenberg' in heading_id_lower or 'license' in heading_id_lower:
                return False, None, None

            # Skip TOC and pure content markers
            if heading_id_lower in ('contents', 'toc', 'table-of-contents'):
                return True, heading_id, 'toc'  # Special type for TOC

            # Check for front/back matter
            if heading_id_lower in self.FRONT_MATTER_IDS:
                return True, heading_id, 'front_matter'
            if heading_id_lower in self.BACK_MATTER_IDS:
                return True, heading_id, 'back_matter'

            # Check for part headers (PART_I, PART_II, etc.)
            if heading_id_lower.startswith('part_') or heading_id_lower.startswith('part-'):
                return True, heading_id, 'part'

            # Check for roman numerals or numbers (I, II, III, 1, 2, 3)
            if re.match(r'^[IVXLC]+$', heading_id) or re.match(r'^\d+$', heading_id):
                return True, heading_id, 'chapter'

            # Check for chapter-like patterns (chapter-1, chap_2, ch3, etc.)
            if re.match(r'^(chapter|chap|ch)[_-]?\d+', heading_id_lower):
                return True, heading_id, 'chapter'

        # Strategy 4: div with id like "ch1", "ch2", etc.
        if tag == 'div' and 'id' in attrs_dict:
            div_id = attrs_dict['id'].lower()
            if re.match(r'^ch\d+$', div_id):
                self.in_chapter_div = True
                self.pending_chapter_id = attrs_dict['id']
                return False, None, None  # Wait for h2 to get the title

        # Strategy 5: h2/h3 inside a chapter div (may not have an id)
        if tag in ('h2', 'h3') and self.in_chapter_div and self.pending_chapter_id:
            # Use the pending chapter ID
            chapter_id = self.pending_chapter_id
            self.pending_chapter_id = None  # Clear it
            return True, chapter_id, 'chapter'

        return False, None, None

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)

        # Skip boilerplate sections (can be div or section)
        if 'class' in attrs_dict and 'pg-boilerplate' in attrs_dict['class']:
            self.in_boilerplate = True
            self.boilerplate_depth = 1
            self.skip_content = True
            return

        # Track depth inside boilerplate
        if self.in_boilerplate and tag in ('div', 'section'):
            self.boilerplate_depth += 1
            return

        # Skip pageNum spans (navigation links like [Contents], [13], etc.)
        if tag == 'span' and 'class' in attrs_dict:
            if 'pagenum' in attrs_dict['class'].lower():
                self.in_pagenum = True
                return

        if self.skip_content or self.in_boilerplate:
            return

        # Check for chapter/section start
        is_chapter, section_id, section_type = self._is_chapter_start(tag, attrs_dict)

        if is_chapter and section_id:
            # Save previous section if exists
            if self.current_section:
                self._save_section()

            # If this is TOC, mark it and skip content collection
            if section_type == 'toc':
                self.in_toc = True
                self.current_section = None
                return

            # Reset TOC flag when we hit a new real section
            self.in_toc = False

            self.chapter_id = section_id
            self.current_section = {
                'id': section_id,
                'type': section_type,
                'content': []
            }
            return

        # Skip content inside TOC
        if self.in_toc:
            return

        # Track content tags
        if self.current_section and not self.in_boilerplate:
            if tag == 'p':
                self.current_content = []
            elif tag == 'h1' or tag == 'h2' or tag == 'h3':
                self.current_content = []
            elif tag == 'hr':
                self.current_section['content'].append('\n---\n')
            elif tag == 'blockquote':
                self.current_content = ['> ']
            elif tag == 'em' or tag == 'i':
                self.current_content.append('*')
            elif tag == 'strong' or tag == 'b':
                self.current_content.append('**')
            elif tag == 'br':
                self.current_content.append('  \n')
    
    def handle_endtag(self, tag):
        # Track depth inside boilerplate
        if self.in_boilerplate and tag in ('div', 'section'):
            self.boilerplate_depth -= 1
            if self.boilerplate_depth <= 0:
                self.in_boilerplate = False
                self.skip_content = False
            return

        # Reset pagenum flag when span closes
        if tag == 'span' and self.in_pagenum:
            self.in_pagenum = False
            return

        # Reset chapter div flag when div closes
        if tag == 'div' and self.in_chapter_div:
            self.in_chapter_div = False

        if self.skip_content or self.in_boilerplate or self.in_toc or self.in_pagenum:
            return

        if self.current_section:
            if tag == 'p':
                content = ''.join(self.current_content).strip()
                if content:
                    self.current_section['content'].append(content + '\n\n')
                self.current_content = []
            elif tag == 'h1':
                raw_content = ''.join(self.current_content)
                content = self._normalize_heading(raw_content)
                if content:
                    # Only set title if not already set
                    if 'title' not in self.current_section:
                        self.current_section['title'] = content
                    self.current_section['content'].append(f'# {content}\n\n')
                self.current_content = []
            elif tag == 'h2':
                raw_content = ''.join(self.current_content)
                content = self._normalize_heading(raw_content)
                if content:
                    # Only set title if not already set
                    if 'title' not in self.current_section:
                        self.current_section['title'] = content
                    self.current_section['content'].append(f'## {content}\n\n')
                self.current_content = []
            elif tag == 'h3':
                raw_content = ''.join(self.current_content)
                content = self._normalize_heading(raw_content)
                if content:
                    # Only set title if not already set
                    if 'title' not in self.current_section:
                        self.current_section['title'] = content
                    self.current_section['content'].append(f'### {content}\n\n')
                self.current_content = []
            elif tag == 'blockquote':
                content = ''.join(self.current_content).strip()
                if content:
                    self.current_section['content'].append(content + '\n\n')
                self.current_content = []
            elif tag == 'em' or tag == 'i':
                self.current_content.append('*')
            elif tag == 'strong' or tag == 'b':
                self.current_content.append('**')
    
    def handle_data(self, data):
        if self.skip_content or self.in_boilerplate or self.in_toc or self.in_pagenum:
            return

        if self.current_section:
            # Preserve the data with its whitespace structure
            if data:
                self.current_content.append(data)
    
    def _normalize_heading(self, raw_content):
        """Normalize heading content: convert line breaks to <br>, clean up spaces."""
        # Convert line breaks to <br>
        content = re.sub(r'[\r\n]+', '<br>', raw_content)
        # Collapse multiple spaces/tabs to single space
        content = re.sub(r'[ \t]+', ' ', content)
        # Clean up spaces around <br>
        content = re.sub(r'\s*<br>\s*', '<br>', content)
        # Remove leading/trailing <br> tags
        content = re.sub(r'^(<br>)+', '', content)
        content = re.sub(r'(<br>)+$', '', content)
        # Final strip
        content = content.strip()
        return content

    def _save_section(self):
        """Save the current section to appropriate list."""
        if not self.current_section:
            return

        # Skip TOC sections - we don't need them as separate files
        if self.current_section['type'] == 'toc':
            self.current_section = None
            return

        content = ''.join(self.current_section['content']).strip()
        if content:
            section_data = {
                'id': self.current_section['id'],
                'title': self.current_section.get('title', self.current_section['id']),
                'content': content,
                'type': self.current_section['type']
            }

            # Chapters, parts, and back matter go to chapters list
            if self.current_section['type'] in ('chapter', 'part', 'back_matter'):
                self.chapters.append(section_data)
            else:
                # Front matter
                self.front_matter.append(section_data)

        self.current_section = None
    
    def get_results(self):
        """Get parsed chapters and front matter."""
        # Save any remaining section
        if self.current_section:
            self._save_section()
        
        return self.front_matter, self.chapters


def download_gutenberg_html(book_id):
    """Download HTML from Project Gutenberg."""
    urls = [
        f"https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}-images.html",
        f"https://www.gutenberg.org/files/{book_id}/{book_id}-h/{book_id}-h.htm",
        f"https://www.gutenberg.org/files/{book_id}/{book_id}-h.htm",
    ]
    
    for url in urls:
        try:
            print(f"Trying: {url}")
            with urlopen(url) as response:
                content = response.read().decode('utf-8')
                print(f"✓ Successfully downloaded from {url}")
                return content
        except URLError as e:
            print(f"✗ Failed: {e}")
            continue
    
    raise Exception(f"Could not download book {book_id} from any HTML URL")


def extract_metadata(html_content):
    """Extract title and author from HTML metadata."""
    title = None
    author = None
    
    # Try meta tags first
    title_match = re.search(r'<meta name="dc\.title" content="([^"]+)"', html_content)
    if title_match:
        title = html.unescape(title_match.group(1))
    
    author_match = re.search(r'<meta name="dc\.creator" content="([^"]+)"', html_content)
    if author_match:
        author = html.unescape(author_match.group(1))
        # Clean up author name if it has dates
        author = re.sub(r'\s*\([^)]+\).*$', '', author)
    
    # Fallback to title tag
    if not title:
        title_match = re.search(r'<title>([^<]+)</title>', html_content)
        if title_match:
            title = html.unescape(title_match.group(1))
            title = re.sub(r'The Project Gutenberg eBook of\s+', '', title, flags=re.IGNORECASE)
    
    return title, author


class WholeBookParser(HTMLParser):
    """Simple parser to extract all text content from Gutenberg HTML."""

    def __init__(self):
        super().__init__()
        self.content = []
        self.in_boilerplate = False
        self.boilerplate_depth = 0
        self.current_text = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)

        # Skip boilerplate
        if 'class' in attrs_dict and 'pg-boilerplate' in attrs_dict['class']:
            self.in_boilerplate = True
            self.boilerplate_depth = 1
            return

        if self.in_boilerplate and tag in ('div', 'section'):
            self.boilerplate_depth += 1
            return

        if self.in_boilerplate:
            return

        # Handle block elements
        if tag == 'p':
            self.current_text = []
        elif tag in ('h1', 'h2', 'h3', 'h4'):
            self.current_text = []
        elif tag == 'br':
            self.current_text.append('  \n')
        elif tag in ('em', 'i'):
            self.current_text.append('*')
        elif tag in ('strong', 'b'):
            self.current_text.append('**')
        elif tag == 'hr':
            self.content.append('\n---\n\n')

    def handle_endtag(self, tag):
        if self.in_boilerplate and tag in ('div', 'section'):
            self.boilerplate_depth -= 1
            if self.boilerplate_depth <= 0:
                self.in_boilerplate = False
            return

        if self.in_boilerplate:
            return

        if tag == 'p':
            text = ''.join(self.current_text).strip()
            if text:
                self.content.append(text + '\n\n')
            self.current_text = []
        elif tag == 'h1':
            text = ''.join(self.current_text).strip()
            if text:
                self.content.append(f'# {text}\n\n')
            self.current_text = []
        elif tag == 'h2':
            text = ''.join(self.current_text).strip()
            if text:
                self.content.append(f'## {text}\n\n')
            self.current_text = []
        elif tag in ('h3', 'h4'):
            text = ''.join(self.current_text).strip()
            if text:
                self.content.append(f'### {text}\n\n')
            self.current_text = []
        elif tag in ('em', 'i'):
            self.current_text.append('*')
        elif tag in ('strong', 'b'):
            self.current_text.append('**')

    def handle_data(self, data):
        if self.in_boilerplate:
            return
        data = data.strip()
        if data:
            self.current_text.append(data + ' ')

    def get_content(self):
        return ''.join(self.content).strip()


def extract_whole_book(html_content, title, author):
    """Extract the entire book as a single section when no chapters are found."""
    parser = WholeBookParser()
    parser.feed(html_content)
    content = parser.get_content()

    if not content:
        return None

    return {
        'id': 'full-text',
        'title': title or 'Full Text',
        'content': content,
        'type': 'chapter'
    }


def normalize_text(text, for_yaml=False):
    """Normalize text by removing weird characters and handling line breaks.

    Args:
        text: The text to normalize
        for_yaml: If True, escape for YAML front matter (always quote, use <br> for line breaks)
    """
    if not text:
        return text

    # Remove page number markers like [vi], [3], [123]
    text = re.sub(r'\[(?:[ivxlc]+|\d+)\]', '', text, flags=re.IGNORECASE)

    # Remove control characters and other weird Unicode
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)

    # Replace line breaks with <br>, max 2 in a row for multiple breaks
    text = re.sub(r'[\r\n]{3,}', '<br><br>', text)
    text = re.sub(r'[\r\n]+', '<br>', text)

    # Normalize whitespace (multiple spaces to single, but preserve <br>)
    text = re.sub(r'[ \t]+', ' ', text)

    # Strip leading/trailing whitespace
    text = text.strip()

    # For YAML, always quote the value
    if for_yaml and text:
        # Escape any existing quotes and wrap in quotes
        text = '"' + text.replace('"', '\\"') + '"'

    return text


def create_markdown_file(section, book_title=None, book_author=None, order=1):
    """Convert section to markdown with front matter."""
    # Normalize title for YAML front matter
    title = normalize_text(section['title'], for_yaml=True)

    front_matter = "---\n"
    front_matter += f"title: {title}\n"
    if book_author:
        # Normalize author for YAML
        author = normalize_text(book_author, for_yaml=True)
        front_matter += f"byline: {author}\n"
    front_matter += f"order: {order}\n"
    front_matter += "---\n\n"

    return front_matter + section['content']


def sanitize_filename(text):
    """Convert text to safe filename."""
    # Remove <br> tags first
    text = re.sub(r'<br\s*/?>', ' ', text, flags=re.IGNORECASE)
    # Remove other HTML-like tags
    text = re.sub(r'<[^>]+>', '', text)
    # Remove problematic filename characters
    text = re.sub(r'[<>:"/\\|?*]', '', text)
    text = re.sub(r'\s+', '-', text)
    text = text.lower().strip('-')
    return text[:50]


def save_chapters(front_matter, chapters, output_dir, book_slug, book_title=None, book_author=None):
    """Save front matter and chapters as markdown files."""
    output_path = Path(output_dir) / book_slug
    output_path.mkdir(parents=True, exist_ok=True)
    
    all_sections = front_matter + chapters
    print(f"\nSaving {len(front_matter)} front matter sections and {len(chapters)} chapters to {output_path}/")
    
    for idx, section in enumerate(all_sections, 1):
        # Determine filename
        if idx <= len(front_matter):
            number = f"00-{idx:02d}"
        else:
            number = f"{idx - len(front_matter):02d}"
        
        filename = f"{number}-{sanitize_filename(section['title'])}.md"
        filepath = output_path / filename
        
        markdown_content = create_markdown_file(section, book_title, book_author, idx)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"  ✓ {filename}")
    
    return output_path


def create_index(front_matter, chapters, output_dir, book_slug, book_title, book_author):
    """Create an index.md file with links to all sections."""
    output_path = Path(output_dir) / book_slug
    index_path = output_path / 'README.md'
    
    content = f"# {book_title}\n\n"
    if book_author:
        content += f"*by {book_author}*\n\n"
    
    if front_matter:
        content += "## Front Matter\n\n"
        for idx, section in enumerate(front_matter, 1):
            number = f"00-{idx:02d}"
            filename = f"{number}-{sanitize_filename(section['title'])}.md"
            content += f"- [{section['title']}]({filename})\n"
        content += "\n"
    
    content += "## Chapters\n\n"
    for idx, chapter in enumerate(chapters, 1):
        number = f"{idx:02d}"
        filename = f"{number}-{sanitize_filename(chapter['title'])}.md"
        content += f"- [{chapter['title']}]({filename})\n"
    
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  ✓ README.md (index)")


def main():
    parser = argparse.ArgumentParser(
        description='Download and split a Project Gutenberg HTML book into markdown chapters.'
    )
    parser.add_argument('book_id', type=str, 
                       help='Project Gutenberg book ID (e.g., 64317 for Great Gatsby)')
    parser.add_argument('--output', '-o', default='./books', 
                       help='Output directory (default: ./books)')
    parser.add_argument('--slug', '-s', 
                       help='Custom folder name (default: book-{id})')
    
    args = parser.parse_args()
    
    book_id = args.book_id
    output_dir = args.output
    book_slug = args.slug or f"book-{book_id}"
    
    print("="*60)
    print(f"Processing Gutenberg book ID: {book_id}")
    
    # Download the HTML
    try:
        html_content = download_gutenberg_html(book_id)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    # Extract metadata
    print("\nExtracting metadata...")
    title, author = extract_metadata(html_content)
    if title:
        print(f"  Title: {title}")
    if author:
        print(f"  Author: {author}")
    
    # Parse HTML to extract chapters
    print("\nParsing HTML and extracting chapters...")
    parser = GutenbergHTMLParser()
    parser.feed(html_content)
    front_matter, chapters = parser.get_results()
    
    print(f"  Found {len(front_matter)} front matter sections")
    print(f"  Found {len(chapters)} chapters")
    
    if not chapters and not front_matter:
        print("  No chapters found - extracting as single document...")
        # Create a single section with all content
        whole_book = extract_whole_book(html_content, title or book_slug, author)
        if whole_book:
            chapters = [whole_book]
        else:
            print("Warning: Could not extract any content!")
            sys.exit(1)
    
    # Save chapters
    output_path = save_chapters(front_matter, chapters, output_dir, book_slug, title, author)
    
    # Create index
    create_index(front_matter, chapters, output_dir, book_slug, title or book_slug, author)
    
    print("\n" + "="*60)
    print(f"✓ Complete! Files saved to: {output_path}")
    print(f"  Front matter sections: {len(front_matter)}")
    print(f"  Chapters: {len(chapters)}")
    print(f"  Total files: {len(front_matter) + len(chapters)}")


if __name__ == '__main__':
    main()