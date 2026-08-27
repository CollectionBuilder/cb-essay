#!/usr/bin/env python3
"""
Gutenberg Extraction Script

Extracts a Project Gutenberg book into a CollectionBuilder-Essay project:
- Chapter markdown files → _essay/
- Book metadata          → _data/book.yml
- Cover (and optionally all inline) images → objects/

Usage:
    python3 gutenberg-extraction.py <book_id> [options]

Arguments:
    book_id                 Project Gutenberg book ID (e.g., 84 for Frankenstein)

Options:
     --clear                 Clear existing markdown files from the essay output dir before writing
    --about-page            Generate pages/about.md with a catalog card and placeholder sections
    --project-root DIR      CB-Essay project root; writes to {root}/_essay/ and {root}/_data/book.yml (default: current directory)
    --output, -o DIR        Write essay markdown files here instead of {project-root}/_essay/
    --slug, -s NAME         Custom book slug for book.yml (default: auto-generated)
    --skip-images           Skip downloading images to objects/
    --all-images            Download all inline images in addition to the cover
    --illustrations MODE    How to handle the book's illustrations:
                              none     - ignore them (default)
                              link     - place image-gallery includes pointing at
                                         Gutenberg's own image URLs (nothing downloaded)
                              download - fetch into objects/, register as collection
                                         items in _data/<slug>-metadata.csv, and point
                                         _config.yml at that CSV
    --collection-images     Alias for --illustrations download
    --local-html, -l FILE   Use a locally downloaded HTML file instead of fetching from Gutenberg
    --verbose, -v           Enable verbose output

Examples:
    python3 gutenberg-extraction.py 64317
    python3 gutenberg-extraction.py 84 --clear
    python3 gutenberg-extraction.py 84 --about-page
    python3 gutenberg-extraction.py 84 --project-root ~/my-site
    python3 gutenberg-extraction.py 84 --output ./staging
    python3 gutenberg-extraction.py 11 --all-images
    python3 gutenberg-extraction.py 25290 --illustrations link
    python3 gutenberg-extraction.py 25290 --illustrations download
    python3 gutenberg-extraction.py 84 --local-html pg84.html

If downloads fail (403 errors), download the HTML manually first:
    wget -O book.html 'https://www.gutenberg.org/cache/epub/84/pg84-images.html'
    python3 gutenberg-extraction.py 84 --local-html book.html
"""

import re
import os
import sys
import csv
import json
import gzip
import zlib
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


_verbose = False


def vprint(*args, **kwargs):
    if _verbose:
        print(*args, **kwargs)


# =============================================================================
# Configuration
# =============================================================================

# Gutenberg URL patterns
GUTENBERG_URLS = {
    'html_images': 'https://www.gutenberg.org/cache/epub/{id}/pg{id}-images.html',
    'html_simple': 'https://www.gutenberg.org/files/{id}/{id}-h/{id}-h.htm',
    'html_alt': 'https://www.gutenberg.org/files/{id}/{id}-h.htm',
    'cover_hires_jpg': 'https://www.gutenberg.org/cache/epub/{id}/images/cover.jpg',
    'cover_hires_png': 'https://www.gutenberg.org/cache/epub/{id}/images/cover.png',
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
    r'^[ivxlcdm]+\.\s+\w+',      # I. Title, II. Title (roman numeral + period + space + word)
    r'^[ivxlcdm]+\.$',           # I., II., III. (roman numerals with period only)
    r'^\d+\.\s+\w+',             # 1. Title, 2. Title (number + period + space + word)
    r'^\d+\.$',                   # 1., 2., 3. (numbers with period only)
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
    'list of illustrations', 'list of plates', 'list of figures',
    'illustrations', 'plates',
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


def find_toc_region(html_text: str) -> Tuple[Optional[str], str]:
    """Return the HTML of the table of contents, or None if there isn't one.

    Precision matters: a region that overshoots picks up page-number and
    illustration links from the body, which then get mistaken for chapters.

    Returns (region, method) where method is 'container', 'heading' or 'none' —
    the extraction report leans on it, since a book with no TOC is a book whose
    chapter splitting deserves a second look.
    """
    def has_links(region: str) -> bool:
        # A "Contents" label with no links (e.g. <p class="toc">CONTENTS</p>) is
        # a heading for the TOC, not the TOC itself — keep looking.
        return len(re.findall(r'href=["\']#', region)) >= 2

    # 1) An explicit toc/contents container. Gutenberg uses div/nav/section but
    #    also p/ul/ol/table (e.g. <p class="toc"> in many illustrated editions).
    for match in re.finditer(
            r'<(div|nav|section|p|ul|ol|table)\b[^>]*(?:class|id)=["\']'
            r'[^"\']*(?:toc|contents)[^"\']*["\'][^>]*>(?:.*?)</\1>',
            html_text, re.IGNORECASE | re.DOTALL):
        if has_links(match.group(0)):
            return match.group(0), 'container'

    # 2) Otherwise the block following a heading that is itself "Contents".
    #    Match the heading's own text only — an unbounded .*? would run past it.
    for match in re.finditer(r'<h([1-4])\b[^>]*>(.*?)</h\1>', html_text,
                             re.IGNORECASE | re.DOTALL):
        text = re.sub(r'<[^>]+>', ' ', match.group(2))
        text = ' '.join(text.split()).lower()
        if 'content' not in text or 'gutenberg' in text:
            continue
        rest = html_text[match.end():]
        next_heading = re.search(r'<h[1-4]\b', rest, re.IGNORECASE)
        region = rest[:next_heading.start()] if next_heading else rest
        if has_links(region):
            return region, 'heading'

    return None, 'none'


def extract_toc_anchors(html_text: str) -> List[str]:
    """Extract anchor IDs from table of contents links.

    This is the most reliable way to find chapter boundaries per the extraction guide.
    TOC links like <a href="#chapter-1"> tell us exactly where sections are.
    """
    anchors = []

    toc_html, _method = find_toc_region(html_text)
    whole_document = toc_html is None
    if whole_document:
        # No TOC to go on — scan everything, but hold links to a stricter standard
        toc_html = html_text

    # Extract all internal anchors (href="#...")
    anchor_pattern = r'<a[^>]+href=["\']#([^"\']+)["\'][^>]*>'
    matches = re.findall(anchor_pattern, toc_html, re.IGNORECASE)

    # Page anchors are chapter starts only when a real TOC points at them
    page_anchor = re.compile(r'^(?:page|pg)[-_]?[\divxlcdm]+$', re.IGNORECASE)

    for anchor in matches:
        anchor_lower = anchor.lower()
        # Skip non-chapter anchors
        if any(skip in anchor_lower for skip in ['note', 'footnote', 'pg-', 'gutenberg']):
            continue
        if FIGURE_ANCHOR_RE.match(anchor):
            continue
        if whole_document and page_anchor.match(anchor):
            continue
        if anchor not in anchors:
            anchors.append(anchor)

    return anchors



def extract_toc_part_map(html_text: str) -> Dict[str, str]:
    """Map chapter anchor IDs to their part label using Gutenberg's large-bold TOC style.

    Detects the specific pattern:
      <a href="#partNN" class="pginternal">
        <span style="font-size: large;"><b>— I —</b></span>
      </a>

    Returns {} if the pattern isn't present (graceful no-op for most books).
    """
    link_re = re.compile(
        r'<a\b[^>]*\bhref="#([^"]+)"[^>]*class="pginternal"[^>]*>(.*?)</a>',
        re.IGNORECASE | re.DOTALL,
    )
    link_re2 = re.compile(
        r'<a\b[^>]*class="pginternal"[^>]*\bhref="#([^"]+)"[^>]*>(.*?)</a>',
        re.IGNORECASE | re.DOTALL,
    )
    part_id_re = re.compile(r'^part\d+$', re.IGNORECASE)

    matches = []
    seen = set()
    for m in link_re.finditer(html_text):
        key = (m.start(), m.group(1))
        if key not in seen:
            seen.add(key)
            matches.append((m.start(), m.group(1), m.group(2)))
    for m in link_re2.finditer(html_text):
        key = (m.start(), m.group(1))
        if key not in seen:
            seen.add(key)
            matches.append((m.start(), m.group(1), m.group(2)))
    matches.sort(key=lambda x: x[0])

    if not matches:
        return {}

    sequence = []
    for _, anchor_id, content in matches:
        if part_id_re.match(anchor_id):
            # Extract label from link text: strip HTML, strip em-dashes/whitespace
            label = re.sub(r'<[^>]+>', '', content)
            label = re.sub(r'[—–\-\s]+', ' ', label).strip()
            roman_match = re.search(r'\b([IVXLCDM]+)\b', label, re.IGNORECASE)
            label = roman_match.group(1).upper() if roman_match else label
            sequence.append((anchor_id, label or anchor_id))
        else:
            sequence.append((anchor_id, None))

    if not any(part for _, part in sequence):
        return {}

    part_map = {}
    current_part = None
    for anchor_id, part_label in sequence:
        if part_label is not None:
            current_part = part_label
            part_map[anchor_id] = current_part  # part divider gets its own label
        elif current_part is not None:
            part_map[anchor_id] = current_part

    return part_map


def is_section_id(element_id: str, toc_anchors: List[str] = None) -> Tuple[bool, str]:
    """Check if an element ID marks a section boundary.

    Args:
        element_id: The ID attribute of an element
        toc_anchors: List of anchor IDs from the TOC (if available)

    Returns (is_section, section_type) tuple.
    """
    id_lower = element_id.lower()

    # Skip Gutenberg boilerplate IDs
    if any(skip in id_lower for skip in ['gutenberg', 'license', 'pg-', 'boilerplate']):
        return False, ''

    # If this ID is in the TOC anchors, it's definitely a section
    if toc_anchors and element_id in toc_anchors:
        # Determine type from ID
        if any(kw in id_lower for kw in ['preface', 'introduction', 'foreword', 'prologue',
                                         'dedication', 'illustration', 'plates']):
            return True, 'front_matter'
        if any(kw in id_lower for kw in ['epilogue', 'afterword', 'appendix', 'notes', 'index', 'glossary']):
            return True, 'back_matter'
        if 'content' in id_lower or 'toc' in id_lower:
            return True, 'toc'
        return True, 'chapter'

    # Check ID patterns that indicate chapters
    chapter_id_patterns = [
        r'^chapter[-_]?[ivxlcdm\d]+',
        r'^chap[-_]?[ivxlcdm\d]+',
        r'^ch[-_]?[ivxlcdm\d]+',
        r'^letter[-_]?[ivxlcdm\d]+',
        r'^book[-_]?[ivxlcdm\d]+',
        r'^part[-_]?[ivxlcdm\d]+',
        r'^volume[-_]?[ivxlcdm\d]+',
        r'^[ivxlcdm]+$',  # Pure roman numerals
        r'^\d+$',  # Pure numbers
    ]

    for pattern in chapter_id_patterns:
        if re.match(pattern, id_lower):
            return True, 'chapter'

    # Check for front/back matter IDs
    if any(kw in id_lower for kw in ['preface', 'introduction', 'foreword', 'prologue',
                                     'dedication', 'illustration', 'plates']):
        return True, 'front_matter'
    if any(kw in id_lower for kw in ['epilogue', 'afterword', 'appendix', 'index', 'glossary', 'bibliography']):
        return True, 'back_matter'
    if 'content' in id_lower or 'toc' in id_lower:
        return True, 'toc'

    return False, ''


# =============================================================================
# Utility Functions
# =============================================================================

def read_response(response, binary: bool = False) -> bytes | str:
    """Read a urllib response, decompressing per Content-Encoding.

    HEADERS advertises gzip/deflate, and Gutenberg honors it. urllib does NOT
    decompress automatically, so the raw body must be inflated here — otherwise
    the "HTML" is binary garbage and the parsers silently find zero content.
    """
    data = response.read()
    encoding = (response.headers.get('Content-Encoding') or '').lower()

    if 'gzip' in encoding:
        data = gzip.decompress(data)
    elif 'deflate' in encoding:
        try:
            data = zlib.decompress(data)
        except zlib.error:
            data = zlib.decompress(data, -zlib.MAX_WBITS)  # raw deflate

    if binary:
        return data

    charset = response.headers.get_content_charset() or 'utf-8'
    return data.decode(charset, errors='replace')


def make_request(url: str, binary: bool = False, timeout: int = 30,
                 max_retries: int = MAX_RETRIES, use_fallbacks: bool = True) -> Optional[bytes | str]:
    """Make an HTTP request with retries and error handling.

    The defaults suit the one fetch the whole run depends on — the book HTML.
    Bulk fetches (images) should pass a lighter policy: when Gutenberg throttles,
    the full retry-plus-wget-plus-curl chain costs ~25s per miss.
    """
    import subprocess
    import shutil

    # First try with urllib
    for attempt in range(max_retries):
        try:
            request = Request(url, headers=HEADERS)
            with urlopen(request, timeout=timeout) as response:
                return read_response(response, binary)
        except HTTPError as e:
            if e.code == 404:
                # Try wget/curl as fallback before giving up on 404
                break
            if attempt == max_retries - 1:
                break
        except URLError as e:
            if attempt == max_retries - 1:
                break
        except Exception as e:
            if attempt == max_retries - 1:
                break

        time.sleep(RETRY_DELAY * (attempt + 1))

    if not use_fallbacks:
        return None

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
                ['curl', '-sfL', '--max-time', str(timeout), url],
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

    # Remove problematic filename characters. The slug built from this ends up
    # as a CSV filename referenced from _config.yml, so keep it to word
    # characters and hyphens.
    text = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '', text)
    text = re.sub(r'[^\w\s-]', ' ', text, flags=re.UNICODE)  # a space, so 'I. Down' keeps its break
    text = re.sub(r'\s+', '-', text)
    text = re.sub(r'-{2,}', '-', text)
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

