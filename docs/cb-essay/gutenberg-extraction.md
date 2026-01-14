# Project Gutenberg HTML extraction patterns for Python scripts

Project Gutenberg's **60,000+ free ebooks use remarkably consistent patterns** despite spanning decades of digitization. Most books follow predictable HTML structures with text-based markers for boilerplate, standardized image URL patterns, and Dublin Core metadata—making automated extraction highly feasible. Here's what works reliably across the widest range of books.

## Primary discovery: text markers trump HTML structure

The single most important finding is that **text-based pattern matching is far more reliable than HTML structure parsing** for Project Gutenberg books. While HTML elements vary significantly between older (pre-2005) and newer (post-2010) digitizations, text markers remain remarkably consistent. This should fundamentally shape your Python extraction strategy—use regex and string matching as your primary tool, not CSS selectors.

## Boilerplate identification and removal

### Text markers that define content boundaries

Project Gutenberg uses **START and END markers** that reliably indicate where actual book content begins and ends. Your script should search for these text patterns first:

**Header end markers** (where actual content begins):
```python
START_MARKERS = [
    "*** START OF THIS PROJECT GUTENBERG EBOOK",
    "*** START OF THE PROJECT GUTENBERG EBOOK", 
    "*** START OF THE PROJECT GUTENBERG ETEXT",
    "*END*THE SMALL PRINT",  # older books
]
```

**Footer start markers** (where actual content ends):
```python
END_MARKERS = [
    "End of the Project Gutenberg EBook",
    "End of Project Gutenberg's",
    "*** END OF THIS PROJECT GUTENBERG EBOOK",
    "*** END OF THE PROJECT GUTENBERG EBOOK",
    "End of this Project Gutenberg",
]
```

### Recommended Python implementation

```python
def remove_gutenberg_boilerplate(html_text):
    """Remove Project Gutenberg header and footer boilerplate."""
    lines = html_text.split('\n')
    
    start_line = 0
    end_line = len(lines)
    
    # Find content start (after header)
    for i, line in enumerate(lines):
        if any(marker in line for marker in START_MARKERS):
            start_line = i + 1
            break
    
    # Find content end (before footer) - only check after line 100
    for i in range(max(100, start_line), len(lines)):
        if any(marker in lines[i] for marker in END_MARKERS):
            end_line = i
            break
    
    return '\n'.join(lines[start_line:end_line])
```

**Critical insight**: Always start footer detection **after line 100** to avoid false positives from book titles that contain words like "End of" in the actual narrative. The boilerplate text is **not marked with specific HTML tags or classes**—it's simply part of the body text, requiring pure text-based detection.

### Boilerplate variations by era

**Older books** (pre-2000s): Use `*END THE SMALL PRINT!` markers with version numbers
**Newer books** (2000s+): Use `*** START OF` and `*** END OF` with asterisks
**Very old HTML**: May have minimal or no visible boilerplate in the HTML body

Your script should handle **all marker variations** using case-insensitive matching and try multiple patterns before falling back to heuristics (skip first 50-100 lines, last 50 lines).

## HTML structure patterns for chapters and sections

### Chapter identification approaches

Project Gutenberg uses **heading tags** (h1, h2, h3) for structural markup, but the specific patterns vary:

**Common heading patterns**:
- `<h1>` - Reserved for book title
- `<h2>` - Most common for chapter headings 
- `<h3>` - Sometimes used for chapter subdivisions

**Typical chapter markup**:
```html
<h2>Chapter I</h2>
<h2>CHAPTER II</h2>
<h2 id="chapter_01">Chapter 1</h2>
```

**Finding chapters programmatically**:
```python
from bs4 import BeautifulSoup
import re

soup = BeautifulSoup(html_content, 'html.parser')

# Find all heading tags that likely represent chapters
chapter_headers = soup.find_all(
    ['h1', 'h2', 'h3'], 
    string=re.compile(r'chapter', re.IGNORECASE)
)

# Alternative: find by ID patterns
chapter_divs = soup.find_all('div', id=re.compile(r'chapter', re.IGNORECASE))
```

### Paragraph and content structure

**Paragraphs**: Almost universally marked with simple `<p>` tags without classes:
```html
<p>Paragraph content here.</p>
```

