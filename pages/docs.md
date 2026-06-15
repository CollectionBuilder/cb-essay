---
layout: docs
title: CB-Essay Documentation
permalink: /docs.html
---

## Overview {#overview}

**CB-Essay** is a Jekyll-based framework that extends [CollectionBuilder-CSV](https://collectionbuilder.github.io/cb-docs/) to combine long-form essay writing with digital collection features. Write in Markdown, integrate primary sources, and publish multimodal scholarly work on the web for free.

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

**When to use this section:** After you've created your first essay and want to add blockquotes, margin notes, or other specialized features.

CB-Essay provides specialized includes for scholarly writing. **Copy the examples below directly into your essays.** For complete examples and best practices, see the [Writing Features essay](/_essay/04-essay-features.html).

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

**When to use this section:** When you want to add images, PDFs, audio, or other collection items to your essays.

This section covers the basics of referencing collection items in essays. For a complete tutorial with examples, see the [Collection Integration essay](/_essay/05-collection-integration.html).

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

**When to use this section:** To customize your site's colors, fonts, navigation, and homepage layout.

Configure all theme options in `_data/theme.yml`:


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

### Navigation and Homepage Layout Options


```yaml
show-contents-nav: true    # "Contents" button in navbar opens chapter list panel
show-homepage-toc: true    # chapter table of contents on the homepage
show-section-nav: false    # floating sidebar TOC built from H2s on each essay page
```

**Common configurations:**

Simple essay (single narrative, minimal nav):
```yaml
show-contents-nav: false
show-homepage-toc: false
show-section-nav: false
```

Multi-chapter monograph:
```yaml
show-contents-nav: true
show-homepage-toc: true
show-section-nav: false
```

Long single essay with in-page navigation:
```yaml
show-contents-nav: false
show-homepage-toc: false
show-section-nav: true
```


### Color Themes

CB-Essay includes 8 built-in color themes inspired by historical printing presses, each designed for accessibility and long-form reading:

```yaml
color-theme: aldine  # default, idaho, lyre, nonesuch, aldine, doves, kelmscott, gregynog, ashendene
```

**Built-in themes:**
- `default` - Warm cream neutral
- `idaho` - Douglas-fir green
- `lyre` - Faded indigo
- `nonesuch` - Cream with red accents (light navbar)
- `aldine` - Marine blue
- `doves` - Severe black-on-white
- `kelmscott` - Holland blue with red (light navbar)
- `gregynog` - Slate buckram grey-blue
- `ashendene` - Faded brown

Each theme provides coordinated colors for navbar, links, accents, and UI elements.

**Custom color:**
```yaml
color-theme: custom
custom-color: "#8B4513"
navbar-style: dark  # dark or light
```

The system automatically generates an accessible color palette from your hex color.

### Typography & Fonts

CB-Essay offers three font options:

**1. Theme fonts (easiest)** - Automatically matched to your color theme:
```yaml
base-font-family: theme
display-font-family: theme
```

**2. Georgia (no CDN)** - Works offline, no external requests:
```yaml
base-font-family: Georgia
display-font-family: Georgia
```

**3. Custom Google Font:**
```yaml
base-font-family: "'Literata', Georgia, serif"
display-font-family: "'Literata', Georgia, serif"
font-cdn: "https://fonts.googleapis.com/css2?family=Literata:ital,opsz,wght@0,7..72,400;0,7..72,500;1,7..72,400&display=swap"
```

You can mix options - for example, use theme fonts for body text with a custom display font for headings.

**Font size:**
```yaml
base-font-size: 1.2em  # 1.2em - 1.4em recommended for long-form reading
```

### Creating Your Own Theme

CB-Essay includes an AI prompt template at `_prompts/add-theme.md` that guides you through creating custom color themes with coordinated typography.

**What it does:**
- Interviews you about color preferences, navbar style, and aesthetic goals
- Generates complete OKLCH color palettes with accessible contrast ratios
- Creates theme definitions for `_sass/_color-tokens.scss`
- Adds theme documentation to `_data/theme.yml`
- Optionally suggests Google Font pairings

**How to use with an LLM:**

1. **With Claude Code (local):**
   - Open `_prompts/add-theme.md` in your project
   - Ask Claude Code to read the file and follow its instructions
   - Claude will ask for your theme details and make the necessary edits

2. **With Claude.ai (online):**
   - Open `_prompts/add-theme.md` in your repository
   - Copy the contents and paste into a new conversation at [claude.ai](https://claude.ai)
   - Attach these files as context:
     - `_sass/_color-tokens.scss`
     - `_data/theme.yml`
     - `_includes/essay/head/theme-fonts.html` (if adding font pairing)
   - Answer the prompts about your desired theme
   - Claude will provide the code changes to copy into your files

3. **With other LLMs:**
   - The prompt is designed to work with any AI assistant
   - Provide the prompt contents and the three files above
   - Follow the generated instructions to add your theme

**Example workflow:**
```
You: "I want to create a theme called 'forest' with deep evergreen colors"

LLM: "What hue should the theme use? (0-360 degrees, or describe the color)"
You: "Deep forest green, around 150 degrees"

LLM: "Should the navbar be dark (white text) or light (dark text)?"
You: "Dark navbar with cream text"

[LLM generates complete theme code for _color-tokens.scss and theme.yml]
```

The prompt uses CB-Essay's OKLCH color system to ensure your custom theme has proper contrast ratios and coordinates navbar, link, accent, and UI colors automatically.

For complete theme documentation, see [Theme Options Guide](https://github.com/CollectionBuilder/cb-essay/blob/main/docs/cb-essay/theme-options.md).

---

## Working with AI {#working-with-ai}

CB-Essay is data-driven: nearly every change happens in a CSV, in `_data/theme.yml`, or in an essay's Markdown — not in HTML or Liquid. To keep AI assistants working *with* that architecture instead of around it, the repo ships three files at its root:

- **`AGENTS.md`** — the authoritative ruleset. Most coding agents read it automatically at the start of a session, so they already know the customization hierarchy, what never to edit, the essay includes, and the theming system — no need to paste rules into every prompt.
- **`CLAUDE.md`** — a one-line pointer that imports `AGENTS.md`, so Claude Code and Cowork get the same rules with no setup.
- **`HUMANS.md`** — a guide for *you*: how to prompt for outcomes, which changes to review closely, and how to brief the AI for bigger work like a new theme or a redesign.

### How to use them

1. **Just start prompting.** With `AGENTS.md` in the repo, describe outcomes ("switch the site to the `doves` theme," "add a margin aside here") and let the agent route the change to the right file.
2. **Read `HUMANS.md` first.** It teaches you the few "red flags" to watch for in a diff — for example, an agent editing SCSS to recolor the site instead of changing `color-theme` in `_data/theme.yml`.
3. **Keep `AGENTS.md` current.** If you change how the framework works, update that file — every agent inherits the improvement.

For creating custom color themes specifically, the [Theme Options](#theme-options) section above covers the dedicated `_prompts/add-theme.md` workflow.

---

## Print & PDF Output {#print-pdf}

Generate publication-ready PDFs directly from your browser using Paged.js.

### Print Hub

Visit `/print/` to:
- Print individual essays or build custom books
- Choose Letter, A4, or 6×9″ page formats
- Preview paginated layout before printing

### Configuration

Configure print output in `_data/theme.yml`:

```yaml
print:
  author: "Your Name"     # Author on cover and in PDF metadata
  institution: "Your Org" # Institution on cover
  aside-style: margin     # margin (floats into gutter) or inline (callout blocks)
```

### What Works in Print

✅ **Supported:** Blockquotes, asides, images, section breaks, footnotes (as endnotes), running headers, page numbers, table of contents

❌ **Web-only:** Mini-maps, timelines, videos, iframes

### Optimization

- Use high-resolution images (1200px+ width)
- Keep aside text concise
- Test margin vs inline aside styles
- Preview early and often

For complete details on page formats, accessibility features, and technical specifications, visit the [Print Hub](/print/).

---

## Accessibility {#accessibility}

CB-Essay has been tested against the [Web Content Accessibility Guidelines (WCAG) 2.1](https://www.w3.org/WAI/standards-guidelines/wcag/) using tools like WAVE and Lighthouse, and **an unmodified site should be WCAG 2.1 accessible out of the box.** Focus indicators are visible, interactive features are keyboard-operable, and the built-in color themes are tuned for sufficient contrast.

**An accessible foundation is not the same as an accessible published site.** Once you customize the theme or add your own content, accessibility becomes your responsibility — you must test and verify it yourself. The most common things to check:

- **Alt text** — Set `featured-image-alt-text` in `_data/theme.yml`, and add an `image_alt_text` column to your metadata CSV to give each collection item custom, meaningful alt text (recommended for any image that carries meaning; falls back to the title if omitted).
- **Transcripts** — Add an `object_transcript` column to your metadata CSV for audio and video items; CB renders it as a transcript on the item page. Provide one for every audio/video object.
- **Heading order** — Use `##`, `###` in sequence; don't skip levels or pick a heading for its size.
- **Color contrast** — Built-in themes are pre-checked. If you use `color-theme: custom`, re-test contrast (aim for at least 4.5:1 for body text) and never rely on color alone to convey meaning.
- **Keyboard** — After adding any interactive feature, confirm it works with Tab, Enter, and Escape only.

Before publishing, run an automated check (WAVE or Lighthouse), do a keyboard-only pass, and spot-check with a screen reader. Repeat whenever you add content.

For detailed, essay-specific guidance and a full resource list, see the [Accessibility Guide](https://github.com/CollectionBuilder/cb-essay/blob/main/docs/cb-essay/accessibility.md).

---

## Gutenberg Extractor {#gutenberg}

CB-Essay includes a GitHub Action to import **60,000+ public domain books** from Project Gutenberg directly into your `_essay/` folder.

### How to Use

1. First, [Setup GitHub Pages](#2-enable-github-pages) using the instructions above in the Quickstart. (5 minutes)
2. Once that's done, go to the **Actions** tab in your GitHub repository
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

**When to use this section:** Advanced features for working with your collection metadata - timelines, maps, data downloads, and metadata configuration.

CB-Essay includes all standard CollectionBuilder pages and features. This section is for advanced users who want to customize CollectionBuilder visualizations and pages.

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
- Ensure item has fields: display_template, image_small, image_thumb
- Test that item page loads: `/items/objectid.html`

### Theme Issues

**Table of contents not showing:**
- Verify `show-homepage-toc: true` in `_data/theme.yml`
- Check essays have `order` field in front matter
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

### Community & Support

- [GitHub Discussions](https://github.com/CollectionBuilder/collectionbuilder-csv/discussions)
- [GitHub Issues](https://github.com/CollectionBuilder/cb-essay/issues)

### Learning Resources

- [Markdown Tutorial](https://www.markdowntutorial.com/)
- [Git Basics](https://docs.github.com/en/get-started/using-git/about-git)
- [GitHub Pages Guide](https://docs.github.com/en/pages)

---

**Ready to start?** Check out the [demo essays](_essay/) to see CB-Essay in action, then create your first essay in the `_essay/` folder!
