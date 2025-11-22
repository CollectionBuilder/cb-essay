#!/usr/bin/env python3
"""
Gutenberg Book to Markdown Chapters Converter
Downloads a Project Gutenberg book and splits it into individual markdown files per chapter.
"""

import re
import os
import sys
import argparse
from pathlib import Path
from urllib.request import urlopen
from urllib.error import URLError


HEADING_WORD_REGEX = re.compile(
    r'^(?P<label>chapter|letter|book|volume|part|section|prologue|epilogue|preface|introduction|etymology|extracts)\b(?P<rest>.*)$',
    re.IGNORECASE
)
ROMAN_NUMERAL_REGEX = re.compile(r'^(?P<roman>[IVXLCDM]{1,8})(?:[\.\)])?$', re.IGNORECASE)
HEADING_PRIORITY = {'word': 0, 'roman': 1}
LOWERCASE_REGEX = re.compile(r'[a-z]')
MIN_BODY_CHARS = 60
DENSE_GAP_THRESHOLD = 300
NUMBER_WORDS = {
    'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten',
    'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen',
    'eighteen', 'nineteen', 'twenty', 'thirty', 'forty', 'fifty', 'sixty',
    'seventy', 'eighty', 'ninety'
}
ORDINAL_WORDS = {
    'first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'eighth',
    'ninth', 'tenth', 'eleventh', 'twelfth', 'thirteenth', 'fourteenth',
    'fifteenth', 'sixteenth', 'seventeenth', 'eighteenth', 'nineteenth',
    'twentieth', 'thirtieth', 'fortieth', 'fiftieth', 'sixtieth',
    'seventieth', 'eightieth', 'ninetieth'
}
STANDALONE_HEADINGS = {'prologue', 'epilogue', 'preface', 'introduction', 'etymology'}
DESCRIPTIVE_STANDALONE_HEADINGS = {'extracts'}


