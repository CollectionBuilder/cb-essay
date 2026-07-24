# Inline & Margin Features

The essay includes you'll use most often — quotations, margin notes, and galleries that drop directly into the flow of a paragraph. Part of the [Essay Features Reference](essay-features.md).

## Blockquote

Styled quotation blocks with optional attribution and source.

### Basic Usage

```liquid
{% include essay/feature/blockquote.html
   quote="Knowledge comes, but wisdom lingers"
   speaker="Alfred Lord Tennyson" %}
```

### All Parameters

```liquid
{% include essay/feature/blockquote.html
   quote="The only way out is through"
   speaker="Robert Frost"
   source="A Servant to Servants"
   source-link="https://example.com"
   size="lg"
   align="center"
   class="my-custom-class"
   bottom="true" %}
```

| Parameter | Required | Description | Values |
|-----------|----------|-------------|--------|
| `quote` | **Yes** | Quote text (supports Markdown) | Any text |
| `speaker` | No | Person quoted | Any text |
| `source` | No | Title of source work | Any text |
| `source-link` | No | URL to source (opens new tab) | URL |
| `size` | No | Text size | `xl`, `lg`, `md`, `sm`, default |
| `align` | No | Text alignment | `left`, `center`, `right` |
| `class` | No | Additional CSS classes | Class names |
| `bottom` | No | Remove bottom padding | any value |

### Examples

**Simple quote:**
```liquid
{% include essay/feature/blockquote.html
   quote="To be or not to be, that is the question" %}
```

**With speaker and source:**
```liquid
{% include essay/feature/blockquote.html
   quote="The reports of my death are greatly exaggerated"
   speaker="Mark Twain"
   source="New York Journal, 1897" %}
```

**Large centered quote:**
```liquid
{% include essay/feature/blockquote.html
   quote="In the beginning was the Word"
   size="xl"
   align="center" %}
```

---

## Aside (Margin Note)

Creates margin notes that appear beside your text. Can display just text or include collection items.

### Text Only

```liquid
{% include essay/feature/aside.html
   text="This is a margin note providing additional context" %}
```

### With Collection Item

```liquid
{% include essay/feature/aside.html
   objectid="demo_001"
   text="Additional context about this item" %}
```

### All Parameters

```liquid
{% include essay/feature/aside.html
   objectid="demo_001"
   text="Custom caption and context"
   caption="Custom title override"
   height="300px"
   gallery="false" %}
```

| Parameter | Required | Description | Values |
|-----------|----------|-------------|--------|
| `text` | No* | Margin note text (supports Markdown) | Any text |
| `objectid` | No* | Collection item ID | Valid objectid from metadata |
| `caption` | No | Override item title | Any text |
| `height` | No | Max height for images | CSS height value (default: 205px) |
| `gallery` | No | Link to spotlight viewer vs item page | `true` (default), `false` |

*At least one of `text` or `objectid` must be provided

### Examples

**Simple margin note:**
```liquid
{% include essay/feature/aside.html
   text="Montaigne wrote this essay in 1580" %}
```

**Item with context:**
```liquid
{% include essay/feature/aside.html
   objectid="demo_012"
   text="This manuscript shows the original handwriting" %}
```

**Image without gallery:**
```liquid
{% include essay/feature/aside.html
   objectid="demo_003"
   gallery="false"
   height="250px" %}
```

---

## Image Aside

Specialized aside for displaying collection images in margins.

### Usage

```liquid
{% include essay/feature/image-aside.html %}
```

**Note:** This include is typically called automatically by `aside.html` when an objectid has image fields. Use `aside.html` instead.

---

## Image Gallery

Display one or more items — images, video, audio, or PDFs — as an inline gallery that opens in a full-screen Spotlight viewer. `objectid` accepts collection items, external URLs, or relative paths; mix as many as you like with semicolons.

### Usage

```liquid
{% include essay/feature/image-gallery.html
   objectid="demo_001;demo_002;demo_003" %}
```

### Parameters

| Parameter | Required | Description | Values |
|-----------|----------|-------------|--------|
| `objectid` | **Yes** | Semicolon-separated list: collection objectids, external URLs, and/or relative paths | `id1;id2;id3`, `https://...`, `/assets/img/x.jpg` |
| `alt` | Conditional | Alt text; required for external/relative sources, optional for collection items (falls back to metadata) | Any text, `;`-separated |
| `caption` | No | Caption below each item; defaults to item title for collection items. Set `caption=false` (no quotes) to hide all captions | Any text, `;`-separated, or `false` |
| `title` | No | Title shown in the Spotlight viewer | Any text, `;`-separated |
| `source` | No | Source attribution in the Spotlight viewer; defaults to metadata `source` for collection items | Any text, `;`-separated |
| `sourcelink` | No | URL for the source attribution link; defaults to metadata `source_identifier` for collection items | Any URL, `;`-separated |
| `link` | No | Overrides where the item links; defaults to the item page (collection items) or the file itself (external/relative) | Any URL, `;`-separated |
| `width` | No | Desktop width as a percentage of the container (always 100% on mobile) | `25`, `50`, `75`, `100` |

Non-image items (video, audio, PDF) render as a labeled placeholder and open the matching player automatically — no separate include per media type.

### Example

```liquid
{% include essay/feature/image-gallery.html
   objectid="demo_001;demo_005;demo_012"
   caption="Manuscript variations from the collection" %}
```

**Mixed media:**

```liquid
{% include essay/feature/image-gallery.html
   objectid="image_item;video_item;audio_item;pdf_item" %}
```

---

## New Section (Scrollama Transition)

Creates a visual section break with scrolling transition effects.

### Usage

```liquid
{% include essay/new-section.html %}

## New Section Title

Content for the new section...
```

### How It Works

- Creates a visual break in the essay
- Uses Scrollama library for scroll-triggered animations
- Helps structure long essays into distinct sections
- Works automatically - no parameters needed

### Example

```liquid
## Introduction

Opening paragraphs...

{% include essay/new-section.html %}

## Historical Context

New section content...
```

---

## Best Practices

### Asides
- Use sparingly (2-4 per essay max)
- Keep text brief (1-3 sentences)
- Ensure referenced objects exist in metadata
- Test on mobile (asides may display inline)

### Blockquotes
- Use for significant quotations
- Always include `speaker` for attribution
- Keep quotes focused and relevant
- Don't nest blockquotes

### Images
- Optimize before adding to collection
- Provide meaningful alt text in metadata
- Test loading times
- Consider mobile display

### Section Breaks
- Use to separate major sections
- Don't overuse (creates choppy reading)
- Ensure sections are substantial
- Works best with 3-4 sections per essay

## Troubleshooting

### Aside appears inline instead of margin
- This is normal on mobile/small screens
- Asides automatically reflow for responsive design
- Test on desktop to see margin layout

---

**[← Back to Essay Features Reference](essay-features.md)**
