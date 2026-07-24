# Scrollytelling Blocks

Pin an image in the viewport while multiple narrative text panels scroll over or beside it — the StoryMaps / scrolly-explainer pattern. Useful for manuscript walkthroughs, archival photo essays, site surveys, or any story where a visual needs to anchor the reader while text builds around it. Part of the [Essay Features Reference](essay-features.md); for a Leaflet map instead of an image, see [Scrollytelling Map Backgrounds](essay-features-scrolly-map.md).

A scrolly block requires three paired includes:

1. **`scrolly-media.html`** — opens the block and sets the first (pinned) image
2. **`scrolly-step.html`** — adds each subsequent text panel (optionally swapping the image)
3. **`scrolly-end.html`** — closes the block and returns to normal essay flow

## Immersive layout (default)

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

## Sidecar layout

Image stays fixed on the right; text panels scroll on the left. Collapses to stacked on mobile.

```liquid
{% include essay/feature/scrolly-media.html objectid="photo_001" layout="sidecar" %}

Text panel beside the image.

{% include essay/feature/scrolly-step.html objectid="photo_002" %}

Second panel; image swaps on the right.

{% include essay/feature/scrolly-end.html %}
```

## Using direct image paths instead of objectids

```liquid
{% include essay/feature/scrolly-media.html
   src="/assets/img/my-photo.jpg"
   alt="Description of the image"
   caption="Credit: University Archives" %}
```

## `scrolly-media.html` parameters

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

## `scrolly-step.html` parameters

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

## `scrolly-end.html` parameters

None. Just closes the block.

## Image focus and animation

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

## Controlling step duration

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

## Layout notes

**Immersive:** The sticky image fills the full viewport. Text cards float over it. After the last panel, the block adds a full viewport of blank space so the image scrolls cleanly off screen before the next essay content appears.

**Sidecar:** Text scrolls on the left (45% width), image stays fixed on the right (55% width). The same full-viewport bottom padding keeps the image sticky through all panels. On mobile both layouts collapse to the same stacked style: image at top, text scrolling below.

## Scroll direction

Scrolling back up restores the correct image automatically — each panel's "effective image" (the last image defined at or before that point in the block) is pre-computed at page load, so forward and backward scrolling always show the right visual.

## Notes

- Always close every block with `scrolly-end.html` — an unclosed block breaks the essay layout.
- Steps without `objectid`/`src` keep the previously shown image.
- Multiple scrolly blocks on one page work independently.
- Print output renders the initial image once, then all panel text inline beneath it.
- Disable Scrollama on an essay page with `scrollama: false` in front matter — scrolly blocks won't animate but render as readable static content.

## Best Practices

- Always close with `scrolly-end.html` — unclosed blocks break the essay layout
- Use landscape-oriented images (16:9 or wider) for best results in immersive; portrait works well in sidecar
- Keep panel text concise (2-4 sentences); readers are processing the image at the same time
- Default `step-height` is `300vh`; increase to `90vh`–`100vh` for a slower, more meditative pace or decrease to `50vh` for quick transitions
- Test on mobile: both layouts collapse to the same stacked style (image above, text below)
- Avoid nesting scrolly blocks
- Use `image-focus` to keep the subject of an image in frame when using `cover` mode
- Keep animations subtle — `zoom-in` and `ken-burns` work well for archival images; `pan-left`/`pan-right` suit wide panoramas
- Don't apply `animate` to every step; reserve it for panels where movement adds meaning

---

**[← Back to Essay Features Reference](essay-features.md)** · **[→ Scrollytelling Map Backgrounds](essay-features-scrolly-map.md)**
