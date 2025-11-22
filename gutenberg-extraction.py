#!/usr/bin/env python3
"""
Gutenberg Extraction Script

A robust script for extracting book data from Project Gutenberg, including:
- Book metadata (title, author, subjects, language, etc.)
- Cover and inline images
- Content converted to markdown files
- A 000-data.yml file with comprehensive book metadata

Usage:
    python gutenberg-extraction.py <book_id> [options]

Example:
    python gutenberg-extraction.py 64317 --output ./books
"""

import re
import os
import sys
import json
import argparse
import time
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from urllib.parse import urljoin, urlparse
from html.parser import HTMLParser
from datetime import datetime
import html
from typing import Optional, Dict, List, Tuple, Any


# =============================================================================
# Configuration
# =============================================================================

# Gutenberg URL patterns
GUTENBERG_URLS = {
    'html_images': 'https://www.gutenberg.org/cache/epub/{id}/pg{id}-images.html',
    'html_simple': 'https://www.gutenberg.org/files/{id}/{id}-h/{id}-h.htm',
    'html_alt': 'https://www.gutenberg.org/files/{id}/{id}-h.htm',
    'cover_medium': 'https://www.gutenberg.org/cache/epub/{id}/pg{id}.cover.medium.jpg',
    'cover_small': 'https://www.gutenberg.org/cache/epub/{id}/pg{id}.cover.small.jpg',
    'rdf': 'https://www.gutenberg.org/ebooks/{id}.rdf',
    'json_metadata': 'https://gutendex.com/books/{id}/',  # Third-party API with rich metadata
    'book_page': 'https://www.gutenberg.org/ebooks/{id}',
}

# Request headers to avoid being blocked
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
}

# Retry configuration
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds

# Text-based boilerplate markers (per extraction guide)
START_MARKERS = [
    "*** START OF THIS PROJECT GUTENBERG EBOOK",
    "*** START OF THE PROJECT GUTENBERG EBOOK",
    "*** START OF THE PROJECT GUTENBERG ETEXT",
    "*END*THE SMALL PRINT",  # older books
    "***START OF THE PROJECT GUTENBERG",
]

END_MARKERS = [
    "End of the Project Gutenberg EBook",
    "End of Project Gutenberg's",
    "*** END OF THIS PROJECT GUTENBERG EBOOK",
    "*** END OF THE PROJECT GUTENBERG EBOOK",
    "End of this Project Gutenberg",
    "*** END OF THE PROJECT GUTENBERG",
]

# Chapter heading patterns
CHAPTER_PATTERNS = [
    r'^chapter\s+[ivxlcdm\d]+',  # Chapter I, Chapter 1, etc.
    r'^chap\.\s*[ivxlcdm\d]+',   # Chap. I, Chap. 1
    r'^[ivxlcdm]+\.$',           # I., II., III. (roman numerals with period)
    r'^\d+\.$',                   # 1., 2., 3.
    r'^letter\s+[ivxlcdm\d]+',   # Letter I, Letter 1 (for epistolary novels)
    r'^volume\s+[ivxlcdm\d]+',   # Volume I
    r'^book\s+[ivxlcdm\d]+',     # Book I
    r'^part\s+[ivxlcdm\d]+',     # Part I
]

# Front/back matter keywords
FRONT_MATTER_KEYWORDS = [
    'preface', 'introduction', 'foreword', 'prologue', 'dedication',
    'acknowledgment', 'acknowledgement', 'note to the reader', 'author\'s note',
    'contents', 'table of contents',
]

BACK_MATTER_KEYWORDS = [
    'epilogue', 'afterword', 'appendix', 'notes', 'endnotes', 'footnotes',
    'glossary', 'index', 'bibliography', 'about the author',
]


# =============================================================================
# Boilerplate Removal (Text-based, per extraction guide)
# =============================================================================

def remove_gutenberg_boilerplate(html_text: str) -> str:
    """Remove Project Gutenberg header and footer boilerplate using text markers.

    This is the most reliable method per the extraction guide - text markers
    are consistent across all eras of digitization.
    """
    lines = html_text.split('\n')

    start_line = 0
    end_line = len(lines)

    # Find content start (after header) - case insensitive
    for i, line in enumerate(lines):
        line_upper = line.upper()
        if any(marker.upper() in line_upper for marker in START_MARKERS):
            start_line = i + 1
            break

    # Find content end (before footer) - only check after line 100 to avoid false positives
    for i in range(max(100, start_line), len(lines)):
        line_upper = lines[i].upper()
        if any(marker.upper() in line_upper for marker in END_MARKERS):
            end_line = i
            break

    return '\n'.join(lines[start_line:end_line])


