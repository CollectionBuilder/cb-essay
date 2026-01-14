# Essay Writing Guide

CB-Essay uses Jekyll collections to manage essay content. Essays are simple Markdown files with front matter that controls their display and navigation.

## Essay File Structure

### Location
All essay files live in the `_essay/` directory at the root of your project:

```
your-project/
├── _essay/
│   ├── 01-introduction.md
│   ├── 02-chapter-one.md
│   └── 03-conclusion.md
├── _config.yml
└── ...
```

### File Naming
File names should:
- Use lowercase with hyphens
- Optionally include order prefix (e.g., `01-`, `02-`)
- End with `.md`

**Note:** The filename determines the URL slug, but display order is controlled by front matter.

## Front Matter

Every essay file starts with YAML front matter between `---` markers:

### Required Fields

```yaml
---
title: Your Essay Title
order: 1
---
```

- **`title`**: The essay's title (appears in navigation, page header)
- **`order`**: Numeric value controlling display order (1, 2, 3...)

### Optional Fields

```yaml
---
title: Of Thumbs
order: 1
byline: Michel de Montaigne
featured-image: /assets/img/chapter-image.jpg
---
```

- **`byline`**: Author or attribution line
- **`featured-image`**: Header image for this specific essay

## Writing Content

After the front matter, write your essay content in Markdown:

```markdown
---
title: My First Essay
order: 1
---

## Introduction

This is my essay introduction with **bold** and *italic* text.

Here's a paragraph with a [link](https://example.com).

### Subsection

- Bullet point one
- Bullet point two

1. Numbered list
2. Another item
```

### Markdown Basics

CB-Essay supports standard Markdown:

- **Headings:** `## Heading 2`, `### Heading 3`
- **Bold:** `**bold text**`
- **Italic:** `*italic text*`
- **Links:** `[link text](url)`
- **Images:** `![alt text](image-url)`
- **Lists:** `-` for bullets, `1.` for numbers
- **Blockquotes:** `> Quote text` (or use essay blockquote include)

## Navigation

Essays automatically get prev/next navigation based on their `order` value:

```
← Previous Essay  |  Next Essay →
```

Navigation appears at:
- Bottom of each essay page
- Automatic linking based on sequential order

### Order Tips

- Use gaps (1, 10, 20, 30...) to allow easy insertion later
- Order determines sequence, not filename
- Essays with same order value may appear unpredictably

## Essay Themes

CB-Essay supports two homepage/navigation themes set in `_data/theme.yml`:

### Essay Theme (Default)
```yaml
base-theme: essay
```
- Traditional blog-like layout
- Linear reading experience
- Simple navigation

### Monograph Theme
```yaml
base-theme: monograph
```
- Book-like presentation
- Table of contents on homepage
- Chapter-style navigation

## Using Essay Includes

CB-Essay provides special includes for enhanced features. Include them in your Markdown:

### Blockquote Example
```liquid
{% include essay/feature/blockquote.html
   quote="Knowledge comes, but wisdom lingers"
   speaker="Alfred Lord Tennyson" %}
```

### Aside/Margin Note Example
```liquid
{% include essay/feature/aside.html
   text="This is a margin note" %}
```

See the [Essay Features Reference](essay-features.md) for complete documentation of all includes.

## Integrating Collection Items

Reference items from your collection metadata using object IDs:

```liquid
{% include essay/feature/aside.html
   objectid="demo_001"
   text="Additional context about this item" %}
```

The item must exist in your `_data/[metadata].csv` file with matching `objectid`.

## Workflow

### 1. Create Essay File
```bash
touch _essay/my-new-essay.md
```

### 2. Add Front Matter
```yaml
---
title: My New Essay
order: 2
---
```

### 3. Write Content
Use Markdown + essay includes

### 4. Preview Locally
```bash
bundle exec jekyll s
```
Visit `http://localhost:4000/essay/my-new-essay.html`

### 5. Publish
```bash
git add _essay/my-new-essay.md
git commit -m "Add new essay"
git push
```

GitHub Pages will automatically rebuild your site.

## Best Practices

### Organization
- Keep essays focused (one main idea per file)
- Use consistent front matter formatting
- Number essays with gaps for flexibility

### Writing
- Write in plain Markdown first
- Add includes/features after drafting
- Test locally before pushing

### Navigation
- Ensure `order` values are sequential
- Check prev/next links work correctly
- Verify all essays appear in monograph table of contents (if using)

### Performance
- Optimize images before including
- Don't embed too many high-res items per essay
- Test load times on slower connections

## Troubleshooting

### Essay doesn't appear in navigation
- Check `order` field is present and numeric
- Verify file is in `_essay/` directory
- Confirm front matter is valid YAML

### Prev/Next buttons missing
- Check if you have multiple essays (need at least 2)
- Verify `order` values are set
- Ensure essays are building (check `_site/essay/`)

### Include doesn't work
- Check liquid syntax (no extra spaces in `{% %}`)
- Verify objectid exists in metadata
- See browser console for errors

## Next Steps

- [Essay Features Reference](essay-features.md) - Learn all available includes
- [Theme Options](theme-options.md) - Customize your essay site
- [Gutenberg Extraction](gutenberg-extraction.md) - Import public domain books
