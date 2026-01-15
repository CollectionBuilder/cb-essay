# CB-Essay Documentation

Welcome to CB-Essay! This guide will help you create multimodal essays and monographs that integrate digital collection items with long-form narrative writing.

## What is CB-Essay?

CB-Essay is a Jekyll-based static site generator that extends [CollectionBuilder-CSV](https://github.com/CollectionBuilder/collectionbuilder-csv) to support essay and monograph publishing. Write in Markdown, integrate collection items with simple includes, and publish beautiful, accessible scholarly work.

**Perfect for:**
- Digital humanities projects and digital editions
- Annotated texts with primary source integration
- Scholarly essays that incorporate archival materials
- Multimodal monographs
- Publishing public domain texts with scholarly apparatus

## Quick Links

### Getting Started
- **[Essay Writing Guide](essay-writing.md)** - Learn how to create and organize essays
- **[Getting Started Essay](../../_essay/02-getting-started.md)** - Step-by-step walkthrough

### Features & Customization
- **[Essay Features Reference](essay-features.md)** - Complete guide to blockquotes, asides, galleries, maps, and more
- **[Theme Options](theme-options.md)** - Choose between essay and monograph themes, customize appearance

### Advanced Workflows
- **[Gutenberg Extraction](gutenberg-extraction.md)** - Import 60,000+ public domain books from Project Gutenberg

### Example Essays
The demo site includes self-documenting essays that teach while demonstrating features:
1. [Welcome to CB-Essay](../../_essay/01-welcome.md) - Overview and examples
2. [Getting Started](../../_essay/02-getting-started.md) - Setup walkthrough
3. [Essay Features](../../_essay/03-essay-features.md) - All features with copy-paste examples
4. [Collection Integration](../../_essay/04-collection-integration.md) - Blending essays with collection items

## Core Concepts

### The Dual-Collection Model

CB-Essay manages two parallel collections:

1. **Essay Collection** (`_essay/` folder)
   - Your narrative content as Markdown files
   - Sequential navigation with prev/next buttons
   - Controlled by `order` field in front matter

2. **Object Collection** (CSV metadata)
   - Digital collection items
   - Metadata-driven pages
   - Standard CollectionBuilder features (Browse, Map, Timeline)

These collections work together - reference collection items within your essays using simple includes.

### Essay Front Matter

Every essay file needs YAML front matter:

```yaml
---
title: Your Essay Title
order: 1
byline: Your Name (optional)
---
```

Essays display in sequential order based on the `order` value.

### Theme Options

Choose your presentation style in `_data/theme.yml`:

- **`essay`** - Linear reading, simple navigation
- **`monograph`** - Table of contents on homepage, book-like structure

## Essential Features

### Essay-Specific Includes

- **Blockquotes** - Styled quotations with attribution
- **Asides** - Margin notes with optional collection items
- **Image Galleries** - Display multiple items
- **Mini Maps** - Embed maps at specific coordinates
- **Section Transitions** - Visual breaks with scroll effects

See the [Essay Features Reference](essay-features.md) for complete documentation.

### CollectionBuilder Integration

All standard CB features work in essays:
- Item cards and images
- Timelines and maps
- Subject clouds
- Search and browse

Learn more in [Collection Integration](../../_essay/04-collection-integration.md).

## Workflow Options

CB-Essay supports multiple editing workflows:

### Browser-Based (No Installation)
- **GitHub.com** - Edit files directly in your browser
- **GitHub.dev** - Press `.` for VS Code in browser
- **Codespaces** - Full cloud development environment

### Local Development
Follow the [CollectionBuilder-CSV walkthrough](https://collectionbuilder.github.io/cb-docs/docs/walkthroughs/csv-walkthrough/) for local setup with Git and Jekyll.

**Most users work entirely in their browser** using GitHub.com and the Gutenberg extractor.

## Project Gutenberg Integration

Extract 60,000+ public domain books as ready-to-publish essays:

1. Go to **Actions** tab in your repository
2. Click **"Extract Gutenberg Book"**
3. Enter a book ID (e.g., `84` for Frankenstein)
4. Run workflow

The book extracts directly into your `_essay/` folder with proper formatting!

See [Gutenberg Extraction Guide](gutenberg-extraction.md) for details.

## Common Tasks

### Create Your First Essay

1. Create a file in `_essay/` (e.g., `my-essay.md`)
2. Add front matter with title and order
3. Write content in Markdown
4. Commit and push to GitHub
5. GitHub Pages builds automatically

See [Essay Writing Guide](essay-writing.md) for complete workflow.

### Add a Blockquote

```liquid
{% raw %}{% include essay/feature/blockquote.html
   quote="Your quotation here"
   speaker="Author Name" %}{% endraw %}
```

### Add a Margin Note

```liquid
{% raw %}{% include essay/feature/aside.html
   text="Your margin note" %}{% endraw %}
```

### Reference a Collection Item

```liquid
{% raw %}{% include essay/feature/aside.html
   objectid="demo_001"
   text="Context about this item" %}{% endraw %}
```

See [Essay Features Reference](essay-features.md) for all options.

## Configuration Files

### `_config.yml`
- Site title, author, description
- Essay collection settings
- Metadata source

Includes helpful comments explaining essay-specific options.

### `_data/theme.yml`
- Theme choice (essay vs monograph)
- Typography and colors
- Homepage image settings

Includes detailed comments for each option.

### `_data/config-nav.csv`
- Navigation menu structure
- Dropdown organization

## Support & Resources

### Documentation
- [Essay Writing Guide](essay-writing.md)
- [Essay Features Reference](essay-features.md)
- [Theme Options](theme-options.md)
- [Gutenberg Extraction](gutenberg-extraction.md)
- [CollectionBuilder Docs](https://collectionbuilder.github.io/cb-docs/)

### Example Projects
- [Tender Spaces](https://cdil.lib.uidaho.edu/tender-spaces/) - Heavily customized multimodal essay
- [Frankenstein](https://dcnb.github.io/frankenstein) - Monograph theme example *(coming soon)*
- [Wreck of the Deutschland](https://dcnb.github.io/wreck-of-the-deutschland) - Essay theme with poetry *(coming soon)*

### Get Help
- [GitHub Issues](https://github.com/CollectionBuilder/cb-essay/issues)
- [CollectionBuilder Community](https://collectionbuilder.github.io/community.html)

## Copy & Replace Philosophy

CB-Essay is designed for easy adoption:

1. Find a feature you like in the demo essays
2. Copy the include code
3. Paste into your essay
4. Replace the content with yours

No need to understand technical details - just copy and adapt!

---

**Ready to start?** Check out the [Getting Started Essay](../../_essay/02-getting-started.md) or create your first essay file in `_essay/`.