def extract_metadata_from_body_text(html_text: str) -> Dict[str, Any]:
    """Extract metadata from plain text header in Project Gutenberg books.

    This is more reliable than Dublin Core meta tags because it appears
    in virtually every book.
    """
    metadata = {}

    # Only look in the first ~150 lines for header metadata
    header_text = '\n'.join(html_text.split('\n')[:150])

    # Title pattern
    title_match = re.search(r'Title:\s*(.+?)(?:\n|Author:|Release)', header_text, re.IGNORECASE)
    if title_match:
        metadata['title'] = title_match.group(1).strip()

    # Author pattern
    author_match = re.search(r'Author:\s*(.+?)(?:\n|\r|Release|Illustrator|Editor|Translator)', header_text, re.IGNORECASE)
    if author_match:
        author = author_match.group(1).strip()
        # Clean up author name
        author = re.sub(r'\s*\([^)]+\)\s*$', '', author)  # Remove dates in parens
        metadata['author'] = author

    # Language pattern
    lang_match = re.search(r'Language:\s*(\w+)', header_text, re.IGNORECASE)
    if lang_match:
        lang = lang_match.group(1).strip().lower()
        # Convert full names to ISO codes
        lang_map = {'english': 'en', 'french': 'fr', 'german': 'de', 'spanish': 'es', 'italian': 'it'}
        metadata['language'] = lang_map.get(lang, lang)

    # Book ID
    ebook_match = re.search(r'\[(?:EBook|E-?text)\s*#?(\d+)\]', header_text, re.IGNORECASE)
    if ebook_match:
        metadata['ebook_id'] = ebook_match.group(1)

    # Release date
    date_match = re.search(r'Release Date:\s*(.+?)(?:\s*\[|\n|\r)', header_text, re.IGNORECASE)
    if date_match:
        metadata['release_date'] = date_match.group(1).strip()

    # Posting date (older format)
    if 'release_date' not in metadata:
        posting_match = re.search(r'Posting Date:\s*(.+?)(?:\s*\[|\n|\r)', header_text, re.IGNORECASE)
        if posting_match:
            metadata['release_date'] = posting_match.group(1).strip()

    return metadata


def is_chapter_heading(text: str) -> Tuple[bool, str]:
    """Check if text is a chapter heading and return the type.

    Returns (is_chapter, section_type) tuple.
    """
    text_clean = text.strip().lower()
    text_clean = re.sub(r'<[^>]+>', '', text_clean)  # Remove any HTML tags
    text_clean = re.sub(r'\s+', ' ', text_clean).strip()

    # Check for chapter patterns
    for pattern in CHAPTER_PATTERNS:
        if re.match(pattern, text_clean, re.IGNORECASE):
            return True, 'chapter'

    # Check for front matter
    for keyword in FRONT_MATTER_KEYWORDS:
        if text_clean == keyword or text_clean.startswith(keyword + ' ') or text_clean.endswith(' ' + keyword):
            if 'contents' in keyword or 'table' in keyword:
                return True, 'toc'
            return True, 'front_matter'

    # Check for back matter
    for keyword in BACK_MATTER_KEYWORDS:
        if text_clean == keyword or text_clean.startswith(keyword + ' '):
            return True, 'back_matter'

    return False, ''


# =============================================================================
# Utility Functions
# =============================================================================

def make_request(url: str, binary: bool = False, timeout: int = 30) -> Optional[bytes | str]:
    """Make an HTTP request with retries and error handling."""
    import subprocess
    import shutil

    # First try with urllib
    for attempt in range(MAX_RETRIES):
        try:
            request = Request(url, headers=HEADERS)
            with urlopen(request, timeout=timeout) as response:
                content = response.read()
                if binary:
                    return content
                return content.decode('utf-8', errors='replace')
        except HTTPError as e:
            if e.code == 404:
                # Try wget/curl as fallback before giving up on 404
                break
            if attempt == MAX_RETRIES - 1:
                break
        except URLError as e:
            if attempt == MAX_RETRIES - 1:
                break
        except Exception as e:
            if attempt == MAX_RETRIES - 1:
                break

        time.sleep(RETRY_DELAY * (attempt + 1))

    # Fallback: Try wget
    if shutil.which('wget'):
        try:
            result = subprocess.run(
                ['wget', '-q', '-O', '-', '--timeout=30', url],
                capture_output=True,
                timeout=timeout + 10
            )
            if result.returncode == 0 and result.stdout:
                if binary:
                    return result.stdout
                return result.stdout.decode('utf-8', errors='replace')
        except Exception:
            pass

    # Fallback: Try curl
    if shutil.which('curl'):
        try:
            result = subprocess.run(
                ['curl', '-s', '-L', '--max-time', str(timeout), url],
                capture_output=True,
                timeout=timeout + 10
            )
            if result.returncode == 0 and result.stdout:
                if binary:
                    return result.stdout
                return result.stdout.decode('utf-8', errors='replace')
        except Exception:
            pass

    return None


def sanitize_filename(text: str, max_length: int = 50) -> str:
    """Convert text to safe filename."""
    if not text:
        return "untitled"

    # Remove HTML tags and entities
    text = re.sub(r'<[^>]+>', '', text)
    text = html.unescape(text)

    # Remove problematic filename characters
    text = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '', text)
    text = re.sub(r'\s+', '-', text)
    text = text.lower().strip('-')

    # Limit length
    if len(text) > max_length:
        text = text[:max_length].rsplit('-', 1)[0]

    return text or "untitled"


def normalize_text(text: str, for_yaml: bool = False) -> str:
    """Normalize text by cleaning up whitespace and special characters."""
    if not text:
        return ""

    # Remove page number markers like [vi], [3], [123]
    text = re.sub(r'\[(?:[ivxlc]+|\d+)\]', '', text, flags=re.IGNORECASE)

    # Remove control characters
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)

    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    if for_yaml:
        # Escape quotes and special YAML characters
        if any(c in text for c in [':', '#', '[', ']', '{', '}', '&', '*', '!', '|', '>', "'", '"', '%', '@', '`']):
            text = '"' + text.replace('\\', '\\\\').replace('"', '\\"') + '"'
        elif text.startswith('-') or text.startswith('?'):
            text = '"' + text + '"'

    return text