# Figure/plate anchors like #f016 or #f005a point at illustrations, not sections
FIGURE_ANCHOR_RE = re.compile(r'^(?:f|fig|img|illus|plate)[-_]?\d+[a-z]?$', re.IGNORECASE)
IMAGE_EXT_RE = re.compile(r'\.(?:jpe?g|png|gif|webp|svg)$', re.IGNORECASE)


class FigureParser(HTMLParser):
    """Collect every <img> with the context that makes it a catalogable figure.

    Gutenberg wraps illustrations in a recognizable pattern:

        <a id="f002"></a>                         <- stable anchor, cited by the
        <a href="images/image002h.png">              list of illustrations
          <img alt="The Origin of Outline."       <- caption and alt text
               src="images/image002.png">         <- hi-res variant in the href
        </a>

    Attributes are read through HTMLParser rather than a regex so alt text
    survives regardless of attribute order.
    """

    def __init__(self):
        super().__init__()
        self.figures = []
        self.pending_anchor = None
        self.link_href = None
        self.caption_parts = []
        self.in_caption = False
        self.pending_caption = ''

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)

        if 'caption' in (attrs_dict.get('class') or '').lower():
            self.in_caption = True
            self.caption_parts = []
            return

        if tag == 'a':
            if 'id' in attrs_dict and 'href' not in attrs_dict:
                self.pending_anchor = attrs_dict['id']
            if 'href' in attrs_dict:
                self.link_href = attrs_dict['href']
            return

        if tag == 'img':
            src = attrs_dict.get('src', '')
            if not src or src.startswith('data:'):
                return

            hires = self.link_href if self.link_href and IMAGE_EXT_RE.search(self.link_href) else None
            anchor = self.pending_anchor if self.pending_anchor and FIGURE_ANCHOR_RE.match(self.pending_anchor) else None

            self.figures.append({
                'src': src,
                'alt': html.unescape(attrs_dict.get('alt', '') or '').strip(),
                'title': html.unescape(attrs_dict.get('title', '') or '').strip(),
                'anchor': anchor,
                'hires': hires,
                'caption': self.pending_caption,
            })
            self.pending_anchor = None
            self.pending_caption = ''

    def handle_endtag(self, tag):
        if self.in_caption and tag in ('span', 'p', 'div'):
            self.in_caption = False
            caption = ' '.join(''.join(self.caption_parts).split())
            self.caption_parts = []
            if caption:
                # Captions sit either side of the image they belong to
                if self.figures and not self.figures[-1]['caption']:
                    self.figures[-1]['caption'] = caption
                else:
                    self.pending_caption = caption
            return

        if tag == 'a':
            self.link_href = None

    def handle_data(self, data):
        if self.in_caption and data:
            self.caption_parts.append(data)


def extract_figure_captions(html_text: str) -> Dict[str, str]:
    """Map figure anchors to captions using the book's list of illustrations.

    Rows look like: <td>The Origin of Outline</td><td><a href="#f002">f002</a></td>
    """
    captions = {}

    for row in re.findall(r'<tr\b.*?</tr>', html_text, re.IGNORECASE | re.DOTALL):
        link = re.search(r'href=["\']#([^"\']+)["\']', row, re.IGNORECASE)
        if not link or not FIGURE_ANCHOR_RE.match(link.group(1)):
            continue

        cells = re.findall(r'<t[dh]\b[^>]*>(.*?)</t[dh]>', row, re.IGNORECASE | re.DOTALL)
        parts = []
        for cell in cells:
            if 'href' in cell.lower():  # the cell holding the figure reference itself
                continue
            text = ' '.join(re.sub(r'<[^>]+>', ' ', cell).split())
            if text:
                parts.append(html.unescape(text))

        caption = ' '.join(parts).strip()
        if caption:
            captions.setdefault(link.group(1), caption)

    return captions


def is_decorative(figure: Dict) -> bool:
    """Drop caps and rules are page furniture, not figures worth cataloging."""
    if figure.get('anchor') or figure.get('caption'):
        return False
    alt = figure.get('alt', '')
    # alt="M" is an illuminated initial; alt="" is an uncaptioned plate, which
    # is still worth keeping
    return 0 < len(alt) <= 2