def download_gutenberg_text(book_id):
    """Download plain text from Project Gutenberg."""
    # Try multiple URL patterns (Gutenberg has a few)
    urls = [
        f"https://www.gutenberg.org/files/{book_id}/{book_id}-0.txt",
        f"https://www.gutenberg.org/files/{book_id}/{book_id}.txt",
        f"https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.txt"
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
    
    raise Exception(f"Could not download book {book_id} from any URL")


def strip_gutenberg_boilerplate(text):
    """Remove Project Gutenberg header and footer boilerplate."""
    # Find start of actual content
    start_patterns = [
        r'\*\*\* START OF (THIS|THE) PROJECT GUTENBERG EBOOK.*?\*\*\*',
        r'START OF (THIS|THE) PROJECT GUTENBERG EBOOK'
    ]
    
    for pattern in start_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            text = text[match.end():]
            break
    
    # Find end of actual content
    end_patterns = [
        r'\*\*\* END OF (THIS|THE) PROJECT GUTENBERG EBOOK.*?\*\*\*',
        r'END OF (THIS|THE) PROJECT GUTENBERG EBOOK'
    ]
    
    for pattern in end_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            text = text[:match.start()]
            break
    
    return text.strip()


def extract_title_and_author(text):
    """Extract title and author from the beginning of the text."""
    lines = text.split('\n')[:50]  # Check first 50 lines
    
    title = None
    author = None
    
    # Common patterns for title/author
    for i, line in enumerate(lines):
        line = line.strip()
        if not title and len(line) > 0 and len(line) < 100:
            # Look for standalone text that might be a title
            if i > 0 and lines[i-1].strip() == '' and i < len(lines)-1 and lines[i+1].strip() == '':
                if not line.startswith('by') and 'chapter' not in line.lower():
                    title = line
        
        # Look for "by Author Name"
        if line.lower().startswith('by ') and len(line) > 3:
            author = line[3:].strip()
    
    return title, author


def _normalize_heading_text(text):
    return re.sub(r'\s+', ' ', text.strip())


def _extract_table_of_contents(text):
    """
    Extract table of contents entries from the beginning of the text.
    Returns:
    - List of normalized heading strings to look for
    - Position where the TOC section ends (after last TOC entry line)
    """
    toc_entries = []
    lines = text.split('\n')
    
    # Look for a section that looks like a table of contents
    in_toc = False
    toc_start_idx = 0
    toc_last_entry_idx = 0
    toc_type = None  # 'word' or 'roman'
    
    # First pass: find TOC section (look in first 500 lines max)
    for i in range(min(500, len(lines))):
        stripped = lines[i].strip()
        
        # Detect TOC start
        if stripped.upper() in ('CONTENTS', 'TABLE OF CONTENTS'):
            in_toc = True
            toc_start_idx = i
            continue
        
        # If we're in TOC, look for chapter/letter entries
        if in_toc:
            # Check if this looks like a heading entry
            word_match = HEADING_WORD_REGEX.match(stripped)
            if word_match:
                label = word_match.group('label')
                rest = word_match.group('rest').strip()
                # Normalize the entry
                if rest:
                    normalized = f"{label.capitalize()} {rest}".strip()
                else:
                    normalized = label.capitalize()
                normalized_entry = _normalize_heading_text(normalized)
                toc_entries.append(normalized_entry)
                toc_last_entry_idx = i
                toc_type = 'word'
            elif ROMAN_NUMERAL_REGEX.match(stripped):
                # Roman numeral TOC entry - keep as-is
                numeral = stripped.upper().rstrip('.)')
                toc_entries.append(numeral)
                toc_last_entry_idx = i
                toc_type = 'roman'
            elif stripped and stripped not in ('Epilogue', 'EPILOGUE'):
                # Keep scanning - TOC might be long
                continue
            
            # Check if we hit the end marker
            if stripped in ('Epilogue', 'EPILOGUE', 'CONCLUSION'):
                break
    
    if toc_entries and len(toc_entries) >= 3:  # Require at least 3 TOC entries
        # Calculate position after the last TOC entry line
        # We use toc_last_entry_idx (not +1) to get position just after that line's content
        toc_section_end_pos = sum(len(lines[j]) + 1 for j in range(toc_last_entry_idx)) + len(lines[toc_last_entry_idx].rstrip())
        
        print(f"  Found {len(toc_entries)} entries in table of contents ({toc_type} format)")
        print(f"  TOC last entry at line {toc_last_entry_idx}, ends at position {toc_section_end_pos}, first entry: {toc_entries[0]}")
        return toc_entries, toc_section_end_pos
    
    return [], 0


def _looks_like_heading_number(token):
    cleaned = token.strip().lower().strip('.)')
    if not cleaned:
        return False
    cleaned = cleaned.replace('—', '-').replace('–', '-').strip('-')
    if not cleaned:
        return False
    if cleaned.isdigit():
        return True
    roman_candidate = cleaned.upper()
    if ROMAN_NUMERAL_REGEX.fullmatch(roman_candidate):
        return True
    cleaned_parts = cleaned.replace('-', ' ').split()
    if not cleaned_parts:
        return False
    return all(part in NUMBER_WORDS or part in ORDINAL_WORDS for part in cleaned_parts)


def _classify_heading_line(line):
    stripped = line.strip()
    if not stripped:
        return None, None, None
    word_match = HEADING_WORD_REGEX.match(stripped)
    if word_match:
        label_raw = word_match.group('label')
        label_lower = label_raw.lower()
        rest = word_match.group('rest').strip()
        if label_lower in STANDALONE_HEADINGS:
            if rest.strip(' .:-—–'):
                return None, None, None
            return 'word', label_lower.capitalize(), label_lower
        if label_lower in DESCRIPTIVE_STANDALONE_HEADINGS:
            title = f"{label_raw.capitalize()}{rest}".strip()
            return 'word', _normalize_heading_text(title), label_lower
        if not rest:
            return None, None, None
        first_token = rest.split()[0]
        if not _looks_like_heading_number(first_token):
            return None, None, None
        title = f"{label_raw.capitalize()} {rest}".strip()
        return 'word', _normalize_heading_text(title), label_lower
    roman_match = ROMAN_NUMERAL_REGEX.match(stripped)
    if roman_match:
        numeral = roman_match.group('roman').upper().rstrip('.)')
        # Keep Roman numerals as-is (for books like Gatsby)
        return 'roman', numeral, 'roman'
    return None, None, None


def _gather_heading_candidates(text, toc_entries=None):
    """
    Gather heading candidates from text.
    If toc_entries is provided, only include headings that match TOC entries.
    """
    candidates_by_start = {}
    position = 0
    
    for line in text.splitlines(keepends=True):
        heading_type, title, label = _classify_heading_line(line)
        if heading_type and title:
            # If we have a TOC, only accept headings that match TOC entries
            if toc_entries:
                if title not in toc_entries:
                    position += len(line)
                    continue
            
            start_idx = position
            end_idx = position + len(line)
            existing = candidates_by_start.get(start_idx)
            if existing:
                if HEADING_PRIORITY[heading_type] < HEADING_PRIORITY[existing['type']]:
                    candidates_by_start[start_idx] = {
                        'start': start_idx,
                        'end': end_idx,
                        'title': title,
                        'heading': line.strip(),
                        'type': heading_type,
                        'label': label
                    }
            else:
                candidates_by_start[start_idx] = {
                    'start': start_idx,
                    'end': end_idx,
                    'title': title,
                    'heading': line.strip(),
                    'type': heading_type,
                    'label': label
                }
        position += len(line)
    return sorted(candidates_by_start.values(), key=lambda c: c['start'])


def _find_dense_heading_positions(candidates):
    dense_positions = set()
    grouped = {}
    for cand in candidates:
        label = cand.get('label')
        if cand['type'] == 'word' and label in (STANDALONE_HEADINGS | DESCRIPTIVE_STANDALONE_HEADINGS):
            continue
        grouped.setdefault(cand['type'], []).append(cand['start'])
    for heading_type, starts in grouped.items():
        if heading_type not in ('roman', 'word'):
            continue
        starts.sort()
        for idx, pos in enumerate(starts):
            prev_pos = starts[idx - 1] if idx > 0 else None
            next_pos = starts[idx + 1] if idx < len(starts) - 1 else None
            if (prev_pos is not None and pos - prev_pos < DENSE_GAP_THRESHOLD) or \
               (next_pos is not None and next_pos - pos < DENSE_GAP_THRESHOLD):
                dense_positions.add(pos)
    return dense_positions


def _filter_heading_candidates(candidates, text, toc_entries=None, toc_section_end_pos=0):
    """
    Filter heading candidates to remove false positives.
    When we have TOC entries, we find where the first TOC entry actually appears as a heading
    and use everything before that as preamble.
    """
    if not candidates:
        return []
    
    # If we have TOC entries, find where the first one appears as an actual heading
    # (searching AFTER the TOC section ends)
    first_chapter_pos = None
    if toc_entries and toc_section_end_pos > 0:
        # Find the EARLIEST candidate that appears after the TOC section
        # and matches ANY TOC entry
        candidates_after_toc = []
        for cand in candidates:
            # Skip candidates that appear before or within the TOC section  
            if cand['start'] < toc_section_end_pos:
                continue
            # Only keep candidates that match a TOC entry    
            if cand['title'] in toc_entries:
                candidates_after_toc.append(cand)
        
        # Show what we found
        print(f"  Candidates after TOC: {[c['title'] for c in candidates_after_toc[:10]]}")
        
        # The first chapter is simply the earliest one
        if candidates_after_toc:
            first_chapter = min(candidates_after_toc, key=lambda c: c['start'])
            first_chapter_pos = first_chapter['start']
            first_chapter_title = first_chapter['title']
            print(f"  First chapter '{first_chapter_title}' found at position {first_chapter_pos}")
            # Filter: keep only candidates at or after the first chapter position
            candidates = [c for c in candidates if c['start'] >= first_chapter_pos]
            if not candidates:
                return [], None
    else:
        # No TOC - use dense heading detection
        dense_positions = _find_dense_heading_positions(candidates)
        candidates = [c for idx, c in enumerate(candidates) 
                     if idx == 0 or c['start'] not in dense_positions]
    
    filtered = []
    total_length = len(text)
    
    for idx, cand in enumerate(candidates):
        next_start = candidates[idx + 1]['start'] if idx < len(candidates) - 1 else total_length
        body = text[cand['end']:next_start]
        body_stripped = body.strip()
        if not body_stripped:
            continue
        if not LOWERCASE_REGEX.search(body_stripped):
            continue
        body_compact = re.sub(r'\s+', '', body_stripped)
        if len(body_compact) < MIN_BODY_CHARS:
            continue
        
        # Additional validation: check if content looks like actual chapter prose
        # Skip if it looks like a dedication or epigraph (very short with lots of whitespace)
        lines_in_body = body_stripped.split('\n')
        non_empty_lines = [l for l in lines_in_body if l.strip()]
        
        # For first chapter only, require at least 3 non-empty lines to avoid preamble
        # (reduced from 5 to handle letters/short openings)
        if idx == 0 and len(non_empty_lines) < 3:
            continue
        
        # Check for prose-like content - should have sentences with periods
        # Look deeper into content (up to 30 lines instead of 15)
        has_prose = any('. ' in line or '."' in line or '." ' in line for line in non_empty_lines[:30])
        if idx == 0 and not has_prose:
            # For first chapter only, require prose markers
            continue
        
        filtered.append({**cand, 'body_start': cand['end'], 'body_end': next_start})
    
    # Return filtered candidates and the first chapter position if we found it earlier
    return filtered, first_chapter_pos


def split_into_chapters(text, book_title="Book"):
    """Split text into chapters, detecting various chapter heading patterns."""

    # First, try to extract table of contents
    toc_entries, toc_section_end_pos = _extract_table_of_contents(text)
    
    # Gather heading candidates, filtering by TOC if available
    if toc_entries:
        print(f"  Using table of contents to identify chapters")
        raw_candidates = _gather_heading_candidates(text, toc_entries=toc_entries)
        filtered_result = _filter_heading_candidates(raw_candidates, text, toc_entries=toc_entries, toc_section_end_pos=toc_section_end_pos)
        
        # Check if we got back both candidates and first chapter position
        if isinstance(filtered_result, tuple):
            filtered_candidates, first_chapter_pos = filtered_result
        else:
            filtered_candidates = filtered_result
            first_chapter_pos = None
    else:
        print(f"  No table of contents found, using pattern detection")
        raw_candidates = _gather_heading_candidates(text)
        filtered_result = _filter_heading_candidates(raw_candidates, text)
        if isinstance(filtered_result, tuple):
            filtered_candidates, first_chapter_pos = filtered_result
        else:
            filtered_candidates = filtered_result
            first_chapter_pos = None
    
    if not filtered_candidates:
        print("Warning: No chapter markers found. Saving as single file.")
        return [{'number': '1', 'title': book_title, 'content': text.strip(), 'order': 1}]

    print(f"  Detected {len(raw_candidates)} heading candidates, using {len(filtered_candidates)} after filtering")

    chapters = []
    
    # Check for preamble content between TOC and first chapter
    preamble_added = False
    if toc_section_end_pos > 0 and first_chapter_pos and filtered_candidates:
        # Preamble is everything between end of TOC and start of first detected chapter
        preamble_content = text[toc_section_end_pos:first_chapter_pos].strip()
        
        # Check if there are any TOC entry headings within the preamble content
        # (This handles cases like Gatsby where Chapter I isn't detected by our filters)
        preamble_has_chapter = False
        if toc_entries and preamble_content:
            # Search for headings that match TOC entries within the preamble
            for entry in toc_entries[:5]:  # Check first few TOC entries
                # Build a simple regex to find the heading
                # For Roman numerals, look for them centered on their own line
                if entry in ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X']:
                    pattern = rf'^\s*{re.escape(entry)}\s*$'
                else:
                    pattern = rf'^\s*{re.escape(entry)}\s*$'
                
                if re.search(pattern, preamble_content, re.MULTILINE):
                    # Found a chapter heading in the preamble - this means the preamble
                    # actually contains chapter content
                    preamble_has_chapter = True
                    print(f"  Warning: Found chapter heading '{entry}' in preamble area")
                    break
        
        # Only include as preamble if it has substantial content AND no chapter headings
        if preamble_content and len(preamble_content) > 100 and not preamble_has_chapter:
            # Clean up the preamble - remove extra whitespace and blank lines at start/end
            preamble_lines = preamble_content.split('\n')
            # Remove leading/trailing empty lines
            while preamble_lines and not preamble_lines[0].strip():
                preamble_lines.pop(0)
            while preamble_lines and not preamble_lines[-1].strip():
                preamble_lines.pop()
            
            if preamble_lines:
                preamble_content = '\n'.join(preamble_lines)
                chapters.append({
                    'number': '00',
                    'title': 'Preamble',
                    'content': preamble_content,
                    'order': 0
                })
                preamble_added = True
                print(f"  Found preamble content ({len(preamble_content)} characters)")
        elif preamble_has_chapter:
            print(f"  Skipping preamble extraction - contains chapter content")
    
    for idx, candidate in enumerate(filtered_candidates):
        content = text[candidate['body_start']:candidate['body_end']].strip()
        if not content:
            continue
        chapters.append({
            'number': f"{len(chapters)+1:02d}",
            'title': candidate['title'],
            'content': content,
            'order': len(chapters) + 1
        })

    if not chapters:
        print("Warning: Could not build chapters from detected headings. Saving as single file.")
        return [{'number': '1', 'title': book_title, 'content': text.strip(), 'order': 1}]

    return chapters


def convert_to_markdown(chapter_info, book_title=None, book_author=None):
    """Convert chapter text to markdown format with CB-Essay front matter."""
    title = chapter_info['title']
    content = chapter_info['content']
    order = chapter_info['order']
    
    # Remove the chapter heading from content since we'll add it as markdown header
    lines = content.split('\n')
    if lines and (lines[0].strip().startswith('Chapter') or 
                  lines[0].strip().startswith('CHAPTER') or
                  lines[0].strip().startswith('Letter') or
                  lines[0].strip().startswith('LETTER')):
        lines = lines[1:]
    
    content = '\n'.join(lines).strip()
    
    # Create front matter for CB-Essay
    front_matter = "---\n"
    front_matter += f"title: {title}\n"
    if book_author:
        front_matter += f"byline: {book_author}\n"
    front_matter += f"order: {order}\n"
    front_matter += "---\n\n"
    
    # Create markdown with front matter
    markdown = front_matter + content
    
    return markdown


def save_chapters(chapters, output_dir, book_slug, book_title=None, book_author=None):
    """Save chapters as markdown files."""
    output_path = Path(output_dir) / book_slug
    output_path.mkdir(parents=True, exist_ok=True)
    
    print(f"\nSaving {len(chapters)} chapters to {output_path}/")
    
    for chapter in chapters:
        filename = f"{chapter['number']}-{sanitize_filename(chapter['title'])}.md"
        filepath = output_path / filename
        
        markdown_content = convert_to_markdown(chapter, book_title, book_author)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"  ✓ {filename}")
    
    return output_path


