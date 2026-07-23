# Essay Features Reference

CB-Essay provides specialized Liquid includes for enhanced essay features. These includes extend standard Markdown to create rich, interactive scholarly content.

Includes below come in two flavors, and the path tells you which: `feature/...` includes are core CollectionBuilder features that work on any page across your site, while `essay/feature/...` includes are built specifically for essay content.

## Quick Reference

| Feature | Include | Purpose |
|---------|---------|---------|
| Blockquote | `essay/feature/blockquote.html` | Styled quotations with attribution |
| Aside | `essay/feature/aside.html` | Margin notes (text or collection items) |
| Image Aside | `essay/feature/image-aside.html` | Images in margins |
| Image Gallery | `essay/feature/image-gallery.html` | Multi-image, video, audio & PDF galleries |
| Section Break | `essay/new-section.html` | Scrollama transitions |
| **Scrolly Block** | `essay/feature/scrolly-media.html` + `scrolly-step.html` + `scrolly-end.html` | **Sticky image + scrolling text panels** |
| **Scrolly Map Block** | `essay/feature/scrolly-map.html` + `scrolly-step.html` + `scrolly-end.html` | **Sticky Leaflet map + scrolling location narration** |
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
| `step-height` | `300vh` | Minimum scroll height per panel — controls how long each panel stays in view before the next triggers. Set on `scrolly-media.html` to apply to all steps in the block; override on individual `scrolly-step.html` calls for finer control. Accepts any CSS length: `80vh`, `600px`, etc. |
| `image-focus` | `center` | Any CSS `object-position` value (`"top"`, `"80% 30%"`, `"left center"`). Controls which part of the image is visible in `cover` mode and sets the zoom target for `zoom-in`/`zoom-out` animations. |
| `animate` | — | Slow CSS animation on the sticky image. Options: `zoom-in`, `zoom-out`, `pan-left`, `pan-right`, `ken-burns`. See below. |

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
| `image-focus` | — | Override focus point for this step (applied when panel enters view) |
| `animate` | — | Start or change the animation when this panel enters view; restarts on every entry |

### `scrolly-end.html` parameters

None. Just closes the block.

### Image focus and animation

**`image-focus`** sets `object-position` on the sticky image, controlling which part of the image fills the frame in `cover` mode. It also sets the `transform-origin` so zoom animations pull toward that point.

```liquid
{% include essay/feature/scrolly-media.html
   objectid="photo_001"
   image-focus="80% 30%" %}
```

Any CSS `object-position` value works: `"top"`, `"center"`, `"left center"`, `"80% 30%"`.

**`animate`** applies a slow CSS animation (20 seconds, plays once) to the sticky image. The animation restarts each time a panel with `animate` set enters the viewport — whether scrolling forward or back.

| Value | Effect |
|-------|--------|
| `zoom-in` | Slowly zooms toward the `image-focus` point (default: center) |
| `zoom-out` | Starts zoomed in, slowly pulls back |
| `pan-left` | Pans from right edge to left edge |
| `pan-right` | Pans from left edge to right edge |
| `ken-burns` | Diagonal zoom + gentle drift (preset, ignores `image-focus`) |

```liquid
{% include essay/feature/scrolly-media.html
   objectid="photo_001"
   animate="ken-burns" %}

Opening panel — image slowly drifts and zooms.

{% include essay/feature/scrolly-step.html
   objectid="detail_001"
   image-focus="75% 40%"
   animate="zoom-in" %}

Image swaps; new image zooms toward the upper-right subject.

{% include essay/feature/scrolly-step.html
   objectid="wide_001"
   animate="pan-right" %}

Pans across the full width of a wide archival photograph.

{% include essay/feature/scrolly-end.html %}
```

**Notes:**
- `image-focus` on a `scrolly-step.html` is applied when that step enters view. Steps without `image-focus` keep the previously set focus.
- Pan animations (`pan-left`, `pan-right`) sweep the full horizontal range of the image; `image-focus` is ignored for panning but still affects the static position on adjacent steps.
- On image swap, the animation always restarts on the new image (gives each image a clean start). Steps without `animate` that trigger a swap will restart the current animation.
- All animations are suppressed in print/PDF output.

### Controlling step duration

By default each panel is `300vh` tall, giving a comfortable scroll distance before the next panel triggers. Increase `step-height` for longer dwell time on an image, decrease it for a faster pace:

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

## Scrollytelling Map Backgrounds

A scrolly block can use an interactive Leaflet map as its pinned background instead of an image or video — for narrating a journey between locations, or detailing a single site as the reader scrolls. Swap `scrolly-media.html` for `scrolly-map.html`; `scrolly-step.html` and `scrolly-end.html` are shared with the image/video blocks — call `scrolly-step.html` with `map-*` parameters instead of `objectid`/`src`, and close with the same `scrolly-end.html`.

Basemaps, center/zoom defaults, and clustering reuse the same `_data/theme.yml` and `_data/config-map.csv` settings as the full [collection map](maps.md) — see that page for basemap options and popup field configuration.

### Basic usage

```liquid
{% include essay/feature/scrolly-map.html latitude="46.727485" longitude="-117.014185" zoom="5" %}

The map starts centered on the region.

{% include essay/feature/scrolly-step.html map-lat="46.7304" map-lng="-117.0198" map-zoom="15" %}

This panel flies the map to a specific location as it enters view.

{% include essay/feature/scrolly-end.html %}
```

