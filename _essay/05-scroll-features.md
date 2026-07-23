---
title: Scroll-Based Features
order: 45
part: Documentation
---

CB-Essay's scrollytelling blocks pin an image in the viewport while narrative panels scroll over or beside it. Scroll slowly through each section below to see the effects in action — the demos are live, not screenshots.

Every block follows the same three-include pattern:

```liquid
{% raw %}{% include essay/feature/scrolly-media.html objectid="your_image" %}

First panel text.

{% include essay/feature/scrolly-step.html objectid="next_image" %}

Second panel text.

{% include essay/feature/scrolly-end.html %}{% endraw %}
```

---

## Immersive Layout

The **immersive layout** fills the full viewport with a pinned image. Panels float over it in frosted cards. Scroll slowly and watch the panel fade in when it crosses the trigger line.

{% include essay/feature/scrolly-media.html objectid="demo_001" alt="Administration Building, University of Idaho, ca. 1910" %}

**Left panel** is the default. The card appears on the left side of the frame with a light semi-transparent background.

{% include essay/feature/scrolly-step.html position="center" %}

**Center panel.** Add `position="center"` to center the card — useful for brief captions or dramatic statements.

{% include essay/feature/scrolly-step.html objectid="demo_009" position="right" text-background="dark" %}

**Right panel with dark card.** `position="right" text-background="dark"` shifts the card right and inverts it. The image swaps as this panel enters view.

{% include essay/feature/scrolly-end.html %}

**Parameters for panel position and style:**

| `position` | `text-background` | Effect |
|---|---|---|
| `left` (default) | `light` (default) | White card, left side |
| `center` | `light` | White card, centered |
| `right` | `dark` | Dark card, right side |

---

## Zoom In

`animate="zoom-in"` zooms the image toward a point as you scroll through the panel. The zoom amount is directly proportional to scroll position — there is no timer.

{% include essay/feature/scrolly-media.html objectid="demo_031" animate="zoom-in" %}

Scroll through this panel slowly and watch the image zoom in. Fast scrolling zooms fast; pausing holds the image at whatever zoom level you've reached.

{% include essay/feature/scrolly-step.html objectid="demo_011" animate="zoom-in" image-focus="60% 30%" %}

A new image, with `image-focus="60% 30%"` added. The zoom now targets the upper portion of the frame. Use `image-focus` with `zoom-in` to pull your reader's attention toward a specific subject in the photograph.

{% include essay/feature/scrolly-end.html %}

---

## Zoom Out

`animate="zoom-out"` starts the image zoomed in and pulls back as you scroll — useful for establishing shots that open from a close detail to wider context.

{% include essay/feature/scrolly-media.html objectid="demo_033" animate="zoom-out" %}

The image begins close and expands outward. This reversal creates a sense of revelation — arriving at a scene from a detail rather than entering it from a distance.

{% include essay/feature/scrolly-end.html %}

---

## Pan Left / Pan Right

Pan animations sweep the image horizontally as you scroll. Best suited to wide panoramas or long horizontal documents where content is distributed across the frame.

{% include essay/feature/scrolly-media.html objectid="demo_001" animate="pan-right" %}

**Pan right** — the image travels from its left edge to its right edge as you scroll. Slow your scrolling and you'll see the pan slow with you.

{% include essay/feature/scrolly-step.html objectid="demo_009" animate="pan-left" %}

**Pan left** — this panel swaps to a new image and pans in the opposite direction. Alternating directions between panels creates a reading rhythm that feels intentional.

{% include essay/feature/scrolly-end.html %}

---

## Ken Burns

`animate="ken-burns"` combines a slow zoom with a diagonal pan. It uses a preset lower-left → upper-right trajectory and is the effect to reach for when you want motion without needing precise control over the direction.

{% include essay/feature/scrolly-media.html objectid="demo_033" animate="ken-burns" %}

The Ken Burns effect gives archival photographs a sense of life without calling attention to itself. It works best with images that have rich detail throughout the frame rather than a single focal point.

{% include essay/feature/scrolly-step.html objectid="demo_001" animate="ken-burns" step-height="1150vh" %}

Each panel with `animate="ken-burns"` resets to the start of the diagonal drift when it enters view. The motion always begins from the same position regardless of where the previous panel left off.

{% include essay/feature/scrolly-end.html %}

---

## Focus Point

`image-focus` controls which part of the image is visible in `cover` mode and sets the target point for zoom animations. The value is any CSS `object-position` — `"center"`, `"top"`, `"80% 30%"`, etc.

{% include essay/feature/scrolly-media.html objectid="demo_031" image-focus="15% 50%" %}

**Static focus.** `image-focus="15% 50%"` keeps the left portion of the image in frame. Without an animation, this is a static crop — no motion, just a different window into the image.

