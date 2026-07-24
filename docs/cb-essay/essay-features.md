# Essay Features Reference

CB-Essay provides specialized Liquid includes for enhanced essay features. These includes extend standard Markdown to create rich, interactive scholarly content.

Includes below come in two flavors, and the path tells you which: `feature/...` includes are core CollectionBuilder features that work on any page across your site, while `essay/feature/...` includes are built specifically for essay content.

This reference is split across a few pages by feature type:

| Page | Covers |
|------|--------|
| **[Inline & Margin Features](essay-features-inline.md)** | Blockquote, Aside, Image Aside, Image Gallery, New Section — the includes you drop directly into a paragraph |
| **[Scrollytelling Blocks](essay-features-scrolly.md)** | `scrolly-media.html` + `scrolly-step.html` + `scrolly-end.html` — a sticky image with scrolling text panels |
| **[Scrollytelling Map Backgrounds](essay-features-scrolly-map.md)** | `scrolly-map.html` — a sticky Leaflet map (geographic or a tiled manuscript image) with scrolling location narration |
| **[Mini Map & Reusing CollectionBuilder Features](essay-features-more.md)** | `mini-map.html`, plus using standard CollectionBuilder includes (cards, timelines, clouds) inside essays |

## Quick Reference

| Feature | Include | Purpose | Reference |
|---------|---------|---------|-----------|
| Blockquote | `essay/feature/blockquote.html` | Styled quotations with attribution | [Inline & Margin Features](essay-features-inline.md#blockquote) |
| Aside | `essay/feature/aside.html` | Margin notes (text or collection items) | [Inline & Margin Features](essay-features-inline.md#aside-margin-note) |
| Image Aside | `essay/feature/image-aside.html` | Images in margins | [Inline & Margin Features](essay-features-inline.md#image-aside) |
| Image Gallery | `essay/feature/image-gallery.html` | Multi-image, video, audio & PDF galleries | [Inline & Margin Features](essay-features-inline.md#image-gallery) |
| Section Break | `essay/new-section.html` | Scrollama transitions | [Inline & Margin Features](essay-features-inline.md#new-section-scrollama-transition) |
| **Scrolly Block** | `essay/feature/scrolly-media.html` + `scrolly-step.html` + `scrolly-end.html` | **Sticky image + scrolling text panels** | [Scrollytelling Blocks](essay-features-scrolly.md) |
| **Scrolly Map Block** | `essay/feature/scrolly-map.html` + `scrolly-step.html` + `scrolly-end.html` | **Sticky Leaflet map + scrolling location narration** | [Scrollytelling Map Backgrounds](essay-features-scrolly-map.md) |
| Mini Map | `feature/mini-map.html` | Embedded maps | [Mini Map & Reusing CollectionBuilder Features](essay-features-more.md#mini-map) |

---

## Combining Features

You can combine multiple features in a single essay:

```markdown
## Chapter Introduction

Opening paragraph with context.

{% include essay/feature/aside.html
   text="Historical note about this period" %}

Main content continues here with **bold** and *italic* text.

{% include essay/feature/blockquote.html
   quote="A relevant quotation"
   speaker="Primary Source Author" %}

More analysis...

{% include feature/mini-map.html
   latitude="40.7128"
   longitude="-74.0060"
   zoom="11" %}

{% include essay/new-section.html %}

## Next Chapter

Continuation...
```

## Copy & Replace Strategy

**Every feature in the demo essays can be copied directly:**

1. Find a feature you like in the demo
2. Copy the entire `{% include ... %}` block
3. Paste into your essay
4. Replace the parameter values with your content
5. Save and preview

Example - copying a blockquote:

**From demo:**
```liquid
{% include essay/feature/blockquote.html
   quote="Demo quote text"
   speaker="Demo Author" %}
```

**Your version:**
```liquid
{% include essay/feature/blockquote.html
   quote="Your actual quote"
   speaker="Your Source" %}
```

## Troubleshooting

### Include doesn't render
- Check liquid syntax: `{% %}` tags must be exact
- Verify include path is correct
- Look for typos in parameter names
- Check browser console for errors

### Collection item doesn't display
- Verify objectid exists in your metadata CSV
- Check objectid spelling/capitalization
- Ensure item has required fields (image_small, image_thumb, etc.)
- Test item page loads independently

Feature-specific issues (asides displaying inline, maps not loading, etc.) are covered in the Troubleshooting section of each reference page above.

## Next Steps

- [Inline & Margin Features](essay-features-inline.md), [Scrollytelling Blocks](essay-features-scrolly.md), [Scrollytelling Map Backgrounds](essay-features-scrolly-map.md), and [Mini Map & Reusing CollectionBuilder Features](essay-features-more.md) — the full feature reference
- [Essay Writing Guide](essay-writing.md) - Workflow and front matter
- [Theme Options](theme-options.md) - Customize appearance
- Explore demo essays to see features in action
