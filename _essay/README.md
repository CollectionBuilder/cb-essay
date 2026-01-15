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

## Learn More

- Read the demo essays in this folder for examples
- See [Essay Writing Guide](../docs/cb-essay/essay-writing.md) for detailed reference
- See [Essay Features Reference](../docs/cb-essay/essay-features.md) for complete feature documentation
- See [Collection Integration](../docs/cb-essay/gutenberg-extraction.md) for working with collection items

## Getting Help

- [CB-Essay Documentation](../docs/cb-essay/)
- [CollectionBuilder Docs](../docs/)
- [GitHub Issues](https://github.com/CollectionBuilder/cb-essay/issues)

---

**Ready to write?** Create your first essay and start building!