def gutenberg_image_urls(book_id: str, src: str, base_url: str) -> List[str]:
    """Candidate URLs for an image, most likely first.

    A relative src is resolved against Gutenberg rather than the page it came
    from, so --local-html extractions can still fetch images.
    """
    if src.startswith('http'):
        return [src]

    candidates = [
        urljoin(f'https://www.gutenberg.org/cache/epub/{book_id}/', src),
        urljoin(f'https://www.gutenberg.org/files/{book_id}/{book_id}-h/', src),
    ]
    if base_url and base_url.startswith('http'):
        resolved = urljoin(base_url, src)
        if resolved not in candidates:
            candidates.insert(0, resolved)
    return candidates


def build_figures(book_id: str, html_content: str, base_url: str,
                  stats: Dict = None) -> List[Dict]:
    """Parse the book into a list of catalogable figures.

    Pass a dict as `stats` to receive counts of what was seen and filtered.
    """
    parser = FigureParser()
    parser.feed(html_content)

    captions = extract_figure_captions(html_content)

    figures = []
    seen = set()
    counts = {'seen': len(parser.figures), 'duplicate': 0, 'decorative': 0}
    for index, figure in enumerate(parser.figures, 1):
        if figure['src'] in seen:
            counts['duplicate'] += 1
            continue
        seen.add(figure['src'])

        if figure['anchor'] and not figure['caption']:
            figure['caption'] = captions.get(figure['anchor'], '')
        if is_decorative(figure):
            counts['decorative'] += 1
            continue

        anchor = figure['anchor'] or f'img{index:03d}'
        figure['objectid'] = f'{book_id}_{anchor.lower()}'
        figure['urls'] = gutenberg_image_urls(book_id, figure['src'], base_url)
        figure['extension'] = (Path(urlparse(figure['src']).path).suffix or '.jpg').lower()
        figure['original_name'] = Path(urlparse(figure['src']).path).name
        figure['title'] = (figure['caption'] or figure['alt'] or figure['title']
                           or f'Figure {index}').rstrip('.')
        figures.append(figure)

    counts['kept'] = len(figures)
    if stats is not None:
        stats.update(counts)

    return figures


def extract_image_urls(book_id: str, html_content: str, base_url: str) -> Dict:
    """Extract image URLs without downloading them.

    Returns a dict with cover URLs and inline image URLs.
    """
    result = {
        'cover_urls': [
            GUTENBERG_URLS['cover_hires_jpg'].format(id=book_id),
            GUTENBERG_URLS['cover_hires_png'].format(id=book_id),
            GUTENBERG_URLS['cover_medium'].format(id=book_id),
            GUTENBERG_URLS['cover_small'].format(id=book_id),
        ],
        'inline_images': []
    }

    # Find all image tags in HTML
    img_pattern = r'<img[^>]+src=["\']([^"\']+)["\'][^>]*(?:alt=["\']([^"\']*)["\'])?[^>]*>'
    matches = re.findall(img_pattern, html_content, re.IGNORECASE)

    seen_urls = set()
    for src, alt in matches:
        # Skip data URIs
        if src.startswith('data:'):
            continue

        # Resolve relative URLs
        if not src.startswith('http'):
            full_url = urljoin(base_url, src)
        else:
            full_url = src

        # Skip duplicates
        if full_url in seen_urls:
            continue
        seen_urls.add(full_url)

        # Get original filename
        parsed = urlparse(full_url)
        original_name = Path(parsed.path).name

        result['inline_images'].append({
            'url': full_url,
            'original_name': original_name,
            'alt': alt or ''
        })

    return result


class ImageExtractor:
    """Extract and download images from Gutenberg books."""

    def __init__(self, book_id: str, objects_dir: Path, cover_dir: Path = None):
        self.book_id = book_id
        self.objects_dir = objects_dir
        self.cover_dir = cover_dir or objects_dir
        self.downloaded_images = []
        self.cover_image = None
        self.failed_images = []

    def download_cover(self) -> Optional[str]:
        """Download the cover image to the cover directory (assets/img/ by default)."""
        self.cover_dir.mkdir(parents=True, exist_ok=True)

        cover_urls = [
            GUTENBERG_URLS['cover_hires_jpg'].format(id=self.book_id),
            GUTENBERG_URLS['cover_hires_png'].format(id=self.book_id),
            GUTENBERG_URLS['cover_medium'].format(id=self.book_id),
            GUTENBERG_URLS['cover_small'].format(id=self.book_id),
        ]

        for url in cover_urls:
            vprint(f"  Trying cover: {url}")
            content = make_request(url, binary=True)
            if content:
                ext = '.png' if '.png' in url.lower() else '.jpg'
                filename = f"{self.book_id}cover{ext}"
                filepath = self.cover_dir / filename

                with open(filepath, 'wb') as f:
                    f.write(content)

                self.cover_image = filename
                self.downloaded_images.append({
                    'filename': filename,
                    'source_url': url,
                    'type': 'cover'
                })
                print(f"  ✓ Downloaded cover: assets/img/{filename}")
                return filename

        print("  Warning: No cover image found")
        return None

    def download_figures(self, figures: List[Dict], delay: float = 0.2) -> int:
        """Download each figure to objects/<objectid><ext>.

        The filename is the objectid so the metadata CSV, the object file, and
        any Markdown reference all agree. A figure that cannot be fetched is
        skipped rather than failing the run.
        """
        if not figures:
            return 0

        self.objects_dir.mkdir(parents=True, exist_ok=True)
        downloaded = 0
        failed = []

        for index, figure in enumerate(figures, 1):
            filename = f"{figure['objectid']}{figure['extension']}"
            filepath = self.objects_dir / filename

            content = None
            for url in figure['urls']:
                content = make_request(url, binary=True, max_retries=2, use_fallbacks=False)
                if content:
                    figure['source_url'] = url
                    break

            if not content:
                failed.append(figure['objectid'])
                continue

            with open(filepath, 'wb') as f:
                f.write(content)

            figure['downloaded'] = filename
            downloaded += 1
            self.downloaded_images.append({
                'filename': filename,
                'source_url': figure.get('source_url', ''),
                'original_name': figure.get('original_name', ''),
                'type': 'figure',
            })

            if index % 25 == 0 or index == len(figures):
                print(f"  … {index}/{len(figures)} images")
            if delay:
                time.sleep(delay)

        self.failed_images = failed
        print(f"  ✓ Downloaded {downloaded} image(s) to objects/")
        if failed:
            print(f"  Warning: {len(failed)} image(s) could not be fetched: "
                  f"{', '.join(failed[:5])}{' …' if len(failed) > 5 else ''}")
        return downloaded

    def get_results(self) -> Dict:
        """Get summary of downloaded images."""
        return {
            'cover': self.cover_image,
            'images': self.downloaded_images,
        }


# =============================================================================
# HTML to Markdown Conversion
# =============================================================================

def render_markdown_table(rows: List[List[str]], has_header: bool = False) -> str:
    """Render collected table rows as Markdown.

    Kramdown accepts a table with no header row, which suits Gutenberg — its
    tables almost never use <th>.
    """
    rows = [row for row in rows if any(cell.strip() for cell in row)]
    if not rows:
        return ''

    width = max(len(row) for row in rows)
    if width == 1:
        # A single-column table is layout, not data — emit plain paragraphs
        return ''.join(f'{row[0].strip()}\n\n' for row in rows if row[0].strip())

    rows = [row + [''] * (width - len(row)) for row in rows]

    lines = []
    body_start = 0
    if has_header:
        lines.append('| ' + ' | '.join(rows[0]) + ' |')
        lines.append('|' + '|'.join([' --- '] * width) + '|')
        body_start = 1
    for row in rows[body_start:]:
        lines.append('| ' + ' | '.join(row) + ' |')

    return '\n'.join(lines) + '\n\n'


class TableCollector:
    """Accumulates <table> markup so a parser can emit it as Markdown.

    Kept separate from the parsers because both GutenbergHTMLParser and
    WholeBookParser need it, and because tables nest.
    """

    def __init__(self):
        self.stack = []

    @property
    def active(self) -> bool:
        return bool(self.stack)

    def start_table(self) -> None:
        self.stack.append({'rows': [], 'row': None, 'has_header': False})

    def start_row(self) -> None:
        if self.stack:
            self.stack[-1]['row'] = []

    def add_cell(self, text: str, is_header: bool = False, colspan: int = 1) -> None:
        if not self.stack:
            return
        table = self.stack[-1]
        if table['row'] is None:
            table['row'] = []

        text = text.replace('\xa0', ' ')
        text = ' '.join(text.split())  # a Markdown cell must stay on one line
        # Collapsing newlines can strand emphasis markers ("* Greek*" renders as
        # a literal asterisk), so pull them back against their text.
        text = re.sub(r'(\*{1,2})\s+(.+?)\s*\1', r'\1\2\1', text)
        text = re.sub(r'(\*{1,2})(.+?)\s+\1', r'\1\2\1', text)
        text = text.replace('|', '\\|')

        table['row'].append(text)
        table['row'].extend([''] * max(0, colspan - 1))
        if is_header and not table['rows']:
            table['has_header'] = True

    def end_row(self) -> None:
        if not self.stack:
            return
        table = self.stack[-1]
        if table['row'] is not None:
            table['rows'].append(table['row'])
            table['row'] = None

    def end_table(self) -> str:
        if not self.stack:
            return ''
        table = self.stack.pop()
        if table['row']:
            table['rows'].append(table['row'])
        return render_markdown_table(table['rows'], table['has_header'])