**No complex div structures**: Unlike modern web content, Project Gutenberg HTML is deliberately simple. You'll rarely find nested divs with elaborate class hierarchies. Most books are just sequences of `<p>`, `<h2>`, and `<br>` tags.

**Line breaks**: Poetry and verse use `<br>` tags for line breaks within paragraphs:
```html
<p>
First line of poetry<br>
Second line of poetry<br>
</p>
```

**Indentation**: Uses `&nbsp;` entities (non-breaking spaces) rather than CSS, especially in poetry:
```html
<p>&nbsp;&nbsp;&nbsp;&nbsp;Indented line</p>
```

### Front matter and back matter

Project Gutenberg doesn't use **standardized classes** for front matter (preface, introduction) or back matter (appendices). These sections typically appear as:

```html
<h2>Preface</h2>
<p>Content...</p>

<h2>Introduction</h2>
<p>Content...</p>
```

Your script should **parse heading text** to identify these sections by matching against common keywords: "Preface", "Introduction", "Forward", "Appendix", "Notes", "Index".

### Table of contents patterns

When present, tables of contents often use:
```html
<div class="toc">
  <ul>
    <li><a href="#CHAPTER_I">Chapter I</a></li>
    <li><a href="#CHAPTER_II">Chapter II</a></li>
  </ul>
</div>
```

However, **TOC markup is highly inconsistent**. Some books use simple lists with `<br>` tags, others use HTML tables, and many have no HTML TOC at all.

### Old vs. new digitization differences

**Older HTML files** (pre-2005):
- Very minimal markup
- Often lack meta tags entirely
- Simpler structure with just `<p>` and `<h2>` tags
- May use ISO-8859-1 character encoding instead of UTF-8
- Often start directly with chapter content

**Newer HTML files** (post-2010):
- More sophisticated CSS styling
- Include Dublin Core metadata in `<head>`
- Use UTF-8 encoding consistently
- Better structured with semantic HTML5 elements occasionally
- Include linked stylesheets more frequently

**Key recommendation**: Design your script to handle **minimal HTML structure** as the baseline. Any additional structure you find in newer books is a bonus, not something to rely on.

## Image handling and URL patterns

### Cover image access (highly predictable)

Project Gutenberg uses a **completely standardized URL pattern** for cover images:

```python
def get_cover_image_url(book_id):
    """Get cover image URL for any Gutenberg book."""
    return f"https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.cover.medium.jpg"

# Example: Book #1342 (Pride and Prejudice)
# https://www.gutenberg.org/cache/epub/1342/pg1342.cover.medium.jpg
```

These are **auto-generated cover images** stored in the `/cache/epub/` directory. They're always JPEG format, typically 300-400px wide, and available for nearly all books.

### Interior illustrations and images

Images embedded in HTML books use **relative paths** in an `images/` subdirectory:

```html
<img src="images/cover.jpg" alt="Cover">
<img src="images/image001.jpg" alt="Description">
<img src="images/frontispiece.png" alt="Frontispiece">
```

**Directory structure for HTML books**:
```
/files/[ID]/[ID]-h/
├── [ID]-h.htm          (main HTML file)
├── images/             (all images subdirectory)
│   ├── cover.jpg
│   ├── image001.jpg
│   ├── image002.png
│   └── illustration.gif
```

**Image file patterns**:
- Sequential numbering: `image001.jpg`, `image002.jpg`, `image003.png`
- Descriptive names: `alice-falling.jpg`, `caterpillar.png`
- Cover images: `cover.jpg`, `cover.png`, `frontcover.jpg`

### Downloading images programmatically

```python
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def download_book_images(book_id, html_content):
    """Download all images referenced in a Gutenberg HTML book."""
    soup = BeautifulSoup(html_content, 'html.parser')
    base_url = f"https://www.gutenberg.org/files/{book_id}/{book_id}-h/"
    
    images = []
    for img in soup.find_all('img'):
        img_src = img.get('src')
        if img_src:
            # Build full URL from relative path
            img_url = urljoin(base_url, img_src)
            images.append({
                'url': img_url,
                'filename': img_src.split('/')[-1],
                'alt': img.get('alt', '')
            })
    
    return images
```

### Image specifications and formats

**Formats**: JPEG, PNG, and occasionally GIF
**Sizes**: 
- Line drawings/decorative: 20-60 KB
- Standard illustrations: 40-100 KB  
- Color plates: up to 200 KB
- Width: typically 600px maximum for browser display