{% include essay/feature/scrolly-step.html objectid="demo_031" animate="zoom-in" image-focus="15% 50%" %}

**Zoom toward the focus.** The same focus point, now with `animate="zoom-in"`. The zoom pulls inward toward the left edge. The reader's eye is drawn to the same spot that `image-focus` framed.

{% include essay/feature/scrolly-step.html objectid="demo_031" animate="zoom-in" image-focus="85% 50%" %}

**Opposite corner.** The focus point flips to the right side. Each panel can redirect the zoom to a different part of the same image — a way to narrate across a photograph without swapping it.

{% include essay/feature/scrolly-end.html %}

---

## Sidecar Layout

The **sidecar layout** pins the image on the right while text panels scroll on the left. Images use `object-fit: contain` by default so the full document is always visible — no cropping. Collapses to the immersive stacked style on mobile.

{% include essay/feature/scrolly-media.html objectid="demo_019" layout="sidecar" %}

The front side of an archival postcard. Sidecar is well suited to objects with multiple sides, facing pages, or before/after states — the reader can follow your commentary while the relevant image holds steady.

{% include essay/feature/scrolly-step.html objectid="demo_020" %}

The reverse side. Swapping images in sidecar feels like turning a page — the text panel advances the story while the image on the right catches up.

{% include essay/feature/scrolly-end.html %}

Sidecar also accepts `animate` parameters — `animate="zoom-in"` on a sidecar step zooms into the pinned image on the right while the text scrolls on the left.

---

## Map Background

A scrolly block can use an interactive Leaflet map as its pinned background instead of an image or video — useful for narrating a journey between locations, or detailing a single site as the reader scrolls. Swap `scrolly-media.html` for `scrolly-map.html`; `scrolly-step.html` and `scrolly-end.html` are shared with the image/video blocks, just called with `map-*` parameters instead of `objectid`/`src`.

The eight examples below each demonstrate one capability in isolation.

### 1. Basic flyTo between two locations

Each step on a map block can declare a `map-lat`/`map-lng`/`map-zoom` to fly to. The default transition is an animated `flyTo`.

{% include essay/feature/scrolly-map.html latitude="46.725562" longitude="-117.009633" zoom="12" caption="Moscow, Idaho → Hell's Half Acre Lookout" %}

**Starting over the University of Idaho campus** in Moscow, Idaho.

{% include essay/feature/scrolly-step.html map-lat="45.64579" map-lng="-114.62838" map-zoom="10" %}

**The map flies to Hell's Half Acre Lookout**, roughly 100 miles southeast, as this panel enters view — no page reload, no image swap, just an animated `flyTo`.

{% include essay/feature/scrolly-end.html %}

### 2. Instant `setView` vs. animated `flyTo`

`map-transition` controls how the map gets to a step's target: `setView` jumps instantly, `flyTo` (the default) animates.

{% include essay/feature/scrolly-map.html latitude="46.725562" longitude="-117.009633" zoom="6" %}

**Watch the transition style on the next two panels** — one jumps, the other flies.

{% include essay/feature/scrolly-step.html map-lat="47.66432" map-lng="-117.428031" map-zoom="11" map-transition="setView" %}

**Instant jump.** `map-transition="setView"` snaps straight to Spokane with no animation — useful when you want an abrupt cut rather than a journey.

{% include essay/feature/scrolly-step.html map-lat="45.64579" map-lng="-114.62838" map-zoom="10" map-transition="flyTo" %}

**Animated flight.** The default `flyTo` (set explicitly here) glides to Hell's Half Acre Lookout instead of cutting to it.

{% include essay/feature/scrolly-end.html %}

### 3. `pan` transition

`map-transition="pan"` moves the center without changing zoom — a Leaflet `panTo`, useful for small repositions that shouldn't feel like a "flight."

{% include essay/feature/scrolly-map.html latitude="46.725562" longitude="-117.009633" zoom="13" %}

**Centered on campus at a fixed zoom.**

{% include essay/feature/scrolly-step.html map-lat="46.714253" map-lng="-116.983777" map-transition="pan" %}

**A short pan** slides the view toward downtown Moscow without zooming in or out — the frame stays the same size, only the center moves.

{% include essay/feature/scrolly-end.html %}

### 4. Basemap switching mid-scroll

`map-basemap` on a step swaps the tile layer as it enters view — useful for moving from a street map into satellite imagery to reveal terrain.

{% include essay/feature/scrolly-map.html latitude="45.64579" longitude="-114.62838" zoom="12" basemap="Esri_WorldStreetMap" %}

**Starting on the default street basemap.**

{% include essay/feature/scrolly-step.html map-basemap="Esri_WorldImagery" %}