def has_body_text(content: str) -> bool:
    """True if a section has real content, not just a heading and rules.

    Anchors that turn out to mark a figure or a bare divider otherwise become
    empty essay files in the reading order.
    """
    for line in content.split('\n'):
        line = line.strip()
        if not line or line.startswith('#') or set(line) <= {'-', '*', '_'}:
            continue
        return True
    return False


class GutenbergHTMLParser(HTMLParser):
    """Parse Project Gutenberg HTML to extract chapters and content.

    Uses multiple strategies for chapter detection:
    1. TOC anchor links (most reliable)
    2. Element IDs matching chapter patterns
    3. Heading text matching chapter patterns
    """

    def __init__(self, toc_anchors: List[str] = None):
        super().__init__()
        self.toc_anchors = toc_anchors or []
        self.sections = []
        self.current_section = None
        self.current_content = []
        self.tag_stack = []
        self.in_boilerplate = False
        self.boilerplate_depth = 0
        self.in_toc = False
        self.in_pagenum = False
        self.in_caption = False
        self.skip_content = False
        self.tables = TableCollector()
        self.in_cell = False
        self.cell_is_header = False
        self.cell_colspan = 1
        self.in_text_block = False
        self.figure_refs = {}
        self.figures_placed = set()
        self.tables_rendered = 0
        self.sections_dropped = []
        self.images_found = []
        self.pending_heading_text = []
        self.in_heading = False
        self.current_heading_tag = None
        self.pending_section_id = None  # ID to use when heading text is captured
        self.pending_section_type = None
        self.in_pre = False

    def _check_element_id(self, element_id: str) -> Tuple[bool, str]:
        """Check if element ID indicates a section boundary."""
        return is_section_id(element_id, self.toc_anchors)

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

        # Skip page numbers and illustration captions
        if tag == 'span' and 'class' in attrs_dict:
            span_class = attrs_dict['class'].lower()
            if 'pagenum' in span_class:
                self.in_pagenum = True
                return
            if 'caption' in span_class:
                self.in_caption = True
                return

        if self.skip_content or self.in_boilerplate:
            return

        # For heading tags: ALWAYS set up heading tracking first
        # Note: We process headings even in TOC mode to detect when TOC ends
        # This ensures we capture heading text for title and chapter detection
        if tag in ('h1', 'h2', 'h3', 'h4'):
            self.in_heading = True
            self.current_heading_tag = tag
            self.pending_heading_text = []
            self.current_content = []

            # Check if heading has an ID that indicates a section
            if 'id' in attrs_dict:
                is_section, section_type = self._check_element_id(attrs_dict['id'])
                if is_section:
                    # Store pending section info - will be created in handle_endtag
                    self.pending_section_id = attrs_dict['id']
                    self.pending_section_type = section_type
            return  # Don't process further - wait for heading text and endtag

        # For div/section with IDs: check if it's a section boundary
        if tag in ('div', 'section') and 'id' in attrs_dict:
            is_section, section_type = self._check_element_id(attrs_dict['id'])
            if is_section:
                # Save previous section
                if self.current_section:
                    self._save_section()

                if section_type == 'toc':
                    self.in_toc = True
                    self.current_section = None
                    return

                self.in_toc = False
                self.current_section = {
                    'id': attrs_dict['id'],
                    'type': section_type,
                    'title': None,
                    'content': []
                }
                return

        # For anchor tags with IDs: check if they match TOC anchors (common in poetry)
        if tag == 'a' and 'id' in attrs_dict:
            anchor_id = attrs_dict['id']
            # Check if this anchor is in our TOC list
            if anchor_id in self.toc_anchors:
                # Save previous section
                if self.current_section:
                    self._save_section()

                # Classify with the shared ID rules rather than a second set
                _, section_type = self._check_element_id(anchor_id)
                section_type = section_type or 'chapter'  # default for poems/sections

                self.in_toc = False
                self.current_section = {
                    'id': anchor_id,
                    'type': section_type,
                    'title': None,  # Will be filled from next heading
                    'content': []
                }
                return

        # Tables: collect cell by cell, emitted as Markdown on </table>
        if self.current_section and not self.in_toc:
            if tag == 'table':
                self.tables.start_table()
                return
            if self.tables.active:
                if tag == 'tr':
                    self.tables.start_row()
                    return
                if tag in ('td', 'th'):
                    self.in_cell = True
                    self.cell_is_header = tag == 'th'
                    try:
                        self.cell_colspan = max(1, int(attrs_dict.get('colspan', 1)))
                    except (TypeError, ValueError):
                        self.cell_colspan = 1
                    self.current_content = []
                    return

        # Track images
        if tag == 'img' and 'src' in attrs_dict:
            src = attrs_dict['src']
            self.images_found.append(src)
            if self.current_section:
                reference = self.figure_refs.get(src)
                if reference:
                    kind, value = reference
                    if kind == 'include':
                        # Blank lines keep the include a block of its own even
                        # when the figure sits inside a paragraph
                        image_markdown = f'\n{value}\n'
                    else:
                        alt = attrs_dict.get('alt', '')
                        image_markdown = f'![{alt}]({value})'
                    self.figures_placed.add(src)
                    if self.in_text_block or self.in_cell:
                        self.current_content.append(f'\n{image_markdown}\n')
                    else:
                        # Most Gutenberg figures sit in a bare <div>, where
                        # current_content is never flushed — write them straight
                        # into the section instead of losing them.
                        self.current_section['content'].append(f'{image_markdown}\n\n')

        # Format tags (only when we have a current section)
        if self.current_section and not self.in_boilerplate:
            if tag in ('p', 'pre', 'blockquote', 'li'):
                self.in_text_block = True
            if tag == 'p':
                if not self.in_cell:
                    self.current_content = []
            elif tag == 'pre':
                self.current_content = []
                self.in_pre = True
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

        if tag == 'span' and self.in_caption:
            self.in_caption = False
            return

        # Heading tag closing: determine if this starts a new section
        if tag in ('h1', 'h2', 'h3', 'h4') and self.in_heading:
            heading_text = ''.join(self.pending_heading_text).strip()
            self.in_heading = False
            heading_tag = self.current_heading_tag
            self.current_heading_tag = None

            # Determine if this heading marks a section boundary
            # Priority: 1) Pending ID from starttag, 2) Text-based detection
            should_create_section = False
            section_id = None
            section_type = None

            # Check pending section from ID detection in starttag
            if self.pending_section_id:
                should_create_section = True
                section_id = self.pending_section_id
                section_type = self.pending_section_type
                self.pending_section_id = None
                self.pending_section_type = None

            # Also check text-based chapter detection
            if not should_create_section and not self.in_boilerplate and not self.skip_content:
                text_is_chapter, text_section_type = is_chapter_heading(heading_text)
                if text_is_chapter:
                    should_create_section = True
                    section_type = text_section_type
                    # Create safe ID from heading text
                    section_id = re.sub(r'[^a-z0-9]+', '-', heading_text.lower()).strip('-')[:50]
                    section_id = section_id or f'section-{len(self.sections)+1}'

            if should_create_section:
                # Save any previous section first
                if self.current_section:
                    self._save_section()

                if section_type == 'toc':
                    self.in_toc = True
                    self.current_section = None
                else:
                    self.in_toc = False
                    self.current_section = {
                        'id': section_id,
                        'type': section_type,
                        'title': heading_text,
                        'content': []
                    }
                    # Add heading to content with proper markdown level
                    level = {'h1': '#', 'h2': '##', 'h3': '###', 'h4': '###'}[tag]
                    self.current_section['content'].append(f'{level} {heading_text}\n\n')

                self.pending_heading_text = []
                self.current_content = []
                return

            # If heading didn't start a new section but we have a current section,
            # add the heading to the current section's content
            if self.current_section and heading_text:
                level = {'h1': '#', 'h2': '##', 'h3': '###', 'h4': '###'}[tag]
                self.current_section['content'].append(f'{level} {heading_text}\n\n')
                if not self.current_section['title']:
                    self.current_section['title'] = heading_text

            self.pending_heading_text = []
            self.current_content = []
            return

        if self.skip_content or self.in_boilerplate or self.in_toc or self.in_pagenum:
            return

        if self.tables.active:
            if tag in ('td', 'th'):
                self.tables.add_cell(''.join(self.current_content),
                                     self.cell_is_header, self.cell_colspan)
                self.current_content = []
                self.in_cell = False
                self.cell_is_header = False
                self.cell_colspan = 1
                return
            if tag == 'tr':
                self.tables.end_row()
                return
            if tag == 'table':
                table_markdown = self.tables.end_table()
                if table_markdown:
                    self.tables_rendered += 1
                    if self.tables.active:  # nested table: fold into the open cell
                        self.current_content.append(table_markdown)
                    elif self.current_section:
                        self.current_section['content'].append(table_markdown)
                return
            if tag == 'p' and self.in_cell:
                self.current_content.append(' ')  # keep paragraphs in one cell
                return

        if tag in ('p', 'pre', 'blockquote', 'li'):
            self.in_text_block = False

        if self.current_section:
            # For <pre> tags, preserve all whitespace; for others, strip it
            if tag == 'pre':
                content = ''.join(self.current_content)  # Don't strip!
            else:
                content = ''.join(self.current_content).strip()

            if tag == 'p':
                if content:
                    self.current_section['content'].append(content + '\n\n')
                self.current_content = []
            elif tag == 'pre':
                if content:
                    # Preserve pre-formatted text (poetry) with exact whitespace
                    # Don't add extra newlines - keep content exactly as-is
                    self.current_section['content'].append(f'<pre>{content}</pre>\n\n')
                self.current_content = []
                self.in_pre = False
            # Note: h1-h4 are handled in the heading block above
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
        # Page numbers and illustration captions sit inside headings in illustrated
        # editions, but they are not part of the title.
        if self.in_heading and data and not self.in_pagenum and not self.in_caption:
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
        if content and not has_body_text(content):
            self.sections_dropped.append(self.current_section.get('title')
                                         or self.current_section['id'])
        if content and has_body_text(content):
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
        self.in_pre = False
        self.tables = TableCollector()
        self.in_cell = False
        self.cell_is_header = False
        self.cell_colspan = 1

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

        if tag == 'table':
            self.tables.start_table()
            return
        if self.tables.active:
            if tag == 'tr':
                self.tables.start_row()
                return
            if tag in ('td', 'th'):
                self.in_cell = True
                self.cell_is_header = tag == 'th'
                try:
                    self.cell_colspan = max(1, int(attrs_dict.get('colspan', 1)))
                except (TypeError, ValueError):
                    self.cell_colspan = 1
                self.current_text = []
                return

        if tag == 'p':
            if not self.in_cell:
                self.current_text = []
        elif tag == 'pre':
            self.current_text = []
            self.in_pre = True
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

        if self.tables.active:
            if tag in ('td', 'th'):
                self.tables.add_cell(''.join(self.current_text),
                                     self.cell_is_header, self.cell_colspan)
                self.current_text = []
                self.in_cell = False
                self.cell_is_header = False
                self.cell_colspan = 1
                return
            if tag == 'tr':
                self.tables.end_row()
                return
            if tag == 'table':
                table_markdown = self.tables.end_table()
                if table_markdown:
                    if self.tables.active:  # nested table: fold into the open cell
                        self.current_text.append(table_markdown)
                    else:
                        self.content.append(table_markdown)
                return
            if tag == 'p' and self.in_cell:
                self.current_text.append(' ')  # keep paragraphs in one cell
                return

        # For <pre> tags, preserve all whitespace; for others, strip it
        if tag == 'pre':
            text = ''.join(self.current_text)  # Don't strip!
        else:
            text = ''.join(self.current_text).strip()

        if tag == 'p' and text:
            self.content.append(text + '\n\n')
            self.current_text = []
        elif tag == 'pre' and text:
            # Preserve pre-formatted text (poetry) with exact whitespace
            # Don't add extra newlines - keep content exactly as-is
            self.content.append(f'<pre>{text}</pre>\n\n')
            self.current_text = []
            self.in_pre = False
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
            # In <pre> tags, preserve whitespace and newlines
            if self.in_pre:
                self.current_text.append(data)
            else:
                self.current_text.append(data)

    def get_content(self) -> str:
        return ''.join(self.content).strip()