**Important**: All images must have `alt` attributes for accessibility. Project Gutenberg follows W3C accessibility guidelines.

### Cover vs. interior image differences

**Generated cover images** (`/cache/epub/` directory):
- Standardized URL pattern
- Always JPEG, medium size
- Often created by transcribers, not original
- Used for catalog display and downloads

**Original interior illustrations** (`images/` subdirectory):
- Relative paths in HTML
- Multiple formats (PNG for line art, JPEG for photos)
- Original artwork from source book
- Integral to reading experience

## Metadata extraction strategies

### Dublin Core metadata in HTML head

When present, Project Gutenberg uses **Dublin Core metadata tags** following this pattern:

```html
<head profile="http://dublincore.org/specifications/dublin-core/dc-html/">
  <link rel="schema.DC" href="http://purl.org/dc/elements/1.1/" />
  
  <meta name="DC.Title" content="Pride and Prejudice" />
  <meta name="DC.Creator" content="Austen, Jane" />
  <meta name="DC.Language" content="en" />
  <meta name="DC.Date" content="1813" />
  <meta name="DC.Publisher" content="Project Gutenberg" />
  <meta name="DC.Rights" content="Public domain in the USA" />
  <meta name="DC.Subject" content="Fiction" />
  <meta name="DC.Identifier" content="http://www.gutenberg.org/ebooks/1342" />
</head>
```

**Complete list of Dublin Core elements**:
1. DC.Title - Book title
2. DC.Creator - Author (format: "LastName, FirstName")
3. DC.Subject - Genre/topic keywords (can repeat)
4. DC.Description - Summary or abstract
5. DC.Publisher - Usually "Project Gutenberg"
6. DC.Contributor - Translators, illustrators
7. DC.Date - Publication or creation date
8. DC.Type - Resource type (e.g., "Text")
9. DC.Format - MIME type ("text/html; charset=utf-8")
10. DC.Identifier - Unique ID (book number or URL)
11. DC.Source - Original source info
12. DC.Language - ISO 639 code ("en", "fr", "de")
13. DC.Relation - Related resources
14. DC.Coverage - Spatial/temporal coverage
15. DC.Rights - Copyright status

### Extracting metadata with fallbacks

**Critical insight**: Dublin Core meta tags are **inconsistent across the collection**. Older books (pre-2005) often lack them entirely. Your script must implement **multiple extraction strategies**:

```python
class GutenbergMetadataExtractor:
    def extract_from_meta_tags(self, soup):
        """Extract from Dublin Core meta tags."""
        metadata = {}
        
        # Case-insensitive search for DC tags
        title = soup.find('meta', {'name': re.compile(r'DC\.Title', re.I)})
        if title:
            metadata['title'] = title['content']
        
        # Handle multiple authors
        authors = soup.find_all('meta', {'name': re.compile(r'DC\.Creator', re.I)})
        metadata['authors'] = [tag['content'] for tag in authors]
        
        # Language
        lang = soup.find('meta', {'name': re.compile(r'DC\.Language', re.I)})
        if lang:
            metadata['language'] = lang['content']
        
        # Multiple subjects
        subjects = soup.find_all('meta', {'name': re.compile(r'DC\.Subject', re.I)})
        metadata['subjects'] = [tag['content'] for tag in subjects]
        
        return metadata
    
    def extract_from_body_text(self, text):
        """Fallback: extract from PG header text."""
        metadata = {}
        
        # Title pattern
        title_match = re.search(r'Title:\s*(.+?)(?:\n|Author:)', text)
        if title_match:
            metadata['title'] = title_match.group(1).strip()
        
        # Author pattern
        author_match = re.search(r'Author:\s*(.+?)(?:\n|\r)', text)
        if author_match:
            metadata['authors'] = [author_match.group(1).strip()]
        
        # Language pattern
        lang_match = re.search(r'Language:\s*(\w+)', text)
        if lang_match:
            metadata['language'] = lang_match.group(1)
        
        # Book ID
        ebook_match = re.search(r'\[EBook #(\d+)\]', text)
        if ebook_match:
            metadata['ebook_id'] = ebook_match.group(1)
        
        # Release date
        date_match = re.search(r'Release Date:\s*(.+?)\s*\[', text)
        if date_match:
            metadata['release_date'] = date_match.group(1).strip()
        
        return metadata
```