def create_slug(title: str, author: str = None, book_id: str = None) -> str:
    """Create a URL-friendly slug for the book."""
    parts = []

    if author:
        # Get last name only
        author_clean = re.sub(r'\s*\([^)]+\)', '', author)  # Remove dates in parens
        names = author_clean.split(',')[0].split()  # Handle "Last, First" format
        if names:
            parts.append(sanitize_filename(names[0], 20))

    if title:
        parts.append(sanitize_filename(title, 40))

    if book_id:
        parts.append(f"pg{book_id}")

    return '-'.join(parts) if parts else f"book-{book_id}"


# =============================================================================
# Metadata Extraction
# =============================================================================

class MetadataExtractor:
    """Extract metadata from various Gutenberg sources."""

    def __init__(self, book_id: str):
        self.book_id = book_id
        self.metadata = {
            'book_id': book_id,
            'title': None,
            'author': None,
            'authors': [],
            'language': None,
            'subjects': [],
            'bookshelves': [],
            'publication_date': None,
            'rights': None,
            'download_count': None,
            'gutenberg_url': f"https://www.gutenberg.org/ebooks/{book_id}",
            'formats': {},
            'extracted_at': datetime.now().isoformat(),
        }

    def extract_from_html(self, html_content: str) -> None:
        """Extract metadata from HTML meta tags."""
        # Dublin Core metadata
        meta_patterns = {
            'title': r'<meta\s+name="dc\.title"\s+content="([^"]+)"',
            'author': r'<meta\s+name="dc\.creator"\s+content="([^"]+)"',
            'language': r'<meta\s+name="dc\.language"\s+content="([^"]+)"',
            'rights': r'<meta\s+name="dc\.rights"\s+content="([^"]+)"',
            'subject': r'<meta\s+name="dc\.subject"\s+content="([^"]+)"',
        }

        for key, pattern in meta_patterns.items():
            matches = re.findall(pattern, html_content, re.IGNORECASE)
            if matches:
                if key == 'subject':
                    self.metadata['subjects'].extend([html.unescape(m) for m in matches])
                else:
                    value = html.unescape(matches[0])
                    if key == 'author':
                        # Clean up author name (remove dates)
                        value = re.sub(r'\s*\([^)]+\)\s*$', '', value)
                        self.metadata['author'] = value
                        if value not in self.metadata['authors']:
                            self.metadata['authors'].append(value)
                    else:
                        self.metadata[key] = value

        # Fallback: Extract title from <title> tag
        if not self.metadata['title']:
            title_match = re.search(r'<title>([^<]+)</title>', html_content, re.IGNORECASE)
            if title_match:
                title = html.unescape(title_match.group(1))
                title = re.sub(r'The Project Gutenberg eBook of\s+', '', title, flags=re.IGNORECASE)
                title = re.sub(r',?\s*by\s+.*$', '', title, flags=re.IGNORECASE)
                self.metadata['title'] = title.strip()

    def extract_from_gutendex(self) -> None:
        """Extract metadata from Gutendex API (rich JSON metadata)."""
        url = GUTENBERG_URLS['json_metadata'].format(id=self.book_id)
        print(f"  Fetching metadata from Gutendex API...")

        content = make_request(url)
        if not content:
            print(f"  Warning: Could not fetch Gutendex metadata")
            return

        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            print(f"  Warning: Invalid JSON from Gutendex")
            return

        # Extract rich metadata
        if data.get('title'):
            self.metadata['title'] = data['title']

        if data.get('authors'):
            self.metadata['authors'] = []
            for author in data['authors']:
                name = author.get('name', '')
                if name:
                    # Handle "Last, First" format
                    if ',' in name:
                        parts = name.split(',', 1)
                        name = f"{parts[1].strip()} {parts[0].strip()}"
                    self.metadata['authors'].append(name)
            if self.metadata['authors']:
                self.metadata['author'] = self.metadata['authors'][0]

        if data.get('languages'):
            self.metadata['language'] = data['languages'][0] if data['languages'] else None

        if data.get('subjects'):
            self.metadata['subjects'] = data['subjects']

        if data.get('bookshelves'):
            self.metadata['bookshelves'] = data['bookshelves']

        if data.get('download_count'):
            self.metadata['download_count'] = data['download_count']

        if data.get('copyright') is not None:
            self.metadata['rights'] = 'Copyrighted' if data['copyright'] else 'Public Domain'

        if data.get('formats'):
            self.metadata['formats'] = data['formats']

    def extract_from_rdf(self) -> None:
        """Extract metadata from RDF file (most authoritative source)."""
        url = GUTENBERG_URLS['rdf'].format(id=self.book_id)
        print(f"  Fetching RDF metadata...")

        content = make_request(url)
        if not content:
            print(f"  Warning: Could not fetch RDF metadata")
            return

        # Simple RDF parsing (avoiding external dependencies)
        title_match = re.search(r'<dcterms:title>([^<]+)</dcterms:title>', content)
        if title_match:
            self.metadata['title'] = html.unescape(title_match.group(1))

        # Extract creator/author
        creator_match = re.search(r'<pgterms:name>([^<]+)</pgterms:name>', content)
        if creator_match:
            name = html.unescape(creator_match.group(1))
            # Handle "Last, First" format
            if ',' in name:
                parts = name.split(',', 1)
                name = f"{parts[1].strip()} {parts[0].strip()}"
            self.metadata['author'] = name
            if name not in self.metadata['authors']:
                self.metadata['authors'].append(name)

        # Extract language
        lang_match = re.search(r'<dcterms:language[^>]*>\s*<rdf:Description[^>]*>\s*<rdf:value[^>]*>([^<]+)</rdf:value>', content, re.DOTALL)
        if lang_match:
            self.metadata['language'] = lang_match.group(1).strip()

        # Extract subjects
        subject_matches = re.findall(r'<dcterms:subject[^>]*>\s*<rdf:Description[^>]*>\s*<rdf:value>([^<]+)</rdf:value>', content, re.DOTALL)
        for subj in subject_matches:
            subj = html.unescape(subj.strip())
            if subj and subj not in self.metadata['subjects']:
                self.metadata['subjects'].append(subj)

        # Extract publication date
        issued_match = re.search(r'<dcterms:issued[^>]*>([^<]+)</dcterms:issued>', content)
        if issued_match:
            self.metadata['publication_date'] = issued_match.group(1).strip()

    def get_metadata(self) -> Dict[str, Any]:
        """Get all extracted metadata."""
        return self.metadata