def sanitize_filename(text):
    """Convert text to safe filename."""
    # Remove/replace unsafe characters
    text = re.sub(r'[<>:"/\\|?*]', '', text)
    text = re.sub(r'\s+', '-', text)
    text = text.lower().strip('-')
    return text[:50]  # Limit length


def create_index(chapters, output_dir, book_slug, book_title, book_author):
    """Create an index.md file with links to all chapters."""
    output_path = Path(output_dir) / book_slug
    index_path = output_path / 'README.md'
    
    content = f"# {book_title}\n\n"
    if book_author:
        content += f"*by {book_author}*\n\n"
    
    content += "## Chapters\n\n"
    
    for chapter in chapters:
        filename = f"{chapter['number']}-{sanitize_filename(chapter['title'])}.md"
        content += f"- [{chapter['title']}]({filename})\n"
    
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  ✓ README.md (index)")


def main():
    parser = argparse.ArgumentParser(
        description='Download and split a Project Gutenberg book into markdown chapters for CB-Essay.'
    )
    parser.add_argument('book_id', type=str, 
                       help='Project Gutenberg book ID (e.g., 84) or path to local .txt file')
    parser.add_argument('--output', '-o', default='./books', 
                       help='Output directory (default: ./books)')
    parser.add_argument('--slug', '-s', 
                       help='Custom folder name (default: book-{id} or filename)')
    
    args = parser.parse_args()
    
    book_id = args.book_id
    output_dir = args.output
    
    print("="*60)
    
    # Check if book_id is a file path or a book ID
    if os.path.exists(book_id):
        print(f"Reading from local file: {book_id}")
        book_slug = args.slug or Path(book_id).stem
        try:
            with open(book_id, 'r', encoding='utf-8') as f:
                text = f.read()
        except Exception as e:
            print(f"Error reading file: {e}")
            sys.exit(1)
    else:
        print(f"Processing Gutenberg book ID: {book_id}")
        book_slug = args.slug or f"book-{book_id}"
        # Download the book
        try:
            text = download_gutenberg_text(book_id)
        except Exception as e:
            print(f"Error: {e}")
            print("\nTip: You can also provide a local .txt file path instead of a book ID")
            sys.exit(1)
    
    # Strip boilerplate
    print("\nRemoving Gutenberg boilerplate...")
    text = strip_gutenberg_boilerplate(text)
    
    # Extract metadata
    print("Extracting title and author...")
    title, author = extract_title_and_author(text)
    if title:
        print(f"  Title: {title}")
    if author:
        print(f"  Author: {author}")
    
    # Split into chapters
    print("\nSplitting into chapters...")
    chapters = split_into_chapters(text, title or "Book")
    print(f"  Found {len(chapters)} chapters")
    
    # Save chapters
    output_path = save_chapters(chapters, output_dir, book_slug, title, author)
    
    # Create index
    create_index(chapters, output_dir, book_slug, title or book_slug, author)
    
    print("\n" + "="*60)
    print(f"✓ Complete! Files saved to: {output_path}")
    print(f"  Total chapters: {len(chapters)}")


if __name__ == '__main__':
    main()