# =============================================================================
# Output Generation
# =============================================================================

MIME_TYPES = {
    '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.png': 'image/png',
    '.gif': 'image/gif', '.webp': 'image/webp', '.svg': 'image/svg+xml',
}

COLLECTION_CSV_FIELDS = [
    'objectid', 'title', 'creator', 'date', 'description', 'subject',
    'source', 'identifier', 'type', 'format', 'language', 'rights',
    'rightsstatement', 'display_template', 'object_location', 'image_small',
    'image_thumb', 'image_alt_text',
]


def write_collection_csv(figures: List[Dict], metadata: Dict, data_dir: Path,
                         slug: str) -> Optional[str]:
    """Write one metadata row per downloaded figure.

    Returns the CSV stem for the _config.yml `metadata:` pointer, which takes a
    filename with no extension.
    """
    rows = [f for f in figures if f.get('downloaded')]
    if not rows:
        return None

    data_dir.mkdir(parents=True, exist_ok=True)
    csv_stem = f'{slug}-metadata'
    csv_path = data_dir / f'{csv_stem}.csv'

    book_title = metadata.get('title', '')
    gutenberg_url = metadata.get('gutenberg_url', '')

    with open(csv_path, 'w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=COLLECTION_CSV_FIELDS)
        writer.writeheader()
        for figure in rows:
            extension = Path(figure['downloaded']).suffix.lower()
            object_path = f'/objects/{figure["downloaded"]}'
            description = figure.get('caption') or figure.get('alt') or ''
            writer.writerow({
                'objectid': figure['objectid'],
                'title': normalize_text(figure['title']),
                'creator': metadata.get('author', ''),
                'date': metadata.get('publication_date', ''),
                'description': normalize_text(description),
                'subject': 'illustrations',
                'source': f'{book_title} (Project Gutenberg) {gutenberg_url}'.strip(),
                'identifier': figure.get('original_name', ''),
                'type': 'Image;StillImage',
                'format': MIME_TYPES.get(extension, 'image/jpeg'),
                'language': metadata.get('language', ''),
                'rights': metadata.get('rights', 'Public Domain'),
                'rightsstatement': 'https://creativecommons.org/publicdomain/mark/1.0/',
                'display_template': 'image',
                'object_location': object_path,
                # Gutenberg illustrations are small enough to serve as their own
                # derivatives; `rake generate_derivatives` can replace these with
                # real thumbnails later.
                'image_small': object_path,
                'image_thumb': object_path,
                'image_alt_text': normalize_text(figure.get('alt') or figure['title']),
            })

    print(f"  ✓ Wrote {len(rows)} collection items to _data/{csv_stem}.csv")
    return csv_stem


def update_config_metadata(root_path: Path, csv_stem: str) -> bool:
    """Point _config.yml's `metadata:` key at the generated CSV.

    Rewrites the single line rather than round-tripping the YAML, so comments
    and formatting elsewhere in the file are untouched.
    """
    config_path = root_path / '_config.yml'
    if not config_path.exists():
        print(f"  Warning: {config_path} not found; skipping metadata pointer update")
        return False

    text = config_path.read_text(encoding='utf-8')
    updated, count = re.subn(r'(?m)^metadata:.*$', f'metadata: {csv_stem}', text, count=1)
    if not count:
        print("  Warning: no `metadata:` key in _config.yml; skipping pointer update")
        return False

    config_path.write_text(updated, encoding='utf-8')
    print(f"  ✓ Set _config.yml metadata: {csv_stem}")
    return True


def create_cb_essay_book_yml(metadata: Dict, image_urls: Dict, sections_info: Dict,
                             downloaded_cover: str = None) -> str:
    """Create book.yml for CB-Essay _data folder."""
    lines = ['# Book Metadata for CB-Essay', '# Generated by gutenberg-extraction.py', '']

    # Core metadata
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

    lines.append(f'gutenberg_url: "{metadata.get("gutenberg_url", "")}"')

    if metadata.get('download_count'):
        lines.append(f'download_count: {metadata["download_count"]}')

    lines.append(f'extracted_at: "{metadata.get("extracted_at", "")}"')

    # Subjects
    if metadata.get('subjects'):
        lines.append('')
        lines.append('subjects:')
        for subject in metadata['subjects'][:10]:  # Limit to 10
            lines.append(f'  - {normalize_text(subject, for_yaml=True)}')

    # Bookshelves
    if metadata.get('bookshelves'):
        lines.append('')
        lines.append('bookshelves:')
        for shelf in metadata['bookshelves'][:10]:  # Limit to 10
            lines.append(f'  - {normalize_text(shelf, for_yaml=True)}')

    # Images
    lines.append('')
    lines.append('# Cover Image')
    if downloaded_cover:
        lines.append(f'cover_image: "assets/img/{downloaded_cover}"')
    if image_urls.get('cover_urls'):
        lines.append('cover_urls:')
        for url in image_urls['cover_urls']:
            lines.append(f'  - "{url}"')

    # Inline images from book content
    if image_urls.get('inline_images'):
        lines.append('')
        lines.append(f'# Inline Images ({len(image_urls["inline_images"])} found in book)')
        lines.append('inline_images:')
        for img in image_urls['inline_images']:
            lines.append(f'  - url: "{img["url"]}"')
            if img.get('original_name'):
                lines.append(f'    filename: "{img["original_name"]}"')
            if img.get('alt'):
                lines.append(f'    alt: {normalize_text(img["alt"], for_yaml=True)}')

    # Content structure
    lines.append('')
    lines.append('# Content Structure')
    lines.append(f'front_matter_count: {sections_info.get("front_matter_count", 0)}')
    lines.append(f'chapter_count: {sections_info.get("chapter_count", 0)}')
    lines.append(f'total_sections: {sections_info.get("total_sections", 0)}')

    if sections_info.get('files'):
        lines.append('')
        lines.append('# Essay files (in /_essay folder)')
        lines.append('essay_files:')
        for f in sections_info['files']:
            lines.append(f'  - "{f}"')

    return '\n'.join(lines) + '\n'


def liquid_param(text: str) -> str:
    """Make text safe to pass as a double-quoted Liquid include parameter."""
    text = ' '.join((text or '').split())
    return text.replace('"', "'")


def build_figure_references(figures: List[Dict], illustrations: str) -> Dict[str, Tuple[str, str]]:
    """Decide how each figure should appear in the essay Markdown.

    'download' mode cites the collection item by objectid, so caption, alt text
    and the full-screen viewer all come from the metadata CSV. 'link' mode points
    the same include at Gutenberg's own copy of the image, which the include
    accepts as long as alt text is supplied.
    """
    references = {}

    for figure in figures:
        if illustrations == 'download':
            if not figure.get('downloaded'):
                continue
            params = f'objectid="{figure["objectid"]}"'
        elif illustrations == 'link':
            alt = liquid_param(figure.get('alt') or figure['title'])
            params = f'objectid="{figure["urls"][0]}" alt="{alt}"'
            caption = liquid_param(figure.get('caption') or figure.get('title'))
            if caption:
                params += f' caption="{caption}"'
        elif illustrations == 'path':
            # --all-images without collection integration: plain Markdown image
            if not figure.get('downloaded'):
                continue
            references[figure['src']] = ('image', f'/objects/{figure["downloaded"]}')
            continue
        else:
            continue

        references[figure['src']] = (
            'include',
            '{% include essay/feature/image-gallery.html ' + params + ' %}',
        )

    return references


def create_cb_essay_markdown(section: Dict, order: int, part: str = None, is_divider: bool = False) -> str:
    """Create markdown file for CB-Essay _essay folder (simplified front matter)."""
    title = normalize_text(section['title'], for_yaml=True)

    fm_lines = ['---']
    fm_lines.append(f'title: {title}')
    fm_lines.append(f'order: {order}')
    if part:
        fm_lines.append(f'part: {part}')
    if is_divider:
        fm_lines.append('part_divider: true')
    fm_lines.append('---')
    fm_lines.append('')

    return '\n'.join(fm_lines) + section['content']


def save_cb_essay_files(front_matter: List[Dict], chapters: List[Dict],
                        essay_out: Path, data_dir: Path,
                        metadata: Dict, image_urls: Dict,
                        downloaded_cover: str = None,
                        part_map: Dict = None,
                        part_divider_ids: set = None) -> Dict:
    """Save essay markdown files and book.yml."""
    essay_out.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)

    all_sections = front_matter + chapters
    saved_files = []

    print(f"\nSaving {len(front_matter)} front matter + {len(chapters)} chapters...")

    for idx, section in enumerate(all_sections, 1):
        if idx <= len(front_matter):
            number = f"00-{idx:02d}"
        else:
            number = f"{idx - len(front_matter):02d}"

        filename = f"{number}-{sanitize_filename(section['title'])}.md"
        filepath = essay_out / filename

        part = (part_map or {}).get(section.get('id'))
        is_divider = bool(part_divider_ids and section.get('id') in part_divider_ids)
        content = create_cb_essay_markdown(section, idx, part=part, is_divider=is_divider)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        saved_files.append(filename)
        vprint(f"  ✓ {essay_out.name}/{filename}")

    sections_info = {
        'front_matter_count': len(front_matter),
        'chapter_count': len(chapters),
        'total_sections': len(all_sections),
        'files': saved_files
    }

    yaml_content = create_cb_essay_book_yml(metadata, image_urls, sections_info, downloaded_cover)
    yaml_path = data_dir / 'book.yml'

    with open(yaml_path, 'w', encoding='utf-8') as f:
        f.write(yaml_content)

    return {
        'essay_files': saved_files,
        'book_yml': str(yaml_path),
        'image_urls': image_urls
    }