# =============================================================================
# Image Extraction
# =============================================================================

class ImageExtractor:
    """Extract and download images from Gutenberg books."""

    def __init__(self, book_id: str, output_dir: Path):
        self.book_id = book_id
        self.output_dir = output_dir
        self.images_dir = output_dir / 'images'
        self.downloaded_images = []
        self.cover_image = None

    def download_cover(self) -> Optional[str]:
        """Download the cover image."""
        self.images_dir.mkdir(parents=True, exist_ok=True)

        # Try medium cover first, then small
        cover_urls = [
            GUTENBERG_URLS['cover_medium'].format(id=self.book_id),
            GUTENBERG_URLS['cover_small'].format(id=self.book_id),
        ]

        for url in cover_urls:
            print(f"  Trying cover: {url}")
            content = make_request(url, binary=True)
            if content:
                # Determine extension from URL
                ext = '.jpg'
                if '.png' in url.lower():
                    ext = '.png'

                filename = f"cover{ext}"
                filepath = self.images_dir / filename

                with open(filepath, 'wb') as f:
                    f.write(content)

                self.cover_image = filename
                self.downloaded_images.append({
                    'filename': filename,
                    'source_url': url,
                    'type': 'cover'
                })
                print(f"  ✓ Downloaded cover: {filename}")
                return filename

        print(f"  Warning: No cover image found")
        return None

    def extract_images_from_html(self, html_content: str, base_url: str) -> List[Dict]:
        """Extract and download images referenced in HTML content."""
        self.images_dir.mkdir(parents=True, exist_ok=True)

        # Find all image tags
        img_pattern = r'<img[^>]+src=["\']([^"\']+)["\'][^>]*>'
        matches = re.findall(img_pattern, html_content, re.IGNORECASE)

        inline_images = []
        for idx, src in enumerate(matches, 1):
            # Skip data URIs
            if src.startswith('data:'):
                continue

            # Resolve relative URLs
            if not src.startswith('http'):
                src = urljoin(base_url, src)

            # Download the image
            print(f"  Downloading image {idx}: {src}")
            content = make_request(src, binary=True)
            if not content:
                continue

            # Determine filename
            parsed = urlparse(src)
            original_name = Path(parsed.path).name
            ext = Path(original_name).suffix or '.jpg'

            # Create safe filename
            safe_name = sanitize_filename(Path(original_name).stem, 30)
            filename = f"img-{idx:03d}-{safe_name}{ext}"
            filepath = self.images_dir / filename

            with open(filepath, 'wb') as f:
                f.write(content)

            image_info = {
                'filename': filename,
                'source_url': src,
                'original_name': original_name,
                'type': 'inline'
            }
            inline_images.append(image_info)
            self.downloaded_images.append(image_info)
            print(f"  ✓ Downloaded: {filename}")

        return inline_images

    def get_results(self) -> Dict:
        """Get summary of downloaded images."""
        return {
            'cover': self.cover_image,
            'images': self.downloaded_images,
            'images_dir': str(self.images_dir.relative_to(self.output_dir.parent)) if self.images_dir.exists() else None
        }


# =============================================================================
# HTML to Markdown Conversion
# =============================================================================