**Switching to satellite imagery** with `map-basemap="Esri_WorldImagery"` reveals the surrounding forest terrain around the lookout without moving the map.

{% include essay/feature/scrolly-end.html %}

### 5. Curated markers with auto-opening popups

`markers` takes a comma-separated list of objectids and plots each as a marker. Pair a step's `map-objectid` with `map-open-popup="true"` to fly to a marker and open its popup automatically — a way to "feature" specific collection items as the reader scrolls.

{% include essay/feature/scrolly-map.html latitude="47.66" longitude="-117.43" zoom="11" markers="demo_002,demo_018" %}

**Two Spokane locations are plotted** as markers from the start. Scroll to feature each one.

{% include essay/feature/scrolly-step.html map-objectid="demo_002" map-open-popup="true" map-zoom="15" %}

**Featuring the Spokane County Court House** — the map flies in and its popup opens on its own, no click required.

{% include essay/feature/scrolly-step.html map-objectid="demo_018" map-open-popup="true" map-zoom="15" %}

**Featuring the second location** — the previous popup closes and this marker's popup opens as the map flies over.

{% include essay/feature/scrolly-end.html %}

### 6. The whole collection as markers

`show-collection="true"` plots every geo-tagged item in your metadata CSV — the same items shown on the full collection map page — directly on the scrolly background.

{% include essay/feature/scrolly-map.html latitude="46.7" longitude="-117.0" zoom="5" show-collection=true %}

**Every geo-tagged demo item appears as a marker** on this regional view — no need to list objectids one at a time.

{% include essay/feature/scrolly-step.html map-lat="46.0" map-lng="-116.0" map-zoom="6" %}

**Flying south** still keeps every collection marker visible on the map underneath.

{% include essay/feature/scrolly-end.html %}

### 7. Interactive sidecar map

`layout="sidecar"` pins the map on the right at a smaller scale and, unlike the full-bleed `immersive` layout, defaults to `interactive="true"` — the reader can drag and scroll-zoom it directly, since it's no longer competing with the page for the whole viewport's scroll gesture.

{% include essay/feature/scrolly-map.html objectid="demo_001" layout="sidecar" zoom="14" %}

**This map is explorable.** Try dragging or scrolling to zoom — sidecar's smaller, inset frame makes that safe without hijacking the page scroll. (Interactivity is automatically disabled on narrow/mobile screens, where sidecar collapses to a stacked overlay.)

{% include essay/feature/scrolly-step.html map-lat="46.714253" map-lng="-116.983777" map-zoom="13" %}

**Steps still drive the map** even in sidecar mode — this panel flies toward downtown Moscow, and the reader can keep exploring from there.

{% include essay/feature/scrolly-end.html %}

### 8. `objectid`-seeded block

Instead of raw coordinates, `scrolly-map.html` can seed its center and an initial marker straight from a collection item's `latitude`/`longitude` — the same convenience `feature/mini-map.html` offers.

{% include essay/feature/scrolly-map.html objectid="demo_008" zoom="13" %}

**Centered automatically on Hell's Half Acre Lookout**, with a marker for `demo_008` already plotted, just from passing `objectid="demo_008"` — no coordinates typed by hand.

{% include essay/feature/scrolly-step.html map-zoom="16" %}

**A step can still move the map** even when the block was seeded by `objectid` — this panel zooms in further without changing the center.

{% include essay/feature/scrolly-end.html %}

---

## Video Background

Video backgrounds work through the same `objectid` and `src` params as images — no separate parameter needed. The include detects video automatically from the collection item's `display_template` or from the file extension (`.mp4`, `.webm`, `.ogg`).

**From the collection** — set `display_template: video` on the item in your metadata CSV:

```liquid
{% raw %}{% include essay/feature/scrolly-media.html objectid="demo_video_001" %}{% endraw %}
```

The item's `image_small` is used as the poster frame automatically.

**From a direct file path** — point `src` at any `.mp4`, `.webm`, or `.ogg` file:

```liquid
{% raw %}{% include essay/feature/scrolly-media.html src="/assets/video/bg.mp4" poster="/assets/img/bg-poster.jpg" %}{% endraw %}
```

`poster` is optional but recommended for direct paths — it prevents a blank background while the video loads. The video autoplays, loops, and is muted (required for browser autoplay). All layouts, `image-focus`, and scroll-linked animations work exactly as they do for images.

Step-swapping via `objectid` or `src` on `scrolly-step.html` is not available when a video background is active; the video plays continuously through all steps.

 
{% include essay/feature/scrolly-media.html objectid="demo_010" video-start="10" %}

This is a video that isn't very exciting but you can see it working here ... 