# =============================================================================
# Main Extraction Process
# =============================================================================

def looks_like_html(content: str) -> bool:
    """Sanity-check a downloaded page before handing it to the parsers.

    Guards against compressed/binary or error-page responses, which otherwise
    parse to zero sections and fail much later with a confusing message.
    """
    if not content or len(content) < 2000:
        # Real Gutenberg books run to tens of KB; anything this small is an
        # error or gateway-timeout page, even though it parses as valid HTML.
        return False
    head = content[:5000].lower()
    return '<html' in head or '<body' in head or '<p' in head or '<div' in head


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
        if content and looks_like_html(content):
            print(f"  ✓ Downloaded HTML from {url}")
            return content, url
        if content:
            print(f"  ✗ Response was not readable HTML ({len(content)} chars) — trying next source")

    return None, None


def generate_about_page(metadata: Dict, root_path: Path) -> None:
    """Write pages/about.md with the catalog card include and attribution paragraph."""
    pages_dir = root_path / 'pages'
    pages_dir.mkdir(parents=True, exist_ok=True)

    title = metadata.get('title', 'About This Book')
    author = metadata.get('author', '')
    page_title = f"{title} — About"
    sep = '-' * 3
    include_tag = '{%' + ' include essay/feature/catalog-card.html ' + '%}'

    edition_note = (
        f"This edition was automatically generated from [Project Gutenberg](https://www.gutenberg.org/about/), the preeminent library of "
        "public domain ebooks on the internet.\n\n"
        "The edition is published using [CB-Essay](https://collectionbuilder.github.io/cb-essay/), "
        "and the text used for this edition was extracted via its "
        "[Gutenberg Extraction Script](https://github.com/CollectionBuilder/cb-essay/blob/main/gutenberg-extraction.py)."
    )

    lines = [
        sep,
        f'title: "{page_title}"',
        'layout: about',
        'permalink: /about.html',
        'credits: true',
        'text-search: false',
        sep,
        '',
        include_tag,
        '',
        '## About This Edition',
        '',
        edition_note,
        '',
    ]

    about_path = pages_dir / 'about.md'
    with open(about_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f"  ✓ pages/about.md")


def update_theme_print_author(root_path: Path, author: Optional[str]) -> bool:
    """Update _data/theme.yml print.author when author metadata is available."""
    author_value = (author or '').strip()
    if not author_value:
        print("  Skipping theme print.author update (no author metadata)")
        return False

    theme_path = root_path / '_data' / 'theme.yml'
    if not theme_path.exists():
        print(f"  Warning: {theme_path} not found; skipping print.author update")
        return False

    content = theme_path.read_text(encoding='utf-8')
    has_trailing_newline = content.endswith('\n')
    lines = content.splitlines()

    author_yaml = '"' + author_value.replace('\\', '\\\\').replace('"', '\\"') + '"'

    print_start = None
    for i, line in enumerate(lines):
        if re.match(r'^\s*print:\s*$', line):
            print_start = i
            break

    if print_start is None:
        if lines and lines[-1].strip():
            lines.append('')
        lines.append('print:')
        lines.append(f'  author: {author_yaml}')
    else:
        print_end = len(lines)
        for i in range(print_start + 1, len(lines)):
            line = lines[i]
            if line and not line.startswith((' ', '\t')):
                print_end = i
                break

        author_line = None
        for i in range(print_start + 1, print_end):
            if re.match(r'^\s{2}author\s*:', lines[i]):
                author_line = i
                break

        if author_line is not None:
            lines[author_line] = f'  author: {author_yaml}'
        else:
            lines.insert(print_start + 1, f'  author: {author_yaml}')

    updated = '\n'.join(lines)
    if has_trailing_newline:
        updated += '\n'

    theme_path.write_text(updated, encoding='utf-8')
    print(f'  ✓ Updated _data/theme.yml print.author: {author_value}')
    return True


def count_prose_words(text: str) -> int:
    """Word count of Markdown body text, ignoring markup we generated ourselves.

    Liquid includes and image references would otherwise inflate the count —
    167 image-gallery includes are well over a thousand words of tags.
    """
    text = re.sub(r'\{%.*?%\}', ' ', text, flags=re.DOTALL)
    text = re.sub(r'!\[[^\]]*\]\([^)]*\)', ' ', text)
    text = re.sub(r'<[^>]+>', ' ', text)
    return len(text.split())


def count_source_words(html_text: str) -> int:
    """Word count of the de-boilerplated source, for a retention comparison."""
    body = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', html_text,
                  flags=re.DOTALL | re.IGNORECASE)
    return len(re.sub(r'<[^>]+>', ' ', body).split())


TOC_METHOD_LABELS = {
    'container': 'a contents container in the markup',
    'heading': 'the block following a "Contents" heading',
    'none': 'NOT FOUND — fell back to scanning the whole document',
}


