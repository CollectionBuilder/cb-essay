# Essay Content Folder

This folder contains your essay content as Markdown files with front matter.

## Creating Essays

Each essay is a Markdown file with YAML front matter:

```yaml
---
title: Your Essay Title
order: 1
byline: Your Name (optional)
---

Your essay content in Markdown...
```

### Required Front Matter

- **`title`** - The essay's title (appears in navigation and page header)
- **`order`** - Numeric value controlling display order (1, 2, 3...)

### Optional Front Matter

- **`byline`** - Author attribution line
- **`featured-image`** - Header image specific to this essay

## File Naming

Name your essay files descriptively:

```
01-introduction.md
02-chapter-one.md
03-chapter-two.md
04-conclusion.md
```

The **filename determines the URL**, but the **`order` field controls navigation sequence**.

## Writing Workflow

1. **Create** a new `.md` file in this folder
2. **Add front matter** with title and order
3. **Write content** in Markdown
4. **Save** and preview locally with `bundle exec jekyll s`
5. **Push to GitHub** to publish

## Essay Features

CB-Essay provides specialized includes for scholarly writing:

### Blockquotes

```liquid
{% include essay/feature/blockquote.html
   quote="Your quotation here"
   speaker="Author Name" %}
```

### Asides (Margin Notes)

```liquid
{% include essay/feature/aside.html
   text="Margin note providing context" %}
```

### Asides with Collection Items

```liquid
{% include essay/feature/aside.html
   objectid="demo_001"
   text="Context about this item" %}
```

### Image Galleries

```liquid
{% include essay/feature/image-gallery.html
   objectid="item1;item2;item3" %}
```

### Mini Maps

```liquid
{% include feature/mini-map.html
   latitude="46.727485"
   longitude="-117.014185"
   zoom="12" %}
```

### Section Breaks

```liquid
{% include essay/new-section.html %}
```

## Copy & Replace Strategy

**The demo essays in this folder show working examples of every feature.** To use a feature:

1. Find it in a demo essay
2. Copy the `{% include ... %}` code block
3. Paste into your essay
4. Replace the content with your own
5. Save and preview

## Order Tips

Use gaps in your order numbers for flexibility:

```yaml
order: 10  # Instead of 1
order: 20  # Instead of 2
order: 30  # Instead of 3
```

This makes it easy to insert essays later without renumbering everything.

## Reference Pages (Hidden from Navigation)

Not every file in this folder needs to be part of the sequential teaching flow. A deep-reference page — a big gallery of examples for one feature, like `scrolly-media-gallery.md` — can live here too, using the same layout, styling, and scripts as any other essay, but excluded from the homepage table of contents, the off-canvas "Contents" panel, and prev/next navigation. Give it a high `order` value (so it sorts harmlessly at the end of the collection) and set `hide_from_nav: true`:

```yaml
---
title: Your Reference Gallery
order: 1000
hide_from_nav: true
---
```

Link to it explicitly from wherever it's relevant (a teaching-sequence essay, or `/docs.html`) instead of relying on it to appear in navigation.

## Excluding an Essay From Print/PDF

Some essays are web-only — a scrolly-media gallery, a maps-heavy chapter, anything that doesn't translate to a printed page. Set `hide_from_print: true` and the essay is dropped from the Print Hub's book builder checklist, table of contents, and individual "Print Essay" cards, and from full-book PDF generation:

```yaml
---
title: Interactive Map Tour
order: 50
hide_from_print: true
---
```

The essay still appears normally on the website; only the `/print/` hub and generated PDFs skip it.

## Learn More

- Read the demo essays in this folder for examples
- See [CB-Essay Documentation](/docs.html) for complete reference
- Check the [Essay Features section](/docs.html#essay-features) for all available features
- Learn about [Collection Integration](/docs.html#collection-integration)

## Getting Help

- [CB-Essay Documentation](/docs.html)
- [CollectionBuilder Docs](https://collectionbuilder.github.io/cb-docs/)
- [GitHub Issues](https://github.com/CollectionBuilder/cb-essay/issues)

---

**Ready to write?** Create your first essay and start building!