### `scrolly-map.html` parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `objectid` | — | Seeds center/zoom from a collection item's `latitude`/`longitude`; also plots a marker for it |
| `latitude` / `longitude` | `theme.yml` site defaults | Initial map center (required unless using `objectid`) |
| `zoom` | `theme.yml` `zoom-level` (5) | Initial zoom level |
| `basemap` | `theme.yml` `map-base` | `Esri_WorldStreetMap`, `Esri_NatGeoWorldMap`, `Esri_WorldImagery`, `OpenStreetMap_Mapnik`, `Stadia_AlidadeSmooth`, `Stadia_StamenToner` |
| `interactive` | `false` for `immersive`, `true` for `sidecar` | Enable reader drag/scroll-zoom/touch-zoom/keyboard. Always forced off below 768px regardless of this setting. |
| `markers` | — | Comma-separated objectids to plot as a curated marker set, each with a popup |
| `show-collection` | `false` | Plot every geo-tagged item in your metadata CSV as markers — the same selection shown on the full collection map |
| `cluster` | `theme.yml` `map-cluster` | Cluster markers when `show-collection` is used |
| `flyto-duration` | `2` | Default `flyTo` animation duration (seconds) for this block's steps; overridable per step |
| `caption` | — | Small credit/attribution line, same as `scrolly-media.html` |
| `layout` | `immersive` | `immersive` (full-screen) or `sidecar` (side-by-side, map right — see interactivity note below) |
| `position` | `left` | First panel position: `left`, `center`, or `right` |
| `text-background` | `light` | First panel card style: `light` or `dark` |
| `step-height` | `300vh` | Same pacing mechanism as `scrolly-media.html` |

### `scrolly-step.html` map parameters

These are additive to the existing image params on `scrolly-step.html` (`objectid`, `src`, `image-focus`, `animate`, etc.) — use whichever set matches the block type you opened. A step with none of the parameters below leaves the map exactly where it was.

| Parameter | Default | Description |
|-----------|---------|-------------|
| `map-lat` / `map-lng` | — | Target coordinates for this step |
| `map-zoom` | *(keeps current zoom)* | Target zoom level |
| `map-objectid` | — | Resolve the target from a collection item instead of raw coordinates; also the marker featured by `map-open-popup` |
| `map-transition` | `flyTo` | `flyTo` (animated), `setView` (instant), or `pan` (moves center only, no zoom change) |
| `map-basemap` | — | Swap the basemap tile layer on this step |
| `map-open-popup` | — | objectid of a marker to open (or `true` when paired with `map-objectid`) — closes any previously open popup first |
| `map-flyto-duration` | *(inherits block default)* | Per-step override of `flyto-duration` |

### Markers and the full collection

`markers="obj1,obj2"` plots a curated set of collection items as markers with popups (title, thumbnail, and any `_data/config-map.csv` fields, same as the full collection map's popups). `show-collection="true"` instead plots every geo-tagged item in your metadata CSV, respecting `theme.yml`'s `map-child-objects` setting, and can be clustered via `cluster="true"` (or the `theme.yml` `map-cluster` default).

Pairing a step's `map-objectid` with `map-open-popup="true"` flies to that marker and opens its popup automatically — a way to "feature" a specific collection item as the reader scrolls, rather than requiring a click.

### Interactivity

Immersive (full-bleed) map backgrounds default to `interactive="false"` — dragging and scroll-zoom are disabled so the reader's scroll gesture always scrolls the page, not the map. Sidecar map backgrounds default to `interactive="true"` instead, since the pinned map only occupies part of the viewport there and behaves more like an inset, explorable map. Either can be overridden explicitly with `interactive="true"`/`interactive="false"`; interactivity is always disabled below a 768px viewport regardless of this setting, since sidecar collapses to a stacked overlay on mobile.

### Notes

- No RAF-driven continuous scroll-scrubbed panning — map movement is discrete per step (`flyTo`/`setView`/`pan`), triggered when a step enters view, since Leaflet's `flyTo` owns its own animation loop and isn't built to be scrubbed frame-by-frame the way image `animate` zoom/pan is.
- Missing coordinates or a failed Leaflet load render a visible fallback message in place of the map rather than a blank or broken frame.
- Print/PDF output hides the map and shows a "view online" note in its place — Leaflet tiles won't load reliably in the print pipeline.
- Leaflet's CSS/JS are loaded by `scrolly-map.html` itself, only on pages that use it — not on every essay page.

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
{% include feature/card.html objectid="demo_001" %}
```

### Timeline

```liquid
{% include feature/timelinejs.html %}
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
- Default `step-height` is `300vh`; increase to `90vh`–`100vh` for a slower, more meditative pace or decrease to `50vh` for quick transitions
- Test on mobile: both layouts collapse to the same stacked style (image above, text below)
- Avoid nesting scrolly blocks
- Use `image-focus` to keep the subject of an image in frame when using `cover` mode
- Keep animations subtle — `zoom-in` and `ken-burns` work well for archival images; `pan-left`/`pan-right` suit wide panoramas
- Don't apply `animate` to every step; reserve it for panels where movement adds meaning

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
