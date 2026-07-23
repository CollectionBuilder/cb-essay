# CB-Essay

**Multi-modal essay writing meets digital collections**

Built on CollectionBuilder, CB-Essay combines long-form narrative writing with items from your digital collection. Create annotated editions, scholarly essays with integrated primary sources, or multimodal monographs that blend text and collection items seamlessly.

[**View Demo Site**](#) <!-- Add your demo URL here -->

---

## What is CB-Essay?

CB-Essay is a Jekyll-based static site generator that extends [CollectionBuilder-CSV](https://github.com/CollectionBuilder/collectionbuilder-csv) to support essay and monograph publishing alongside digital collection features. Write in Markdown, integrate collection items with simple includes, and publish beautiful, accessible scholarly work.

**Perfect for:**
- Digital humanities projects and digital editions
- Annotated texts with primary source integration
- Scholarly essays that incorporate archival materials
- Multimodal monographs combining narrative and collection items
- Publishing public domain texts with scholarly apparatus

---

## Quick Start

1. **Use this template** - Click "Use this template" to create your repository
2. **Add your essays** - Create Markdown files in the `_essay/` folder with simple front matter:
   ```yaml
   ---
   title: Your Essay Title
   order: 1
   ---
   ```
3. **Deploy** - Go to Settings → Pages, select "GitHub Actions" as source, configure the Jekyll workflow (change ruby-version to 3.4 on line 40), and commit

Essays appear in sequential order based on the `order` field, with automatic prev/next navigation.

---

## Key Features

### Essay Writing
- Sequential essay navigation with prev/next buttons
- Independent navigation flags for a single linear essay or a book-style multi-chapter monograph
- Support for long-form scholarship with chapter-like organization

### CollectionBuilder Integration
- All standard CB-CSV features: Browse, Map, Timeline, Subjects, Data downloads
- Seamless integration of collection items within essays
- Dual-collection workflow: essays + metadata-driven object pages

### Essay-Specific Includes
- **Blockquotes** - Styled quotations with attribution
- **Asides** - Margin notes with optional collection items
- **Image galleries** - Inline image displays
- **Maps** - Embedded mini-maps with custom coordinates
- **Section transitions** - Scrollama-powered visual breaks

### 📚 Bonus: Project Gutenberg Extractor

Extract **60,000+ public domain books** from Project Gutenberg as ready-to-publish essays using our GitHub Action workflow:

1. Navigate to **Actions** tab → **"Extract Gutenberg Book"**
2. Enter a Project Gutenberg book ID:
   - Frankenstein: `84`
   - Pride and Prejudice: `1342`
   - The Great Gatsby: `64317`
   - [Find more books](https://www.gutenberg.org/)
3. Click "Run workflow" - the book extracts directly into `_essay/` folder

The script automatically:
- Downloads and cleans Gutenberg HTML
- Removes boilerplate text
- Splits into chapter files with proper front matter
- Extracts metadata to `_data/book.yml`
- Stores cover image URLs

See it in action: [Extracting a Book from Project Gutenberg](_essay/035-gutenberg-extraction.md) (end-user walkthrough) or [the technical extraction reference](docs/cb-essay/gutenberg-extraction.md) (maintainer-level).

---

## Learn By Example

The demo site is **self-documenting** - each essay teaches you how to use CB-Essay while demonstrating the features:

1. **Welcome to CB-Essay** - Overview and introduction
2. **CB-Essay in the Wild** - Live example sites
3. **Get Started** - Your first essay walkthrough
4. **Extracting a Book from Project Gutenberg** - Publish a public domain book in minutes
5. **Essay Writing Features** - All includes with copy-paste examples
6. **Scroll-Based Features** - Scrollytelling overview, with dedicated Scrolly Media and Scrolly Map galleries for deep reference
7. **Publishing, Printing & Reading** - Print, search, deployment, and sharing

**Copy and replace:** Every feature you see can be copied directly into your own essays. Just replace the demo content with yours.

---

## Documentation

- [**Essay Writing Guide**](docs/cb-essay/essay-writing.md) - Front matter, navigation, workflow
- [**Essay Features Reference**](docs/cb-essay/essay-features.md) - Complete guide to all essay includes
- [**Gutenberg Extraction**](docs/cb-essay/gutenberg-extraction.md) - Detailed extraction workflow
- [**Theme Options**](docs/cb-essay/theme-options.md) - Color theme, fonts, homepage layout, and navigation flags
- [**Accessibility**](docs/cb-essay/accessibility.md) - WCAG 2.1 out of the box, and testing after you customize
- [**Working with AI**](HUMANS.md) - Prompting and reviewing AI coding assistants (`AGENTS.md` carries the rules)
- [**CollectionBuilder Docs**](docs/index.md) - Full CB-CSV documentation

---

## Technical Overview

CB-Essay is built on:
- **Jekyll** - Static site generator
- **CollectionBuilder-CSV** - Digital collection framework
- **Bootstrap 5** - Responsive design
- **Custom essay collection** - Sequential navigation system

Requirements:
- Ruby and Jekyll
- Git and GitHub account
- Basic Markdown knowledge

---

## Credits & License

**CB-Essay** is developed by the [Center for Digital Inquiry and Learning (CDIL)](https://cdil.lib.uidaho.edu/) at the University of Idaho Library.

Built on [CollectionBuilder-CSV](https://github.com/CollectionBuilder/collectionbuilder-csv).

- **Code:** MIT License
- **Documentation:** CC-BY

---

## Get Started

Ready to create your essay?

1. [Use this template](../../generate)
2. Check out the [Getting Started Guide](docs/cb-essay/essay-writing.md)
3. Explore the [demo site](#) to see features in action

Questions? See our [documentation](docs/cb-essay/) or open an issue.