### Metadata in body text headers

All Project Gutenberg books include **plain text metadata** in the header boilerplate:

```
Title: Pride and Prejudice
Author: Jane Austen
Release Date: June 1998 [EBook #1342]
Language: English
```

This text-based metadata is **more reliable than HTML meta tags** because it appears in virtually every book. Parse it using regex before falling back to Dublin Core tags.

### Alternative metadata source: RDF files

For comprehensive metadata, Project Gutenberg provides **RDF/XML files**:

```python
def get_rdf_metadata_url(book_id):
    return f"https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.rdf"
```

These XML files contain complete metadata including:
- Author birth/death dates
- Full subject classifications (Library of Congress)
- All available formats
- Comprehensive publication info

**Recommendation**: For a robust extraction tool, fetch the RDF file as your primary metadata source, then fall back to HTML parsing.

### Extracting book structure information

```python
def extract_structure(soup):
    """Extract chapter count and section types."""
    structure = {}
    
    # Count chapters by finding chapter headings
    chapter_pattern = re.compile(r'chapter', re.IGNORECASE)
    chapters = soup.find_all(['h1', 'h2', 'h3'], string=chapter_pattern)
    
    structure['chapter_count'] = len(chapters)
    structure['chapter_titles'] = [h.get_text().strip() for h in chapters]
    
    # Check for table of contents
    toc = soup.find(['div', 'nav'], class_=re.compile(r'toc', re.I))
    structure['has_toc'] = toc is not None
    
    # Identify section types by class names
    sections = soup.find_all(['section', 'div'], class_=True)
    structure['section_types'] = list(set([
        s.get('class')[0] for s in sections if s.get('class')
    ]))
    
    return structure
```

**Reality check**: Chapter counts must be **inferred from heading tags** because there's no standardized way to encode this in metadata. Pattern matching on heading text is your only option.

## General patterns for maximum compatibility

### The simplicity principle

Project Gutenberg HTML follows a **minimalist philosophy**:
- Valid W3C HTML 4.01 or HTML5
- Simple, flat structure (minimal nesting)
- Semantic markup (`<h2>` for chapters, `<p>` for paragraphs)
- No JavaScript, no frames, no pop-ups
- Accessible at all font sizes
- Readable even without CSS

**This simplicity is your advantage**. You don't need complex DOM traversal—simple BeautifulSoup selectors and text parsing will handle 95% of books.

### Character encoding variations

**Modern books**: UTF-8 (`charset=utf-8`)
**Older books**: ISO-8859-1 (Latin-1) or other extended ASCII

Always check the meta charset declaration:
```html
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
```

Your Python script should:
```python
def detect_encoding(html_bytes):
    """Detect encoding from meta tag or BOM."""
    # Try to decode as UTF-8 first
    try:
        text = html_bytes.decode('utf-8')
        return text, 'utf-8'
    except UnicodeDecodeError:
        # Fall back to ISO-8859-1
        text = html_bytes.decode('iso-8859-1')
        return text, 'iso-8859-1'
```

### URL patterns for accessing books

**Standard HTML URL pattern**:
```
https://www.gutenberg.org/files/[ID]/[ID]-h/[ID]-h.htm
```

Examples:
- Pride and Prejudice: `https://www.gutenberg.org/files/1342/1342-h/1342-h.htm`
- Moby Dick: `https://www.gutenberg.org/files/2701/2701-h/2701-h.htm`
- Frankenstein: `https://www.gutenberg.org/files/84/84-h/84-h.htm`

**Alternative directory structure** (newer books):
```
/cache/epub/[ID]/pg[ID]-images.html
```

Your script should try the `/files/` URL first, then fall back to `/cache/epub/` if needed.

## Recommended Python extraction workflow

Based on all these patterns, here's the optimal extraction strategy:

### 1. Fetch and clean

```python
def extract_gutenberg_book(book_id):
    # Fetch HTML
    url = f"https://www.gutenberg.org/files/{book_id}/{book_id}-h/{book_id}-h.htm"
    response = requests.get(url)
    html_bytes = response.content
    
    # Detect encoding
    html_text, encoding = detect_encoding(html_bytes)
    
    # Remove boilerplate first
    clean_text = remove_gutenberg_boilerplate(html_text)
    
    # Parse with BeautifulSoup
    soup = BeautifulSoup(clean_text, 'html.parser')
    
    return soup
```

