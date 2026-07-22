# Essay Features Reference

CB-Essay provides specialized Liquid includes for enhanced essay features. These includes extend standard Markdown to create rich, interactive scholarly content.

## Quick Reference

| Feature | Include | Purpose |
|---------|---------|---------|
| Blockquote | `essay/feature/blockquote.html` | Styled quotations with attribution |
| Aside | `essay/feature/aside.html` | Margin notes (text or collection items) |
| Image Aside | `essay/feature/image-aside.html` | Images in margins |
| Image Gallery | `essay/feature/image-gallery.html` | Multi-image displays |
| Section Break | `essay/new-section.html` | Scrollama transitions |
| **Scrolly Block** | `essay/feature/scrolly-media.html` + `scrolly-step.html` + `scrolly-end.html` | **Sticky image + scrolling text panels** |
| Mini Map | `feature/mini-map.html` | Embedded maps |

---

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

Display multiple collection items as an inline gallery.

### Usage

```liquid
{% include essay/feature/image-gallery.html
   objectid="demo_001;demo_002;demo_003" %}
```

### Parameters

| Parameter | Required | Description | Values |
|-----------|----------|-------------|--------|
| `objectid` | **Yes** | Semicolon-separated list of objectids | `id1;id2;id3` |
| `caption` | No | Gallery caption | Any text |

### Example

```liquid
{% include essay/feature/image-gallery.html
   objectid="demo_001;demo_005;demo_012"
   caption="Manuscript variations from the collection" %}
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

## Scrollytelling Blocks

Pin an image in the viewport while multiple narrative text panels scroll over or beside it — the StoryMaps / scrolly-explainer pattern. Useful for manuscript walkthroughs, archival photo essays, site surveys, or any story where a visual needs to anchor the reader while text builds around it.

A scrolly block requires three paired includes:

1. **`scrolly-media.html`** — opens the block and sets the first (pinned) image
2. **`scrolly-step.html`** — adds each subsequent text panel (optionally swapping the image)
3. **`scrolly-end.html`** — closes the block and returns to normal essay flow

### Immersive layout (default)

The image fills the full viewport; text cards float over it.

```liquid
{% include essay/feature/scrolly-media.html objectid="photo_001" alt="Archival photograph" %}

First panel text. Written in normal Markdown — the image is pinned behind it.

{% include essay/feature/scrolly-step.html objectid="photo_002" %}

When this panel scrolls into view the image cross-fades to photo_002.

{% include essay/feature/scrolly-step.html position="right" text-background="dark" %}

Third panel with a dark card, no image swap — previous image stays.

{% include essay/feature/scrolly-end.html %}

Normal essay text resumes here after the block closes.
```

### Sidecar layout

Image stays fixed on the right; text panels scroll on the left. Collapses to stacked on mobile.

```liquid
{% include essay/feature/scrolly-media.html objectid="photo_001" layout="sidecar" %}

Text panel beside the image.

{% include essay/feature/scrolly-step.html objectid="photo_002" %}

Second panel; image swaps on the right.

{% include essay/feature/scrolly-end.html %}
```

### Using direct image paths instead of objectids

```liquid
{% include essay/feature/scrolly-media.html
   src="/assets/img/my-photo.jpg"
   alt="Description of the image"
   caption="Credit: University Archives" %}
```

### `scrolly-media.html` parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `objectid` | — | Collection item ID; resolves to its `image_small` (or `object_download`) |
| `src` | — | Direct image path or URL (alternative to `objectid`) |
| `alt` | — | Image alt text |
| `caption` | — | Small credit line overlaid at bottom-right of image |
| `layout` | `immersive` | `immersive` (full-screen) or `sidecar` (side-by-side, image right) |
| `position` | `left` | First panel position: `left`, `center`, or `right` |
| `text-background` | `light` | First panel card style: `light` or `dark` |
| `step-height` | `70vh` | Minimum scroll height per panel — controls how long each panel stays in view before the next triggers. Set on `scrolly-media.html` to apply to all steps in the block; override on individual `scrolly-step.html` calls for finer control. Accepts any CSS length: `80vh`, `600px`, etc. |

### `scrolly-step.html` parameters

Same as `scrolly-media.html` except `layout` (set once on the opening include).

| Parameter | Default | Description |
|-----------|---------|-------------|
| `objectid` | — | Swap image to this collection item when panel enters view |
| `src` | — | Swap image to this URL when panel enters view |
| `alt` | — | Updated alt text for swapped image |
| `position` | `left` | Panel position for this step |
| `text-background` | `light` | Panel card style for this step |
| `step-height` | *(inherits)* | Per-step height override; overrides the block-level `step-height` for this panel only |

### `scrolly-end.html` parameters

None. Just closes the block.

### Controlling step duration

By default each panel is `70vh` tall, giving a comfortable scroll distance before the next panel triggers. Increase `step-height` for longer dwell time on an image, decrease it for a faster pace:

```liquid
{% comment %} Slow, meditative — linger on each image {% endcomment %}
{% include essay/feature/scrolly-media.html objectid="photo_001" step-height="100vh" %}