class GutenbergHTMLParser(HTMLParser):
    """Parse Project Gutenberg HTML to extract chapters and content."""

    # Known section types
    FRONT_MATTER_IDS = {
        'dedication', 'preface', 'introduction', 'prologue', 'foreword',
        'contents', 'acknowledgments', 'acknowledgements', 'note', 'notes'
    }
    BACK_MATTER_IDS = {
        'epilogue', 'afterword', 'appendix', 'footnotes', 'endnotes',
        'bibliography', 'glossary', 'index'
    }

    def __init__(self):
        super().__init__()
        self.sections = []
        self.current_section = None
        self.current_content = []
        self.tag_stack = []
        self.in_boilerplate = False
        self.boilerplate_depth = 0
        self.in_toc = False
        self.in_pagenum = False
        self.skip_content = False
        self.images_found = []
        self.pending_heading_text = []  # Track heading text for chapter detection
        self.in_heading = False  # Are we inside a heading tag?
        self.current_heading_tag = None  # Which heading tag?

    def _detect_section_type(self, section_id: str) -> str:
        """Determine section type from ID."""
        section_id_lower = section_id.lower()

        if section_id_lower in self.FRONT_MATTER_IDS or section_id_lower.startswith('front'):
            return 'front_matter'
        if section_id_lower in self.BACK_MATTER_IDS or section_id_lower.startswith('back'):
            return 'back_matter'
        if section_id_lower.startswith('part'):
            return 'part'
        if section_id_lower in ('contents', 'toc', 'table-of-contents'):
            return 'toc'
        return 'chapter'

    def _is_chapter_start(self, tag: str, attrs: Dict) -> Tuple[bool, Optional[str], Optional[str]]:
        """Check if this tag marks the start of a chapter/section."""
        # Strategy 1: div/section with meaningful id
        if tag in ('div', 'section') and 'id' in attrs:
            div_id = attrs['id']
            div_id_lower = div_id.lower()

            # Skip Gutenberg-specific sections
            if 'gutenberg' in div_id_lower or 'license' in div_id_lower or 'boilerplate' in div_id_lower:
                return False, None, None

            # Check for chapter patterns
            if (div_id_lower.startswith('chapter') or
                div_id_lower.startswith('chap') or
                re.match(r'^ch[_-]?\d+', div_id_lower) or
                re.match(r'^[ivxlc]+$', div_id_lower) or
                re.match(r'^\d+$', div_id)):
                return True, div_id, 'chapter'

            section_type = self._detect_section_type(div_id)
            if section_type != 'chapter':
                return True, div_id, section_type

        # Strategy 2: h2/h3 with id (common chapter headers)
        if tag in ('h2', 'h3') and 'id' in attrs:
            heading_id = attrs['id']
            heading_id_lower = heading_id.lower()

            # Skip boilerplate
            if 'gutenberg' in heading_id_lower or 'license' in heading_id_lower:
                return False, None, None

            section_type = self._detect_section_type(heading_id)
            return True, heading_id, section_type

        return False, None, None

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        self.tag_stack.append(tag)

        # Handle boilerplate sections
        if 'class' in attrs_dict and 'pg-boilerplate' in attrs_dict['class']:
            self.in_boilerplate = True
            self.boilerplate_depth = 1
            self.skip_content = True
            return

        if self.in_boilerplate and tag in ('div', 'section'):
            self.boilerplate_depth += 1
            return

        # Skip page numbers
        if tag == 'span' and 'class' in attrs_dict:
            if 'pagenum' in attrs_dict['class'].lower():
                self.in_pagenum = True
                return

        if self.skip_content or self.in_boilerplate:
            return

        # Check for chapter/section start
        is_chapter, section_id, section_type = self._is_chapter_start(tag, attrs_dict)

        if is_chapter and section_id:
            # Save previous section
            if self.current_section:
                self._save_section()

            if section_type == 'toc':
                self.in_toc = True
                self.current_section = None
                return

            self.in_toc = False
            self.current_section = {
                'id': section_id,
                'type': section_type,
                'title': None,
                'content': []
            }
            return

        if self.in_toc:
            return

        # Track images
        if tag == 'img' and 'src' in attrs_dict:
            self.images_found.append(attrs_dict['src'])
            if self.current_section:
                alt = attrs_dict.get('alt', '')
                self.current_content.append(f'\n![{alt}]({attrs_dict["src"]})\n')

        # Track when entering heading tags (for text-based chapter detection)
        if tag in ('h1', 'h2', 'h3', 'h4'):
            self.in_heading = True
            self.current_heading_tag = tag
            self.pending_heading_text = []

        # Format tags
        if self.current_section and not self.in_boilerplate:
            if tag == 'p':
                self.current_content = []
            elif tag in ('h1', 'h2', 'h3', 'h4'):
                self.current_content = []
            elif tag == 'hr':
                self.current_section['content'].append('\n---\n')
            elif tag == 'blockquote':
                self.current_content = []
            elif tag in ('em', 'i'):
                self.current_content.append('*')
            elif tag in ('strong', 'b'):
                self.current_content.append('**')
            elif tag == 'br':
                self.current_content.append('  \n')
            elif tag == 'li':
                self.current_content = ['- ']

    def handle_endtag(self, tag):
        if self.tag_stack and self.tag_stack[-1] == tag:
            self.tag_stack.pop()

        # Track boilerplate depth
        if self.in_boilerplate and tag in ('div', 'section'):
            self.boilerplate_depth -= 1
            if self.boilerplate_depth <= 0:
                self.in_boilerplate = False
                self.skip_content = False
            return

        if tag == 'span' and self.in_pagenum:
            self.in_pagenum = False
            return

        # Text-based chapter detection: when a heading closes, check if it's a chapter
        if tag in ('h1', 'h2', 'h3', 'h4') and self.in_heading:
            heading_text = ''.join(self.pending_heading_text).strip()
            self.in_heading = False
            self.current_heading_tag = None

            # Check if this heading marks a chapter/section (by TEXT content)
            is_chapter, section_type = is_chapter_heading(heading_text)

            if is_chapter and not self.in_boilerplate and not self.skip_content:
                # Save any previous section
                if self.current_section:
                    self._save_section()

                if section_type == 'toc':
                    self.in_toc = True
                    self.current_section = None
                else:
                    self.in_toc = False
                    # Create a safe ID from heading text
                    safe_id = re.sub(r'[^a-z0-9]+', '-', heading_text.lower()).strip('-')[:50]
                    self.current_section = {
                        'id': safe_id or f'section-{len(self.sections)+1}',
                        'type': section_type,
                        'title': heading_text,
                        'content': []
                    }
                    # Add the heading to content
                    level = {'h1': '#', 'h2': '##', 'h3': '###', 'h4': '###'}[tag]
                    self.current_section['content'].append(f'{level} {heading_text}\n\n')

                self.pending_heading_text = []
                self.current_content = []
                return

        if self.skip_content or self.in_boilerplate or self.in_toc or self.in_pagenum:
            return

        if self.current_section:
            content = ''.join(self.current_content).strip()

            if tag == 'p':
                if content:
                    self.current_section['content'].append(content + '\n\n')
                self.current_content = []
            elif tag == 'h1':
                if content:
                    if not self.current_section['title']:
                        self.current_section['title'] = content
                    self.current_section['content'].append(f'# {content}\n\n')
                self.current_content = []
            elif tag == 'h2':
                if content:
                    if not self.current_section['title']:
                        self.current_section['title'] = content
                    self.current_section['content'].append(f'## {content}\n\n')
                self.current_content = []
            elif tag in ('h3', 'h4'):
                if content:
                    if not self.current_section['title']:
                        self.current_section['title'] = content
                    self.current_section['content'].append(f'### {content}\n\n')
                self.current_content = []
            elif tag == 'blockquote':
                if content:
                    # Add blockquote markers to each line
                    lines = content.split('\n')
                    quoted = '\n'.join('> ' + line.strip() for line in lines if line.strip())
                    self.current_section['content'].append(quoted + '\n\n')
                self.current_content = []
            elif tag == 'li':
                if content:
                    self.current_section['content'].append(content + '\n')
                self.current_content = []
            elif tag in ('ul', 'ol'):
                self.current_section['content'].append('\n')
            elif tag in ('em', 'i'):
                self.current_content.append('*')
            elif tag in ('strong', 'b'):
                self.current_content.append('**')

    def handle_data(self, data):
        # Always collect heading text for chapter detection (even before we have a section)
        if self.in_heading and data:
            self.pending_heading_text.append(data)

        if self.skip_content or self.in_boilerplate or self.in_toc or self.in_pagenum:
            return

        if self.current_section and data:
            self.current_content.append(data)

    def _save_section(self):
        """Save the current section."""
        if not self.current_section:
            return

        # Skip TOC
        if self.current_section['type'] == 'toc':
            self.current_section = None
            return

        content = ''.join(self.current_section['content']).strip()
        if content:
            self.sections.append({
                'id': self.current_section['id'],
                'title': self.current_section.get('title') or self.current_section['id'],
                'content': content,
                'type': self.current_section['type']
            })

        self.current_section = None

    def get_results(self) -> Tuple[List[Dict], List[Dict], List[str]]:
        """Get parsed sections."""
        if self.current_section:
            self._save_section()

        front_matter = [s for s in self.sections if s['type'] == 'front_matter']
        chapters = [s for s in self.sections if s['type'] in ('chapter', 'part', 'back_matter')]

        return front_matter, chapters, self.images_found