def write_extraction_report(root_path: Path, report: Dict) -> None:
    """Write extraction-results.md: what the run produced and what needs a human.

    Written on failure too — a run that produced nothing is exactly when the
    numbers are worth reading.
    """
    lines = []
    title = report.get('title') or f"Book {report.get('book_id', '?')}"
    lines.append(f'# Extraction Results — {title}')
    lines.append('')
    meta = [f"Book {report.get('book_id', '?')}"]
    if report.get('slug'):
        meta.append(report['slug'])
    meta.append(report.get('timestamp', ''))
    meta.append(f"illustrations: {report.get('illustrations', 'none')}")
    lines.append(' · '.join(m for m in meta if m))
    lines.append('')

    if report.get('failed'):
        lines.append('## ⚠ Extraction failed')
        lines.append('')
        lines.append(report['failed'])
        lines.append('')

    # ---- Summary ----
    lines.append('## Summary')
    lines.append('')
    lines.append('| | |')
    lines.append('|---|---|')

    sections = report.get('sections', {})
    total = sections.get('front_matter', 0) + sections.get('chapters', 0)
    lines.append(f"| Sections | {total} "
                 f"({sections.get('front_matter', 0)} front matter, "
                 f"{sections.get('chapters', 0)} chapters) |")

    source_words = report.get('source_words', 0)
    output_words = report.get('output_words', 0)
    if source_words:
        retention = 100.0 * output_words / source_words
        lines.append(f'| Text kept | {retention:.1f}% of {source_words:,} source words |')

    tables = report.get('tables', {})
    if tables.get('found'):
        lines.append(f"| Tables | {tables['found']} found, {tables.get('rendered', 0)} rendered |")

    figures = report.get('figures', {})
    if figures.get('kept'):
        lines.append(f"| Figures | {figures['kept']} catalogued, "
                     f"{figures.get('placed', 0)} placed in essays |")
        if figures.get('downloaded') is not None:
            lines.append(f"| Images downloaded | {figures['downloaded']} to objects/ |")

    lines.append(f"| Cover | {report['cover'] if report.get('cover') else 'not found'} |")
    if report.get('collection_csv'):
        lines.append(f"| Collection CSV | _data/{report['collection_csv']}.csv |")
    lines.append('')

    # ---- Needs a human ----
    todo = report.get('todo', [])
    lines.append('## Needs a human')
    lines.append('')
    if todo:
        lines.extend(f'- {item}' for item in todo)
    else:
        lines.append('Nothing flagged — the numbers above are all in normal range.')
    lines.append('')

    # ---- How structure was detected ----
    lines.append('## How structure was detected')
    lines.append('')
    method = report.get('toc_method', 'none')
    lines.append(f'- Table of contents: {TOC_METHOD_LABELS.get(method, method)}')
    lines.append(f"- TOC anchors found: {report.get('toc_anchors', 0)}")
    lines.append(f"- Source: {report.get('source_url', 'unknown')}")
    if report.get('dropped_sections'):
        dropped = ', '.join(report['dropped_sections'][:8])
        more = ' …' if len(report['dropped_sections']) > 8 else ''
        lines.append(f'- Sections dropped as empty: {dropped}{more}')
    lines.append('')

    lines.append('---')
    lines.append('')
    lines.append('Regenerated on every extraction run. See `EXTRACTION-NOTES.md` for how '
                 'the script works and what the known limitations are.')
    lines.append('')

    path = root_path / 'extraction-results.md'
    path.write_text('\n'.join(lines), encoding='utf-8')
    print(f"  ✓ Wrote extraction-results.md")


def build_report_todos(report: Dict) -> List[str]:
    """Turn the run's numbers into an actionable list, or nothing if all is well."""
    todo = []

    if report.get('toc_method') == 'none':
        todo.append('**No table of contents was found**, so chapter boundaries came from '
                    'heading text alone — check that the chapter split looks right.')

    source_words = report.get('source_words', 0)
    output_words = report.get('output_words', 0)
    if source_words and 100.0 * output_words / source_words < 95.0:
        missing = source_words - output_words
        todo.append(f'**{missing:,} source words ({100.0 * missing / source_words:.0f}%) '
                    'did not carry over.** Some of that is always apparatus — page numbers, '
                    'the contents list, transcriber\'s notes — but a gap this size is worth '
                    'a look.')

    tables = report.get('tables', {})
    dropped_tables = tables.get('found', 0) - tables.get('rendered', 0)
    if dropped_tables > 0:
        todo.append(f'{dropped_tables} table(s) were not rendered. Tables that sit before '
                    'the first section (a contents table, for instance) are dropped by '
                    'design; any others are worth checking.')

    figures = report.get('figures', {})
    unplaced = figures.get('kept', 0) - figures.get('placed', 0)
    if unplaced > 0 and figures.get('kept'):
        names = ', '.join(f'`{o}`' for o in report.get('unplaced_figures', [])[:5])
        more = ' …' if len(report.get('unplaced_figures', [])) > 5 else ''
        todo.append(f'{unplaced} figure(s) catalogued but not placed in any essay: {names}{more} '
                    '— usually cover or title-page plates that appear before the first section.')

    if report.get('failed_images'):
        names = ', '.join(f'`{o}`' for o in report['failed_images'][:5])
        more = ' …' if len(report['failed_images']) > 5 else ''
        todo.append(f"{len(report['failed_images'])} image(s) could not be downloaded: "
                    f'{names}{more} — rerun to retry, or Gutenberg may have been throttling.')

    if report.get('dropped_sections'):
        todo.append(f"{len(report['dropped_sections'])} section(s) had a heading but no body "
                    'text and were dropped.')

    if not report.get('cover') and not report.get('images_skipped'):
        todo.append('No cover image was found — set `featured-image` in `_data/theme.yml` '
                    'by hand, or pick `image-style: no-image`.')

    if report.get('collection_csv'):
        todo.append('Collection images are serving as their own thumbnails. Run '
                    '`bundle exec rake generate_derivatives` for real ones.')

    return todo