### 2. Extract metadata (multiple sources)

```python
    # Try RDF metadata first (most reliable)
    rdf_metadata = fetch_rdf_metadata(book_id)
    
    # Fall back to HTML meta tags
    html_metadata = extract_from_meta_tags(soup)
    
    # Fall back to body text parsing
    text_metadata = extract_from_body_text(html_text)
    
    # Merge with priority: RDF > HTML tags > body text
    metadata = {**text_metadata, **html_metadata, **rdf_metadata}
```

### 3. Extract structure and content

```python
    # Find chapters
    chapters = extract_chapters(soup)
    
    # Extract structure info
    structure = extract_structure(soup)
    
    # Get clean text for each chapter
    chapter_texts = []
    for chapter in chapters:
        text = chapter.get_text(strip=True)
        chapter_texts.append(text)
```

### 4. Handle images

```python
    # Download cover image
    cover_url = get_cover_image_url(book_id)
    download_image(cover_url, 'cover.jpg')
    
    # Find and download interior images
    images = download_book_images(book_id, html_text)
```

### 5. Generate outputs

```python
    # Create markdown with front matter
    markdown = generate_markdown(metadata, chapter_texts)
    
    # Generate YAML metadata file
    yaml_output = generate_yaml(metadata, structure)
    
    # Save everything
    save_outputs(markdown, yaml_output, images)
```

## Edge cases and handling strategies

### Books without clear chapter divisions

Some older Project Gutenberg books have **no chapter headings** or use inconsistent formatting. Strategy:
- Search for numbered sections: "I.", "II.", "1.", "2."
- Look for decorative separators: "* * *"
- Fall back to paragraph count thresholds (split every N paragraphs)

### Books with complex structures

Plays, poetry collections, and reference works don't follow novel structure. Strategy:
- Detect book type from metadata subjects
- Use heading hierarchy (h1→h2→h3) as generic structure
- Preserve formatting like line breaks for poetry

### Multi-volume works

Some books span multiple HTML files. Strategy:
- Check for links to adjacent files (next chapter, previous chapter)
- Look for file patterns: `book1.htm`, `book2.htm`
- Process each file separately, then combine

### Missing metadata

When metadata extraction fails completely:
- Use book ID as fallback identifier  
- Parse title from first `<h1>` tag
- Mark fields as "Unknown" rather than crashing

## Validation and testing recommendations

To ensure your script works across the widest range of books:

**Test with diverse sample set**:
- Old books: #84 (Frankenstein, 1818), #1342 (Pride and Prejudice, 1813)
- Modern additions: #64317 (Great Gatsby, 2021 digitization)
- Illustrated books: #11 (Alice in Wonderland), #28885 (Alice with Rackham illustrations)
- Non-fiction: Various reference works and historical texts
- Different languages: Books in French, German, Spanish

**Verify extraction quality**:
- Boilerplate removal: Check first/last paragraphs are actual content
- Chapter detection: Manually count chapters in sample books
- Image downloads: Verify all images are retrieved
- Metadata accuracy: Compare with Project Gutenberg's website
- Character encoding: Test books with accented characters

**Performance considerations**:
- Cache RDF metadata locally to reduce requests
- Use connection pooling for bulk downloads
- Respect robots.txt (2-second delays between requests)
- Handle timeouts and network errors gracefully

## Final recommendations for production code

**Priority order for reliability**:
1. **Text-based boilerplate markers** - most consistent across all eras
2. **RDF metadata files** - authoritative source for bibliographic data
3. **Cover image URL pattern** - 100% predictable
4. **Heading tag parsing** - reliable for chapter detection
5. **Dublin Core meta tags** - use when available, don't depend on them

**Avoid depending on**:
- Complex div structures with classes - highly inconsistent
- CSS selectors for content - older books have minimal styling  
- Standardized section markers - front/back matter varies wildly
- JavaScript or dynamic content - never present in Gutenberg books

**Design philosophy**: Build for the **lowest common denominator** (simple HTML from 1990s) and treat anything more sophisticated as a bonus. Your script will work on 95% of books if you follow text-based patterns and simple HTML parsing. Trying to handle every edge case perfectly will lead to fragile code that works great on 100 books but fails on the other 59,900.