class WholeBookParser(HTMLParser):
    """Extract entire book as single section when no chapters found."""

    def __init__(self):
        super().__init__()
        self.content = []
        self.current_text = []
        self.in_boilerplate = False
        self.boilerplate_depth = 0

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)

        if 'class' in attrs_dict and 'pg-boilerplate' in attrs_dict['class']:
            self.in_boilerplate = True
            self.boilerplate_depth = 1
            return

        if self.in_boilerplate and tag in ('div', 'section'):
            self.boilerplate_depth += 1
            return

        if self.in_boilerplate:
            return

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

        text = ''.join(self.current_text).strip()
        if tag == 'p' and text:
            self.content.append(text + '\n\n')
            self.current_text = []
        elif tag == 'h1' and text:
            self.content.append(f'# {text}\n\n')
            self.current_text = []
        elif tag == 'h2' and text:
            self.content.append(f'## {text}\n\n')
            self.current_text = []
        elif tag in ('h3', 'h4') and text:
            self.content.append(f'### {text}\n\n')
            self.current_text = []
        elif tag in ('em', 'i'):
            self.current_text.append('*')
        elif tag in ('strong', 'b'):
            self.current_text.append('**')

    def handle_data(self, data):
        if not self.in_boilerplate and data:
            self.current_text.append(data)

    def get_content(self) -> str:
        return ''.join(self.content).strip()


# =============================================================================
# Output Generation
# =============================================================================

def create_yaml_data(metadata: Dict, images: Dict, sections_info: Dict) -> str:
    """Create the 000-data.yml content."""
    lines = ['# Book Metadata', '# Generated by gutenberg-extraction.py', '']

    # Core metadata
    lines.append('# === Core Metadata ===')
    lines.append(f'book_id: "{metadata.get("book_id", "")}"')
    lines.append(f'title: {normalize_text(metadata.get("title", ""), for_yaml=True)}')

    if metadata.get('author'):
        lines.append(f'author: {normalize_text(metadata.get("author", ""), for_yaml=True)}')

    if metadata.get('authors') and len(metadata['authors']) > 1:
        lines.append('authors:')
        for author in metadata['authors']:
            lines.append(f'  - {normalize_text(author, for_yaml=True)}')

    if metadata.get('language'):
        lines.append(f'language: "{metadata["language"]}"')

    if metadata.get('publication_date'):
        lines.append(f'publication_date: "{metadata["publication_date"]}"')

    if metadata.get('rights'):
        lines.append(f'rights: {normalize_text(metadata.get("rights", ""), for_yaml=True)}')

    lines.append('')
    lines.append('# === Source Information ===')
    lines.append(f'gutenberg_url: "{metadata.get("gutenberg_url", "")}"')
    if metadata.get('download_count'):
        lines.append(f'download_count: {metadata["download_count"]}')
    lines.append(f'extracted_at: "{metadata.get("extracted_at", "")}"')

    # Subjects
    if metadata.get('subjects'):
        lines.append('')
        lines.append('# === Subjects ===')
        lines.append('subjects:')
        for subject in metadata['subjects']:
            lines.append(f'  - {normalize_text(subject, for_yaml=True)}')

    # Bookshelves
    if metadata.get('bookshelves'):
        lines.append('')
        lines.append('# === Bookshelves ===')
        lines.append('bookshelves:')
        for shelf in metadata['bookshelves']:
            lines.append(f'  - {normalize_text(shelf, for_yaml=True)}')

    # Images
    if images.get('cover') or images.get('images'):
        lines.append('')
        lines.append('# === Images ===')
        if images.get('cover'):
            lines.append(f'cover_image: "images/{images["cover"]}"')
        if images.get('images'):
            lines.append(f'image_count: {len(images["images"])}')

    # Sections info
    lines.append('')
    lines.append('# === Content Structure ===')
    lines.append(f'front_matter_count: {sections_info.get("front_matter_count", 0)}')
    lines.append(f'chapter_count: {sections_info.get("chapter_count", 0)}')
    lines.append(f'total_sections: {sections_info.get("total_sections", 0)}')

    if sections_info.get('files'):
        lines.append('')
        lines.append('# === Generated Files ===')
        lines.append('files:')
        for f in sections_info['files']:
            lines.append(f'  - "{f}"')

    return '\n'.join(lines) + '\n'