You might need to wait awhile to let it play. Probably better to use this feature sparingly in only specific cases -- and we don't have sound ... 

{% include essay/feature/scrolly-end.html %}

---

## Controlling Scroll Speed

`step-height` sets the minimum height of each panel — how far the reader must scroll before the next panel triggers. The CSS default is `300vh`. Shorter values create faster pacing; longer values slow reading down.

Set it on `scrolly-media.html` to apply across the whole block, or on individual `scrolly-step.html` calls to vary the pace within a block:

```liquid
{% raw %}{% include essay/feature/scrolly-media.html objectid="your_image" step-height="150vh" %}

Quick panel — moves through in half the default scroll distance.

{% include essay/feature/scrolly-step.html objectid="another_image" step-height="500vh" %}

Slow panel — the reader lingers before the next image enters.

{% include essay/feature/scrolly-end.html %}{% endraw %}
```

For scroll-linked animations (`zoom-in`, `pan-right`, etc.), longer `step-height` means the animation plays out more gradually — the full zoom or pan happens over a greater scroll distance.

---

## All Parameters

**`scrolly-media.html`** — opens the block:

{:.table .table-striped}
| Parameter | Default | Description |
|---|---|---|
| `objectid` | — | Collection item ID; video detected automatically from `display_template` |
| `src` | — | Direct path to an image or video file (`.mp4`, `.webm`, `.ogg` auto-detected) |
| `poster` | — | Poster frame for `src`-based videos (collection items use `image_small` automatically) |
| `video-start` | — | Start time in seconds for video backgrounds; also applied on every loop restart |
| `alt` | — | Image alt text |
| `caption` | — | Small credit line at bottom-right of image |
| `layout` | `immersive` | `immersive` or `sidecar` |
| `position` | `left` | First panel position: `left`, `center`, `right` |
| `text-background` | `light` | First panel style: `light` or `dark` |
| `step-height` | `300vh` | Minimum scroll height per panel |
| `image-focus` | `center` | CSS `object-position` value; also sets zoom target |
| `animate` | — | `zoom-in`, `zoom-out`, `pan-left`, `pan-right`, `ken-burns` |

**`scrolly-step.html`** — adds a panel (same parameters except `layout`):

`image-focus` and `animate` on a step override the opening values for that panel only. Steps without these parameters keep the current image and no animation.

**`scrolly-end.html`** — no parameters. Always required to close the block, for image/video and map backgrounds alike.

---

**`scrolly-map.html`** — opens a map-background block (used instead of `scrolly-media.html`):

{:.table .table-striped}
| Parameter | Default | Description |
|---|---|---|
| `objectid` | — | Seeds center/zoom from a collection item's `latitude`/`longitude`; also plots a marker for it |
| `latitude` / `longitude` | theme.yml site defaults | Initial map center (required unless using `objectid`) |
| `zoom` | theme.yml `zoom-level` (5) | Initial zoom level |
| `basemap` | theme.yml `map-base` | `Esri_WorldStreetMap`, `Esri_NatGeoWorldMap`, `Esri_WorldImagery`, `OpenStreetMap_Mapnik`, `Stadia_AlidadeSmooth`, `Stadia_StamenToner` |
| `interactive` | `false` (`immersive`) / `true` (`sidecar`) | Enable reader drag/scroll-zoom/touch-zoom (always off on mobile) |
| `markers` | — | Comma-separated objectids to plot as a curated marker set |
| `show-collection` | `false` | Plot every geo-tagged collection item as markers |
| `cluster` | theme.yml `map-cluster` | Cluster markers when `show-collection` is used |
| `flyto-duration` | `2` | Default flyTo animation duration (seconds) for this block's steps |
| `caption` | — | Small credit/attribution line, same as `scrolly-media.html` |
| `layout`, `position`, `text-background`, `step-height` | same as `scrolly-media.html` | Panel layout and pacing |

**`scrolly-step.html`** — map-specific parameters (used alongside a `scrolly-map.html` block; a step with none of these leaves the map wherever it was):

{:.table .table-striped}
| Parameter | Description |
|---|---|
| `map-lat` / `map-lng` | Target coordinates for this step |
| `map-zoom` | Target zoom (keeps current zoom if omitted) |
| `map-objectid` | Resolve the target from a collection item instead of raw coordinates |
| `map-transition` | `flyTo` (default, animated), `setView` (instant), or `pan` (moves center only, no zoom change) |
| `map-basemap` | Swap the basemap tile layer on this step |
| `map-open-popup` | objectid of a marker to open (or `true` when paired with `map-objectid`) |
| `map-flyto-duration` | Per-step override of the block's `flyto-duration` |

---

## Next Steps

**[Collection Integration →](06-collection-integration.html)**