def extract_book(book_id: str, project_root: str = None, essay_dir: str = None,
                 slug: str = None, skip_images: bool = False,
                 download_all_images: bool = False, local_html: str = None,
                 clear: bool = False, about_page: bool = False,
                 illustrations: str = 'none', verbose: bool = False) -> bool:
    """
    Main extraction function. Writes essay files to _essay/, metadata to _data/book.yml,
    and images to objects/ within the project root.

    Args:
        book_id: Project Gutenberg book ID
        project_root: CB-Essay project root (default: current directory)
        essay_dir: Write essay markdown here instead of {project_root}/_essay/
        slug: Custom book slug for book.yml (default: auto-generated)
        skip_images: Skip downloading images to objects/
        download_all_images: Download all inline images, not just the cover
        local_html: Path to local HTML file (skips download)
        clear: Delete existing .md files from essay output dir before writing
        about_page: Generate pages/about.md with catalog card include and placeholder sections
        illustrations: How to handle the book's illustrations —
            'none' (skip), 'link' (cite Gutenberg's copies in image-gallery includes),
            or 'download' (fetch into objects/ and register as collection items)
        verbose: Enable verbose output

    Returns:
        True if successful, False otherwise
    """
    global _verbose
    _verbose = verbose

    print("=" * 60)
    print(f"Extracting Project Gutenberg Book #{book_id}")
    print("=" * 60)

    root_path = Path(project_root) if project_root else Path.cwd()
    essay_out = Path(essay_dir) if essay_dir else root_path / '_essay'
    data_dir = root_path / '_data'
    objects_dir = root_path / 'objects'
    assets_img_dir = root_path / 'assets' / 'img'

    html_content = None
    html_url = None

    # Step 1: Load HTML
    if local_html:
        print(f"\n[1/5] Loading local HTML file: {local_html}")
        try:
            with open(local_html, 'r', encoding='utf-8', errors='replace') as f:
                html_content = f.read()
            html_url = f"file://{Path(local_html).absolute()}"
            vprint(f"  ✓ Loaded {len(html_content)} bytes")
        except Exception as e:
            print(f"  ERROR: Could not read local file: {e}")
            return False

        print("\n[2/5] Extracting metadata from HTML...")
        meta_extractor = MetadataExtractor(book_id)
        meta_extractor.extract_from_html(html_content)
    else:
        print("\n[1/5] Extracting metadata...")
        meta_extractor = MetadataExtractor(book_id)
        meta_extractor.extract_from_gutendex()
        meta_extractor.extract_from_rdf()

        print("\n[2/5] Downloading HTML content...")
        html_content, html_url = download_html(book_id)
        if not html_content:
            print("ERROR: Could not download HTML from any source")
            print("\nTIP: Download the HTML manually and use --local-html:")
            print(f"     wget -O book.html 'https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}-images.html'")
            print(f"     python gutenberg-extraction.py {book_id} --local-html book.html")
            return False

        meta_extractor.extract_from_html(html_content)

    body_metadata = extract_metadata_from_body_text(html_content)
    current_metadata = meta_extractor.get_metadata()
    for key, value in body_metadata.items():
        if key not in current_metadata or not current_metadata[key]:
            meta_extractor.metadata[key] = value

    metadata = meta_extractor.get_metadata()
    print(f"  Title:  {metadata.get('title', 'Unknown')}")
    print(f"  Author: {metadata.get('author', 'Unknown')}")

    if not slug:
        slug = create_slug(metadata.get('title'), metadata.get('author'), book_id)

    # Step 3: Download images to objects/
    print("\n[3/5] Processing images...")
    image_extractor = ImageExtractor(book_id, objects_dir, cover_dir=assets_img_dir)
    downloaded_cover = None

    figures = []
    figure_stats = {}
    if illustrations != 'none' or download_all_images:
        # Cataloguing the figures needs no network — only fetching them does
        figures = build_figures(book_id, html_content, html_url or '', stats=figure_stats)
        print(f"  Found {len(figures)} illustration(s) in the book")

    if skip_images:
        print("  Skipping image downloads (--skip-images)")
        if illustrations == 'download':
            print("  Note: --skip-images means no files to catalogue; "
                  "use --illustrations link to cite Gutenberg's copies instead")
    else:
        downloaded_cover = image_extractor.download_cover()
        if illustrations == 'download' or download_all_images:
            image_extractor.download_figures(figures)
        elif illustrations == 'link':
            print("  Linking to Gutenberg's copies — no image files downloaded")

    # Always collect image URLs for book.yml regardless of download choice
    image_urls = extract_image_urls(book_id, html_content, html_url or '')
    vprint(f"  Found {len(image_urls.get('cover_urls', []))} cover URL(s)")
    vprint(f"  Found {len(image_urls.get('inline_images', []))} inline image URL(s)")

    # Step 4: Parse HTML to markdown
    print("\n[4/5] Parsing content and converting to Markdown...")
    clean_html = remove_gutenberg_boilerplate(html_content)
    vprint(f"  Removed boilerplate: {len(html_content)} -> {len(clean_html)} chars")

    toc_anchors = extract_toc_anchors(html_content)
    _toc_region, toc_method = find_toc_region(html_content)
    if toc_anchors:
        vprint(f"  Found {len(toc_anchors)} TOC anchor links")

    part_map = extract_toc_part_map(html_content)
    part_divider_ids = {k for k in part_map if re.match(r'^part\d+$', k, re.IGNORECASE)}
    if part_map:
        part_labels = sorted(set(part_map.values()))
        vprint(f"  Detected {len(part_labels)} TOC parts: {part_labels}")

    parser = GutenbergHTMLParser(toc_anchors=toc_anchors)
    reference_mode = illustrations
    if reference_mode == 'none' and download_all_images:
        reference_mode = 'path'
    parser.figure_refs = build_figure_references(figures, reference_mode)
    parser.feed(clean_html)
    front_matter, chapters, _ = parser.get_results()

    print(f"  Found {len(front_matter)} front matter + {len(chapters)} chapters")

    report = {
        'book_id': book_id,
        'title': metadata.get('title'),
        'slug': slug,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'illustrations': illustrations,
        'source_url': html_url or local_html or 'unknown',
        'toc_method': toc_method,
        'toc_anchors': len(toc_anchors),
        'source_words': count_source_words(clean_html),
        'tables': {
            'found': len(re.findall(r'<table\b', clean_html, re.IGNORECASE)),
            'rendered': parser.tables_rendered,
        },
        'dropped_sections': parser.sections_dropped,
        'cover': (f'assets/img/{downloaded_cover}' if downloaded_cover
                  else ('skipped (--skip-images)' if skip_images else None)),
        'failed_images': image_extractor.failed_images,
        'images_skipped': skip_images,
    }

    if not chapters and not front_matter:
        print("  No chapters detected — extracting as single document...")
        whole_parser = WholeBookParser()
        whole_parser.feed(clean_html)
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
            report['failed'] = ('No sections and no document-level content could be parsed '
                                'from the source HTML. If the source looks fine in a browser, '
                                'the fetch itself is the first thing to check.')
            report['sections'] = {'front_matter': 0, 'chapters': 0}
            report['output_words'] = 0
            report['todo'] = build_report_todos(report)
            write_extraction_report(root_path, report)
            return False

    # Step 5: Save files
    print("\n[5/5] Saving files...")

    # Handle --clear and warn about existing files
    if essay_out.exists():
        existing_md = list(essay_out.glob('*.md'))
        if clear and existing_md:
            for f in existing_md:
                f.unlink()
            print(f"  Cleared {len(existing_md)} existing file(s) from {essay_out}")
        elif existing_md and not clear:
            print(f"\n  Warning: {len(existing_md)} existing markdown file(s) in {essay_out}")
            print("  Use --clear to remove them before extraction.")

    save_cb_essay_files(
        front_matter, chapters, essay_out, data_dir,
        metadata, image_urls, downloaded_cover,
        part_map=part_map,
        part_divider_ids=part_divider_ids,
    )

    csv_stem = None
    if illustrations == 'download':
        csv_stem = write_collection_csv(figures, metadata, data_dir, slug)
        if csv_stem:
            update_config_metadata(root_path, csv_stem)
        else:
            print("  No illustrations downloaded; collection CSV not written")

    update_theme_print_author(root_path, metadata.get('author'))

    # ---- Extraction report ----
    placed = len(parser.figures_placed)
    report['sections'] = {'front_matter': len(front_matter), 'chapters': len(chapters)}
    report['output_words'] = sum(count_prose_words(s['content'])
                                 for s in front_matter + chapters)
    report['figures'] = {
        'seen': figure_stats.get('seen', 0),
        'decorative': figure_stats.get('decorative', 0),
        'kept': len(figures),
        'placed': placed,
    }
    if illustrations == 'download' or download_all_images:
        report['figures']['downloaded'] = sum(1 for f in figures if f.get('downloaded'))
    report['unplaced_figures'] = [f['objectid'] for f in figures
                                  if f['src'] not in parser.figures_placed]
    report['collection_csv'] = csv_stem if illustrations == 'download' else None
    report['todo'] = build_report_todos(report)
    write_extraction_report(root_path, report)

    total = len(front_matter) + len(chapters)
    print("\n" + "=" * 60)
    print("✓ Extraction Complete!")
    print("=" * 60)
    print(f"  Project root:  {root_path}")
    print(f"  Essay files:   {essay_out} ({total} files)")
    print(f"  Metadata:      {data_dir / 'book.yml'}")
    if downloaded_cover:
        print(f"  Cover image:   assets/img/{downloaded_cover}")
    elif not skip_images:
        print("  Cover image:   not found")

    if about_page:
        generate_about_page(metadata, root_path)
        print(f"  About page:    pages/about.md")

    return True


def main():
    parser = argparse.ArgumentParser(
        description='Extract a Project Gutenberg book into a CollectionBuilder-Essay project.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s 64317                          # Extract The Great Gatsby into ./_essay/
  %(prog)s 84 --clear                     # Extract Frankenstein, clearing prior files first
  %(prog)s 84 --project-root ~/my-site    # Extract into a different project directory
  %(prog)s 84 --output ./staging          # Write markdown to ./staging/ instead of _essay/
  %(prog)s 11 --all-images                # Download all inline images to objects/
  %(prog)s 25290 --illustrations link     # Cite Gutenberg's images, download nothing
  %(prog)s 25290 --illustrations download # Illustrations as collection items + metadata CSV
  %(prog)s 84 --skip-images               # Skip image downloading entirely
  %(prog)s 84 --local-html pg84.html      # Use a locally downloaded HTML file
  %(prog)s 84 --slug frankenstein         # Set a custom book slug in book.yml

If downloads fail (403 errors), download the HTML manually first:
  wget -O book.html 'https://www.gutenberg.org/cache/epub/84/pg84-images.html'
  %(prog)s 84 --local-html book.html
        """
    )

    parser.add_argument('book_id', type=str,
                        help='Project Gutenberg book ID (e.g., 84 for Frankenstein)')
    parser.add_argument('--project-root', metavar='DIR',
                        help='CB-Essay project root — writes to {root}/_essay/ and {root}/_data/book.yml (default: current directory)')
    parser.add_argument('--output', '-o', metavar='DIR',
                        help='Write essay markdown files here instead of {project-root}/_essay/')
    parser.add_argument('--slug', '-s',
                        help='Custom book slug for book.yml (default: auto-generated from title/author)')
    parser.add_argument('--clear', action='store_true',
                        help='Clear existing markdown files from the essay output directory before writing')
    parser.add_argument('--skip-images', action='store_true',
                        help='Skip downloading images to objects/')
    parser.add_argument('--all-images', action='store_true',
                        help='Download all inline images in addition to the cover')
    parser.add_argument('--local-html', '-l', metavar='FILE',
                        help='Path to a locally downloaded HTML file (skips fetching from Gutenberg)')
    parser.add_argument('--illustrations', choices=['none', 'link', 'download'],
                        default='none',
                        help="How to handle the book's illustrations: 'none' (default), "
                             "'link' to cite Gutenberg's copies in image-gallery includes, "
                             "or 'download' to fetch them into objects/ and register them "
                             'as collection items in _data/<slug>-metadata.csv')
    parser.add_argument('--collection-images', action='store_true',
                        help='Alias for --illustrations download')
    parser.add_argument('--about-page', action='store_true',
                        help='Generate pages/about.md with a catalog card include and placeholder editorial sections')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Enable verbose output')

    args = parser.parse_args()

    success = extract_book(
        book_id=args.book_id,
        project_root=args.project_root,
        essay_dir=args.output,
        slug=args.slug,
        clear=args.clear,
        skip_images=args.skip_images,
        download_all_images=args.all_images,
        local_html=args.local_html,
        about_page=args.about_page,
        illustrations='download' if args.collection_images else args.illustrations,
        verbose=args.verbose,
    )

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