def create_markdown_file(section: Dict, metadata: Dict, order: int) -> str:
    """Create markdown file content with front matter."""
    title = normalize_text(section['title'], for_yaml=True)

    fm_lines = ['---']
    fm_lines.append(f'title: {title}')

    if metadata.get('author'):
        fm_lines.append(f'byline: {normalize_text(metadata.get("author", ""), for_yaml=True)}')

    fm_lines.append(f'order: {order}')
    fm_lines.append(f'section_type: "{section["type"]}"')
    fm_lines.append('---')
    fm_lines.append('')

    return '\n'.join(fm_lines) + section['content']


def save_markdown_files(front_matter: List[Dict], chapters: List[Dict],
                        output_dir: Path, metadata: Dict) -> List[str]:
    """Save all markdown files and return list of filenames."""
    output_dir.mkdir(parents=True, exist_ok=True)

    all_sections = front_matter + chapters
    saved_files = []

    print(f"\nSaving {len(front_matter)} front matter sections and {len(chapters)} chapters...")

    for idx, section in enumerate(all_sections, 1):
        # Create filename
        if idx <= len(front_matter):
            number = f"00-{idx:02d}"
        else:
            number = f"{idx - len(front_matter):02d}"

        filename = f"{number}-{sanitize_filename(section['title'])}.md"
        filepath = output_dir / filename

        content = create_markdown_file(section, metadata, idx)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        saved_files.append(filename)
        print(f"  ✓ {filename}")

    return saved_files


# =============================================================================
# Main Extraction Process
# =============================================================================

def download_html(book_id: str) -> Tuple[Optional[str], Optional[str]]:
    """Download HTML content from Project Gutenberg."""
    urls = [
        GUTENBERG_URLS['html_images'].format(id=book_id),
        GUTENBERG_URLS['html_simple'].format(id=book_id),
        GUTENBERG_URLS['html_alt'].format(id=book_id),
    ]

    for url in urls:
        print(f"  Trying: {url}")
        content = make_request(url)
        if content:
            print(f"  ✓ Downloaded HTML from {url}")
            return content, url

    return None, None