First panel — reader must scroll a full screen before anything changes.

{% include essay/feature/scrolly-step.html objectid="photo_002" %}

Second panel, also 100vh (inherits from block).

{% include essay/feature/scrolly-step.html objectid="photo_003" step-height="50vh" %}

Third panel moves faster — useful for a quick transition.

{% include essay/feature/scrolly-end.html %}
```

### Layout notes

**Immersive:** The sticky image fills the full viewport. Text cards float over it. After the last panel, the block adds a full viewport of blank space so the image scrolls cleanly off screen before the next essay content appears.

**Sidecar:** Text scrolls on the left (45% width), image stays fixed on the right (55% width). The same full-viewport bottom padding keeps the image sticky through all panels. On mobile both layouts collapse to the same stacked style: image at top, text scrolling below.

### Scroll direction

Scrolling back up restores the correct image automatically — each panel's "effective image" (the last image defined at or before that point in the block) is pre-computed at page load, so forward and backward scrolling always show the right visual.

### Notes

- Always close every block with `scrolly-end.html` — an unclosed block breaks the essay layout.
- Steps without `objectid`/`src` keep the previously shown image.
- Multiple scrolly blocks on one page work independently.
- Print output renders the initial image once, then all panel text inline beneath it.
- Disable Scrollama on an essay page with `scrollama: false` in front matter — scrolly blocks won't animate but render as readable static content.

---

## Mini Map

Embed a small map with custom coordinates.

### Usage

```liquid
{% include feature/mini-map.html
   latitude="46.727485"
   longitude="-117.014185"
   zoom="10" %}
```

### All Parameters

```liquid
{% include feature/mini-map.html
   latitude="46.727485"
   longitude="-117.014185"
   zoom="10"
   height="300px"
   attribution="Map data © OpenStreetMap contributors" %}
```

| Parameter | Required | Description | Values |
|-----------|----------|-------------|--------|
| `latitude` | **Yes** | Map center latitude | Decimal degrees |
| `longitude` | **Yes** | Map center longitude | Decimal degrees |
| `zoom` | No | Zoom level | 1-18 (default: 10) |
| `height` | No | Map height | CSS height value |
| `attribution` | No | Custom attribution | Text |

### Example

```liquid
{% include feature/mini-map.html
   latitude="48.8566"
   longitude="2.3522"
   zoom="12" %}

*Map showing Paris, France where this event occurred*
```

---

## Using CollectionBuilder Features in Essays

Beyond essay-specific includes, you can use any standard CollectionBuilder feature include:

### Item Card

```liquid
{% include feature/item-card.html objectid="demo_001" %}
```

### Timeline

```liquid
{% include feature/timeline.html %}
```

### Cloud Visualization

```liquid
{% include feature/cloud.html fields="subject" %}
```

See [CollectionBuilder documentation](../index.md) for complete feature reference.

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

### Scrolly Blocks
- Always close with `scrolly-end.html` — unclosed blocks break the essay layout
- Use landscape-oriented images (16:9 or wider) for best results in immersive; portrait works well in sidecar
- Keep panel text concise (2-4 sentences); readers are processing the image at the same time
- Default `step-height` is `70vh`; increase to `90vh`–`100vh` for a slower, more meditative pace or decrease to `50vh` for quick transitions
- Test on mobile: both layouts collapse to the same stacked style (image above, text below)
- Avoid nesting scrolly blocks

### Maps
- Verify coordinates are correct
- Choose appropriate zoom level
- Keep maps relevant to content
- Consider performance impact

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

### Aside appears inline instead of margin
- This is normal on mobile/small screens
- Asides automatically reflow for responsive design
- Test on desktop to see margin layout

### Map doesn't load
- Verify latitude/longitude are valid decimals
- Check zoom level is between 1-18
- Ensure internet connection (uses external map tiles)
- Check browser console for errors

## Next Steps

- [Essay Writing Guide](essay-writing.md) - Workflow and front matter
- [Theme Options](theme-options.md) - Customize appearance
- Explore demo essays to see features in action
