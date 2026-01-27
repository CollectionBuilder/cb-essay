---
layout: docs
title: CB-Essay Documentation
permalink: /docs.html
---

## Overview {#overview}

**CB-Essay** is a Jekyll-based framework that extends [CollectionBuilder-CSV](https://collectionbuilder.github.io/cb-docs/) to combine long-form essay writing with digital collection features. Write in Markdown, integrate primary sources, and publish multimodal scholarly work on the web for free.

### What Makes CB-Essay Different?

Traditional digital publishing treats essays and collections separately. CB-Essay unifies them through a **dual-collection model**:

1. **Essay Collection** (`_essay/` directory) - Your narrative content as Markdown files with sequential navigation
2. **Object Collection** (CSV metadata) - Digital items you can reference within essays using simple includes

This allows you to **write with, on, and for the web** - integrating archival materials, images, maps, and multimedia directly into your scholarly narratives.

### Perfect For

- Digital humanists creating annotated editions
- Historians presenting narratives alongside primary sources
- Educators building interactive course readers
- Archivists providing context around collections
- Writers publishing long-form digital scholarship

---

## Quick Start {#quick-start}

### 1. Get the Template

Visit [github.com/CollectionBuilder/cb-essay](https://github.com/CollectionBuilder/cb-essay) and click **"Use this template"** → **"Create a new repository"**.

### 2. Enable GitHub Pages

1. Go to **Settings** → **Pages**
2. Under **Source**, select **GitHub Actions**
3. GitHub will display a **Jekyll** workflow option - click **Configure**
4. In the workflow file that opens, find line 40 where it says `ruby-version: '3.1'`
5. Change the version from `3.1` to `3.4`
6. Click **Commit changes**

Your site will be live at `https://username.github.io/repository-name` in a few minutes.

### 3. Create Your First Essay

1. Navigate to the `_essay/` folder in your repository
2. Click **"Add file"** → **"Create new file"**
3. Name it `my-first-essay.md`
4. Add this content:

```yaml
---
title: My First Essay
order: 1
---

## Introduction

This is my first essay using CB-Essay! I can write in **Markdown** and include [links](https://example.com).

### Adding Features

I can add blockquotes:

{% raw %}{% include essay/feature/blockquote.html
   quote="Knowledge comes, but wisdom lingers"
   speaker="Alfred Lord Tennyson" %}{% endraw %}

And margin notes:{% raw %}{% include essay/feature/aside.html text="This is a margin note!" %}{% endraw %}
```

5. **Commit changes** and wait for GitHub Pages to rebuild (2-3 minutes)

That's it! Your essay is live.

---

## Essay Writing {#essay-writing}

### File Structure

All essays live in the `_essay/` directory:

```
your-project/
├── _essay/
│   ├── 01-introduction.md
│   ├── 02-chapter-one.md
│   └── 03-conclusion.md
```

### Required Front Matter

Every essay needs YAML front matter:

```yaml
---
title: Your Essay Title
order: 1
---
```

- **`title`**: Appears in navigation and page header
- **`order`**: Controls display sequence (1, 2, 3...)

### Optional Front Matter

```yaml
---
title: Of Thumbs
order: 1
byline: Michel de Montaigne
featured-image: /assets/img/chapter-image.jpg
---
```

- **`byline`**: Author attribution
- **`featured-image`**: Header image for this essay

### Navigation

Essays automatically get prev/next navigation based on `order`. Use gaps (1, 10, 20, 30) to allow easy insertion later.

### Workflow

**Browser-based (recommended):**
1. Edit directly on GitHub.com
2. Use GitHub.dev (press `.` in your repository)
3. Use Codespaces for full development environment

**Local development:**
Follow the [CollectionBuilder-CSV setup guide](https://collectionbuilder.github.io/cb-docs/docs/walkthroughs/csv-walkthrough/) for local Jekyll installation.

For detailed guidance, see [Essay Writing Guide](https://github.com/CollectionBuilder/cb-essay/blob/main/docs/cb-essay/essay-writing.md).

---

## Essay Features {#essay-features}

CB-Essay provides specialized includes for scholarly writing. **Copy the examples below directly into your essays.**

### Blockquotes

Styled quotations with attribution and source links.

**Basic blockquote:**
```liquid
{% raw %}{% include essay/feature/blockquote.html
   quote="Knowledge comes, but wisdom lingers"
   speaker="Alfred Lord Tennyson" %}{% endraw %}
```

**With source:**
```liquid
{% raw %}{% include essay/feature/blockquote.html
   quote="It is a truth universally acknowledged..."
   speaker="Jane Austen"
   source="Pride and Prejudice" %}{% endraw %}
```

**Large centered quote:**
```liquid
{% raw %}{% include essay/feature/blockquote.html
   quote="The only way out is through"
   size="xl"
   align="center" %}{% endraw %}
```

**Parameters:**
- `quote` - Quote text (required)
- `speaker` - Person quoted
- `source` - Title of source work
- `source-link` - URL to source
- `size` - `sm`, `md`, `lg`, `xl`, `xxl`
- `align` - `left`, `center`, `right`

### Asides (Margin Notes)

Margin notes appear beside text on desktop, inline on mobile.

**Text-only aside:**
```liquid
{% raw %}Here's text with a margin note.{% include essay/feature/aside.html text="This is a margin note!" %} Text continues.{% endraw %}
```

**Aside with collection item:**
```liquid
{% raw %}{% include essay/feature/aside.html
   objectid="demo_001"
   text="Context about this item" %}{% endraw %}
```

**Parameters:**
- `text` - Margin note text (supports Markdown)
- `objectid` - Collection item ID from your metadata CSV
- `caption` - Override item title
- `height` - Max height (default: 205px)
- `gallery` - Link to viewer (`true`) or item page (`false`)

### Image Galleries

Display multiple collection items:

```liquid
{% raw %}{% include feature/gallery.html
   heading="Items after 1900"
   filter="item.format contains 'image'" %}{% endraw %}
```

### Mini Maps

Embed maps at specific coordinates:

```liquid
{% raw %}{% include feature/mini-map.html
   latitude="46.727485"
   longitude="-117.014185"
   zoom="10" %}{% endraw %}
```

**Parameters:**
- `latitude` - Center latitude (required)
- `longitude` - Center longitude (required)
- `zoom` - Zoom level 1-18 (default: 10)
- `height` - Map height (CSS value)

### Section Breaks

Create visual breaks with scroll transitions:

```liquid
{% raw %}{% include essay/new-section.html %}

## New Section Title

Content continues...{% endraw %}
```

### Complete Feature Reference

For all parameters and advanced usage, see:
- [Essay Features Reference](https://github.com/CollectionBuilder/cb-essay/blob/main/docs/cb-essay/essay-features.md)
- [Demo essays](_essay/) with live examples

---

## Collection Integration {#collection-integration}

### Using Collection Items

Reference items from your metadata CSV using their `objectid`:

```liquid
{% raw %}{% include essay/feature/aside.html
   objectid="demo_001"
   text="This manuscript shows early revisions" %}{% endraw %}
```

### Metadata Requirements

Items must exist in your `_data/[metadata].csv` file with:
- `objectid` - Unique identifier
- `title` - Item title
- `format` - Item type (image, pdf, video, etc.)
- `image_small`, `image_thumb` - For images

### CollectionBuilder Features in Essays

All standard CollectionBuilder includes work in essays:

**Item card:**
```liquid
{% raw %}{% include feature/item-card.html objectid="demo_001" %}{% endraw %}
```

**Timeline:**
```liquid
{% raw %}{% include feature/timeline.html %}{% endraw %}
```

**Subject cloud:**
```liquid
{% raw %}{% include feature/cloud.html fields="subject" %}{% endraw %}
```

For complete CollectionBuilder documentation, see [CollectionBuilder Docs](https://collectionbuilder.github.io/cb-docs/).

---

## Theme Options {#theme-options}

CB-Essay supports two presentation themes set in `_data/theme.yml`:

### Essay Theme

```yaml
base-theme: essay
```

**Best for:** Traditional essays, article collections, linear narratives

**Features:**
- Clean homepage with "Read the Essay" button
- Linear reading flow
- Minimal navigation

### Monograph Theme

```yaml
base-theme: monograph
```

**Best for:** Multi-chapter books, edited volumes, reference works

**Features:**
- Table of contents on homepage
- Chapter-style navigation
- Book-like presentation
- Byline display in TOC

### Homepage Image Options

**Full image:**
```yaml
image-style: full-image
featured-image: /assets/img/banner.jpg
home-banner-image-position: center
```

**Half image:**
```yaml
image-style: half-image
featured-image: /assets/img/cover.jpg
```

**No image:**
```yaml
image-style: no-image
```

### Customization

**Colors and typography:**
```yaml
base-font-size: 1.3em
text-color: "#191919"
link-color: "#0d6efd"
base-font-family: Georgia
```

For complete theme documentation, see [Theme Options Guide](https://github.com/CollectionBuilder/cb-essay/blob/main/docs/cb-essay/theme-options.md).

---

## Configuration {#configuration}

### `_config.yml`

**Homepage cover page settings:**
```yaml
title: Your Essay Title
author: Your Name  # Displays as "by Your Name" on cover
tagline: A brief tagline  # Only shows if author is empty
description: Longer description for search engines
```

**Cover page display notes:**
- `title` always displays prominently on the cover page
- `author` appears as "by [Author Name]" beneath title
  - If provided, replaces the tagline on cover page
  - Use HTML for multi-line: `author: "Name<br>Edited by Editor"`
- `tagline` only displays if `author` field is empty
  - Can also use HTML for multi-line display

**Essay collection (already configured):**
```yaml
collections:
  essay:
    sort_by: order
    output: true
```

**Metadata source:**
```yaml
metadata: your-metadata-filename  # without .csv extension
```

### `_data/theme.yml`

**Theme selection:**
```yaml
base-theme: essay  # or monograph
image-style: full-image
featured-image: /assets/img/banner.jpg
```

**Typography:**
```yaml
base-font-size: 1.3em
base-font-family: Georgia
text-color: "#191919"
```

### `_data/config-nav.csv`

Controls navigation menu structure. Edit this CSV to customize your site's top navigation.

For standard CollectionBuilder configuration files (config-browse.csv, config-map.csv, etc.), see [CollectionBuilder Configuration Docs](https://collectionbuilder.github.io/cb-docs/docs/config/).

---

## Gutenberg Extractor {#gutenberg}

CB-Essay includes a GitHub Action to import **60,000+ public domain books** from Project Gutenberg directly into your `_essay/` folder.

### How to Use

1. Go to **Actions** tab in your GitHub repository
2. Click **"Extract Gutenberg Book"** workflow
3. Click **"Run workflow"**
4. Enter a book ID (e.g., `84` for Frankenstein, `1342` for Pride and Prejudice)
5. Click **"Run workflow"**

The book extracts as formatted Markdown files in `_essay/` with proper front matter and chapter organization.

### Finding Book IDs

1. Search [Project Gutenberg](https://www.gutenberg.org/)
2. Find the book ID in the URL: `https://www.gutenberg.org/ebooks/84` → ID is `84`

### What Gets Extracted

- Chapter-by-chapter Markdown files
- Metadata (title, author, publication info)
- Cover image (when available)
- Interior illustrations
- Proper front matter with sequential ordering

### After Extraction

1. Review the extracted files in `_essay/`
2. Adjust `order` values if needed
3. Add essay features (blockquotes, asides, etc.)
4. Customize theme in `_data/theme.yml`
5. Commit and push

For technical details, see [Gutenberg Extraction Guide](https://github.com/CollectionBuilder/cb-essay/blob/main/docs/cb-essay/gutenberg-extraction.md).

---

## Publishing {#publishing}

### GitHub Pages (Free)

1. Push changes to your main branch
2. GitHub Pages automatically rebuilds (2-3 minutes)
3. Site is live at `https://username.github.io/repository-name`

**Custom domain:**
1. Add `CNAME` file to repository root with your domain
2. Configure DNS with your domain provider
3. See [GitHub Pages custom domain docs](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site)

### Local Preview

```bash
bundle exec jekyll s
```

Visit `http://localhost:4000` to preview changes before pushing.

### Production Build

```bash
JEKYLL_ENV=production bundle exec jekyll build
```

Outputs to `_site/` directory with full meta tags and analytics.

For complete deployment options, see [CollectionBuilder Deploy Docs](https://collectionbuilder.github.io/cb-docs/docs/deploy/).

---

## CollectionBuilder Features {#collectionbuilder}

CB-Essay includes all standard CollectionBuilder pages and features:

### Built-in Pages

- **Browse** - Grid/list view of all items
- **Map** - Geographic visualization (for items with coordinates)
- **Timeline** - Chronological visualization (for items with dates)
- **Subjects** - Word cloud of subject terms
- **Data** - Downloadable metadata and visualizations

### Feature Includes

Available for use in essays:
- `item-card.html` - Display individual items
- `timeline.html` - Embed timelines
- `cloud.html` - Subject/location clouds
- `image.html` - Single images
- `pdf.html` - Embedded PDFs
- `video.html` - Embedded videos

### Metadata Configuration

Configure feature displays using CSV files in `_data/`:
- `config-browse.csv` - Browse page fields
- `config-metadata.csv` - Item page display
- `config-map.csv` - Map configuration
- `config-search.csv` - Search fields
- `config-table.csv` - Data table columns

### Complete Documentation

For full CollectionBuilder documentation:
- [CollectionBuilder Docs](https://collectionbuilder.github.io/cb-docs/)
- [Feature Includes Reference](https://collectionbuilder.github.io/cb-docs/docs/features/)
- [Metadata Guidelines](https://collectionbuilder.github.io/cb-docs/docs/metadata/)

---

## Troubleshooting {#troubleshooting}

### Essay Issues

**Essay doesn't appear:**
- Check `order` field exists and is numeric in front matter
- Verify file is in `_essay/` directory
- Confirm front matter is valid YAML (proper `---` markers)
- Check `_site/essay/` directory after build

**Prev/Next buttons missing:**
- Need at least 2 essays for navigation
- Verify `order` values are set
- Check layout is `essay-content` (should be automatic)

**Include doesn't work:**
- Check Liquid syntax: `{% raw %}{% %}{% endraw %}` tags must be exact
- Verify objectid exists in metadata CSV
- Check browser console for errors
- Ensure no extra spaces in tag syntax

### Collection Item Issues

**Item doesn't display in aside:**
- Verify objectid exists in `_data/[metadata].csv`
- Check objectid spelling matches exactly (case-sensitive)
- Ensure item has required fields (image_small, image_thumb for images)
- Test that item page loads: `/items/objectid.html`

### Theme Issues

**Table of contents not showing:**
- Verify `base-theme: monograph` in `_data/theme.yml`
- Check essays have `order` field
- Rebuild site (may need to clear cache)

**Featured image not displaying:**
- Check image path (relative paths from site root)
- Verify image file exists in repository
- Check `image-style` is set in theme.yml
- Look for 404 errors in browser console

### Build Issues

**Site not updating:**
- Wait 2-3 minutes for GitHub Pages rebuild
- Check Actions tab for build errors
- Try force rebuild: Settings → Pages → Change source and change back

**Local build fails:**
- Run `bundle install` to update dependencies
- Check Ruby version (3.x recommended)
- Review error messages for missing gems
- See [CollectionBuilder troubleshooting](https://collectionbuilder.github.io/cb-docs/docs/troubleshooting/)

### Common Errors

**Liquid syntax error:**
```
Make sure includes use proper syntax:
{% raw %}{% include path.html param="value" %}{% endraw %}
Not: { include path.html }
```

**YAML parsing error:**
```
Check front matter:
- Use --- markers top and bottom
- Proper indentation (spaces, not tabs)
- Quote values with special characters
```

**Missing objectid:**
```
Error: objectid "demo_001" not found
Solution: Check CSV file has matching objectid in metadata
```

---

## External Resources {#resources}

### Documentation

- [CB-Essay GitHub Repository](https://github.com/CollectionBuilder/cb-essay)
- [CollectionBuilder Documentation](https://collectionbuilder.github.io/cb-docs/)
- [Jekyll Documentation](https://jekyllrb.com/docs/)
- [Markdown Guide](https://www.markdownguide.org/)
- [Liquid Template Language](https://shopify.github.io/liquid/)

### Example Projects

- [Tender Spaces](https://cdil.lib.uidaho.edu/tender-spaces/) - Heavily customized multimodal essay
- [Digital Dramaturgy](https://digitaldramaturgy.github.io/) - Annotated playscripts
- More examples at [CollectionBuilder Showcase](https://collectionbuilder.github.io/showcase.html)

### Community & Support

- [CollectionBuilder Community](https://collectionbuilder.github.io/community.html)
- [GitHub Discussions](https://github.com/CollectionBuilder/collectionbuilder-csv/discussions)
- [GitHub Issues](https://github.com/CollectionBuilder/cb-essay/issues)

### Learning Resources

- [Markdown Tutorial](https://www.markdowntutorial.com/)
- [Git Basics](https://docs.github.com/en/get-started/using-git/about-git)
- [GitHub Pages Guide](https://docs.github.com/en/pages)
- [CollectionBuilder Workshops](https://collectionbuilder.github.io/workshops/)

---

**Ready to start?** Check out the [demo essays](_essay/) to see CB-Essay in action, then create your first essay in the `_essay/` folder!