def extract_book(book_id: str, output_base: str = './books', slug: str = None,
                 skip_images: bool = False, download_all_images: bool = False,
                 local_html: str = None) -> bool:
    """
    Main extraction function.

    Args:
        book_id: Project Gutenberg book ID
        output_base: Base output directory
        slug: Custom folder name (optional)
        skip_images: Skip downloading images entirely
        download_all_images: Download all inline images, not just cover
        local_html: Path to local HTML file (optional, skips download)

    Returns:
        True if successful, False otherwise
    """
    print("=" * 60)
    print(f"Extracting Project Gutenberg Book #{book_id}")
    print("=" * 60)

    html_content = None
    html_url = None

    # Check for local HTML file first
    if local_html:
        print(f"\n[1/5] Loading local HTML file: {local_html}")
        try:
            with open(local_html, 'r', encoding='utf-8', errors='replace') as f:
                html_content = f.read()
            html_url = f"file://{Path(local_html).absolute()}"
            print(f"  ✓ Loaded {len(html_content)} bytes")
        except Exception as e:
            print(f"  ERROR: Could not read local file: {e}")
            return False

        # Extract metadata from local HTML
        print("\n[2/5] Extracting metadata from HTML...")
        meta_extractor = MetadataExtractor(book_id)
        meta_extractor.extract_from_html(html_content)
    else:
        # Step 1: Fetch metadata from online sources
        print("\n[1/5] Extracting metadata...")
        meta_extractor = MetadataExtractor(book_id)
        meta_extractor.extract_from_gutendex()  # Try rich API first
        meta_extractor.extract_from_rdf()  # Then authoritative RDF

        # Step 2: Download HTML
        print("\n[2/5] Downloading HTML content...")
        html_content, html_url = download_html(book_id)
        if not html_content:
            print("ERROR: Could not download HTML from any source")
            print("\nTIP: You can download the HTML manually and use --local-html flag:")
            print(f"     wget -O book.html 'https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}-images.html'")
            print(f"     python gutenberg-extraction.py {book_id} --local-html book.html")
            return False

        # Extract metadata from HTML as additional source
        meta_extractor.extract_from_html(html_content)

    # Also extract metadata from body text (most reliable per extraction guide)
    body_metadata = extract_metadata_from_body_text(html_content)
    # Merge body text metadata (use as fallback for missing fields)
    current_metadata = meta_extractor.get_metadata()
    for key, value in body_metadata.items():
        if key not in current_metadata or not current_metadata[key]:
            meta_extractor.metadata[key] = value

    metadata = meta_extractor.get_metadata()

    print(f"  Title: {metadata.get('title', 'Unknown')}")
    print(f"  Author: {metadata.get('author', 'Unknown')}")

    # Determine output directory
    if not slug:
        slug = create_slug(metadata.get('title'), metadata.get('author'), book_id)
    output_dir = Path(output_base) / slug
    print(f"\n  Output directory: {output_dir}")

    # Step 3: Download images
    print("\n[3/5] Processing images...")
    image_extractor = ImageExtractor(book_id, output_dir)

    if not skip_images:
        image_extractor.download_cover()

        if download_all_images:
            image_extractor.extract_images_from_html(html_content, html_url)
    else:
        print("  Skipping images (--skip-images flag)")

    images_result = image_extractor.get_results()

    # Step 4: Parse HTML and convert to markdown
    print("\n[4/5] Parsing content and converting to Markdown...")

    # Remove boilerplate using text markers (most reliable per extraction guide)
    clean_html = remove_gutenberg_boilerplate(html_content)
    print(f"  Removed boilerplate: {len(html_content)} -> {len(clean_html)} chars")

    parser = GutenbergHTMLParser()
    parser.feed(clean_html)
    front_matter, chapters, _ = parser.get_results()

    print(f"  Found {len(front_matter)} front matter sections")
    print(f"  Found {len(chapters)} chapters/parts")

    # Handle case with no chapters found
    if not chapters and not front_matter:
        print("  No chapters detected - extracting as single document...")
        whole_parser = WholeBookParser()
        whole_parser.feed(html_content)
        content = whole_parser.get_content()

        if content:
            chapters = [{
                'id': 'full-text',
                'title': metadata.get('title', 'Full Text'),
                'content': content,
                'type': 'chapter'
            }]
        else:
            print("ERROR: Could not extract any content")
            return False

    # Save markdown files
    saved_files = save_markdown_files(front_matter, chapters, output_dir, metadata)

    # Step 5: Create YAML data file
    print("\n[5/5] Creating 000-data.yml...")
    sections_info = {
        'front_matter_count': len(front_matter),
        'chapter_count': len(chapters),
        'total_sections': len(front_matter) + len(chapters),
        'files': saved_files
    }

    yaml_content = create_yaml_data(metadata, images_result, sections_info)
    yaml_path = output_dir / '000-data.yml'

    with open(yaml_path, 'w', encoding='utf-8') as f:
        f.write(yaml_content)
    print(f"  ✓ 000-data.yml")

    # Create README
    readme_content = f"# {metadata.get('title', 'Unknown')}\n\n"
    if metadata.get('author'):
        readme_content += f"*by {metadata['author']}*\n\n"
    readme_content += f"Extracted from [Project Gutenberg #{book_id}]({metadata['gutenberg_url']})\n\n"
    readme_content += f"## Contents\n\n"

    if front_matter:
        readme_content += "### Front Matter\n\n"
        for idx, section in enumerate(front_matter, 1):
            filename = f"00-{idx:02d}-{sanitize_filename(section['title'])}.md"
            readme_content += f"- [{section['title']}]({filename})\n"
        readme_content += "\n"

    readme_content += "### Chapters\n\n"
    for idx, chapter in enumerate(chapters, 1):
        filename = f"{idx:02d}-{sanitize_filename(chapter['title'])}.md"
        readme_content += f"- [{chapter['title']}]({filename})\n"

    readme_path = output_dir / 'README.md'
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print(f"  ✓ README.md")

    # Summary
    print("\n" + "=" * 60)
    print("✓ Extraction Complete!")
    print("=" * 60)
    print(f"  Output directory: {output_dir}")
    print(f"  Metadata file:    000-data.yml")
    print(f"  Front matter:     {len(front_matter)} sections")
    print(f"  Chapters:         {len(chapters)} sections")
    print(f"  Images:           {len(images_result.get('images', []))} downloaded")
    if images_result.get('cover'):
        print(f"  Cover image:      images/{images_result['cover']}")

    return True


def main():
    parser = argparse.ArgumentParser(
        description='Extract book data from Project Gutenberg',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s 64317                        # Extract The Great Gatsby
  %(prog)s 1342 --output ./essays       # Extract Pride and Prejudice to ./essays
  %(prog)s 84 --slug frankenstein       # Extract Frankenstein with custom folder name
  %(prog)s 11 --all-images              # Extract Alice's Adventures with all images
  %(prog)s 84 --local-html pg84.html    # Use locally downloaded HTML file

If downloads fail (403 errors), download HTML manually:
  wget -O book.html 'https://www.gutenberg.org/cache/epub/84/pg84-images.html'
  %(prog)s 84 --local-html book.html
        """
    )

    parser.add_argument('book_id', type=str,
                        help='Project Gutenberg book ID (e.g., 64317 for Great Gatsby)')
    parser.add_argument('--output', '-o', default='./books',
                        help='Output directory (default: ./books)')
    parser.add_argument('--slug', '-s',
                        help='Custom folder name (default: auto-generated from title/author)')
    parser.add_argument('--skip-images', action='store_true',
                        help='Skip downloading images')
    parser.add_argument('--all-images', action='store_true',
                        help='Download all inline images (not just cover)')
    parser.add_argument('--local-html', '-l', metavar='FILE',
                        help='Path to locally downloaded HTML file (skips download)')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Enable verbose output')

    args = parser.parse_args()

    success = extract_book(
        book_id=args.book_id,
        output_base=args.output,
        slug=args.slug,
        skip_images=args.skip_images,
        download_all_images=args.all_images,
        local_html=args.local_html
    )

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
