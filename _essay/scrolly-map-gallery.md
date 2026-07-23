---
title: Scrolly Map Gallery
order: 1001
hide_from_nav: true
---

Every `scrolly-map.html` transition, basemap switch, and marker option, demonstrated live with the exact code that produced it. Start with [Scroll-Based Features](05-scroll-features.html) if you haven't seen the basic pattern yet.

A scrolly block can use an interactive Leaflet map as its pinned background instead of an image or video — useful for narrating a journey between locations, or detailing a single site as the reader scrolls. Swap `scrolly-media.html` for `scrolly-map.html`; `scrolly-step.html` and `scrolly-end.html` are shared with the image/video blocks, just called with `map-*` parameters instead of `objectid`/`src`.

The eight examples below each demonstrate one capability in isolation.

---

## 1. Basic flyTo between two locations

Each step on a map block can declare a `map-lat`/`map-lng`/`map-zoom` to fly to. The default transition is an animated `flyTo`.

{% include essay/feature/scrolly-map.html latitude="46.725562" longitude="-117.009633" zoom="12" caption="Moscow, Idaho → Hell's Half Acre Lookout" %}

**Starting over the University of Idaho campus** in Moscow, Idaho.

{% include essay/feature/scrolly-step.html map-lat="45.64579" map-lng="-114.62838" map-zoom="10" %}

**The map flies to Hell's Half Acre Lookout**, roughly 100 miles southeast, as this panel enters view — no page reload, no image swap, just an animated `flyTo`.

{% include essay/feature/scrolly-end.html %}

**Copy this:**
```liquid
{% raw %}{% include essay/feature/scrolly-map.html latitude="46.725562" longitude="-117.009633" zoom="12" caption="Moscow, Idaho → Hell's Half Acre Lookout" %}

**Starting over the University of Idaho campus** in Moscow, Idaho.

{% include essay/feature/scrolly-step.html map-lat="45.64579" map-lng="-114.62838" map-zoom="10" %}

**The map flies to Hell's Half Acre Lookout**, roughly 100 miles southeast, as this panel enters view — no page reload, no image swap, just an animated `flyTo`.

{% include essay/feature/scrolly-end.html %}{% endraw %}
```

---

## 2. Instant `setView` vs. animated `flyTo`

`map-transition` controls how the map gets to a step's target: `setView` jumps instantly, `flyTo` (the default) animates.

{% include essay/feature/scrolly-map.html latitude="46.725562" longitude="-117.009633" zoom="6" %}

**Watch the transition style on the next two panels** — one jumps, the other flies.

{% include essay/feature/scrolly-step.html map-lat="47.66432" map-lng="-117.428031" map-zoom="11" map-transition="setView" %}

**Instant jump.** `map-transition="setView"` snaps straight to Spokane with no animation — useful when you want an abrupt cut rather than a journey.

{% include essay/feature/scrolly-step.html map-lat="45.64579" map-lng="-114.62838" map-zoom="10" map-transition="flyTo" %}

**Animated flight.** The default `flyTo` (set explicitly here) glides to Hell's Half Acre Lookout instead of cutting to it.

{% include essay/feature/scrolly-end.html %}

**Copy this:**
```liquid
{% raw %}{% include essay/feature/scrolly-map.html latitude="46.725562" longitude="-117.009633" zoom="6" %}

**Watch the transition style on the next two panels** — one jumps, the other flies.

{% include essay/feature/scrolly-step.html map-lat="47.66432" map-lng="-117.428031" map-zoom="11" map-transition="setView" %}

**Instant jump.** `map-transition="setView"` snaps straight to Spokane with no animation — useful when you want an abrupt cut rather than a journey.

{% include essay/feature/scrolly-step.html map-lat="45.64579" map-lng="-114.62838" map-zoom="10" map-transition="flyTo" %}

**Animated flight.** The default `flyTo` (set explicitly here) glides to Hell's Half Acre Lookout instead of cutting to it.

{% include essay/feature/scrolly-end.html %}{% endraw %}
```

---

## 3. `pan` transition

`map-transition="pan"` moves the center without changing zoom — a Leaflet `panTo`, useful for small repositions that shouldn't feel like a "flight."

{% include essay/feature/scrolly-map.html latitude="46.725562" longitude="-117.009633" zoom="13" %}

**Centered on campus at a fixed zoom.**

{% include essay/feature/scrolly-step.html map-lat="46.714253" map-lng="-116.983777" map-transition="pan" %}

**A short pan** slides the view toward downtown Moscow without zooming in or out — the frame stays the same size, only the center moves.

{% include essay/feature/scrolly-end.html %}

**Copy this:**
```liquid
{% raw %}{% include essay/feature/scrolly-map.html latitude="46.725562" longitude="-117.009633" zoom="13" %}

**Centered on campus at a fixed zoom.**

{% include essay/feature/scrolly-step.html map-lat="46.714253" map-lng="-116.983777" map-transition="pan" %}

**A short pan** slides the view toward downtown Moscow without zooming in or out — the frame stays the same size, only the center moves.

{% include essay/feature/scrolly-end.html %}{% endraw %}
```

---

## 4. Basemap switching mid-scroll

`map-basemap` on a step swaps the tile layer as it enters view — useful for moving from a street map into satellite imagery to reveal terrain.

{% include essay/feature/scrolly-map.html latitude="45.64579" longitude="-114.62838" zoom="12" basemap="Esri_WorldStreetMap" %}

**Starting on the default street basemap.**

{% include essay/feature/scrolly-step.html map-basemap="Esri_WorldImagery" %}

**Switching to satellite imagery** with `map-basemap="Esri_WorldImagery"` reveals the surrounding forest terrain around the lookout without moving the map.

{% include essay/feature/scrolly-end.html %}

**Copy this:**
```liquid
{% raw %}{% include essay/feature/scrolly-map.html latitude="45.64579" longitude="-114.62838" zoom="12" basemap="Esri_WorldStreetMap" %}

**Starting on the default street basemap.**

{% include essay/feature/scrolly-step.html map-basemap="Esri_WorldImagery" %}

**Switching to satellite imagery** with `map-basemap="Esri_WorldImagery"` reveals the surrounding forest terrain around the lookout without moving the map.

{% include essay/feature/scrolly-end.html %}{% endraw %}
```

---

## 5. Curated markers with auto-opening popups

`markers` takes a comma-separated list of objectids and plots each as a marker. Pair a step's `map-objectid` with `map-open-popup="true"` to fly to a marker and open its popup automatically — a way to "feature" specific collection items as the reader scrolls.

{% include essay/feature/scrolly-map.html latitude="47.66" longitude="-117.43" zoom="11" markers="demo_002,demo_018" %}

**Two Spokane locations are plotted** as markers from the start. Scroll to feature each one.

{% include essay/feature/scrolly-step.html map-objectid="demo_002" map-open-popup="true" map-zoom="15" %}

**Featuring the Spokane County Court House** — the map flies in and its popup opens on its own, no click required.

{% include essay/feature/scrolly-step.html map-objectid="demo_018" map-open-popup="true" map-zoom="15" %}

**Featuring the second location** — the previous popup closes and this marker's popup opens as the map flies over.

{% include essay/feature/scrolly-end.html %}

**Copy this:**
```liquid
{% raw %}{% include essay/feature/scrolly-map.html latitude="47.66" longitude="-117.43" zoom="11" markers="demo_002,demo_018" %}

**Two Spokane locations are plotted** as markers from the start. Scroll to feature each one.

{% include essay/feature/scrolly-step.html map-objectid="demo_002" map-open-popup="true" map-zoom="15" %}

**Featuring the Spokane County Court House** — the map flies in and its popup opens on its own, no click required.

{% include essay/feature/scrolly-step.html map-objectid="demo_018" map-open-popup="true" map-zoom="15" %}

**Featuring the second location** — the previous popup closes and this marker's popup opens as the map flies over.

{% include essay/feature/scrolly-end.html %}{% endraw %}
```

---

## 6. The whole collection as markers

`show-collection="true"` plots every geo-tagged item in your metadata CSV — the same items shown on the full collection map page — directly on the scrolly background.

{% include essay/feature/scrolly-map.html latitude="46.7" longitude="-117.0" zoom="5" show-collection=true %}

**Every geo-tagged demo item appears as a marker** on this regional view — no need to list objectids one at a time.

{% include essay/feature/scrolly-step.html map-lat="46.0" map-lng="-116.0" map-zoom="6" %}

**Flying south** still keeps every collection marker visible on the map underneath.

{% include essay/feature/scrolly-end.html %}

**Copy this:**
```liquid
{% raw %}{% include essay/feature/scrolly-map.html latitude="46.7" longitude="-117.0" zoom="5" show-collection=true %}

**Every geo-tagged demo item appears as a marker** on this regional view — no need to list objectids one at a time.

{% include essay/feature/scrolly-step.html map-lat="46.0" map-lng="-116.0" map-zoom="6" %}

**Flying south** still keeps every collection marker visible on the map underneath.

{% include essay/feature/scrolly-end.html %}{% endraw %}
```

---

## 7. Interactive sidecar map

`layout="sidecar"` pins the map on the right at a smaller scale and, unlike the full-bleed `immersive` layout, defaults to `interactive="true"` — the reader can drag and scroll-zoom it directly, since it's no longer competing with the page for the whole viewport's scroll gesture.

{% include essay/feature/scrolly-map.html objectid="demo_001" layout="sidecar" zoom="14" %}

**This map is explorable.** Try dragging or scrolling to zoom — sidecar's smaller, inset frame makes that safe without hijacking the page scroll. (Interactivity is automatically disabled on narrow/mobile screens, where sidecar collapses to a stacked overlay.)

{% include essay/feature/scrolly-step.html map-lat="46.714253" map-lng="-116.983777" map-zoom="13" %}

**Steps still drive the map** even in sidecar mode — this panel flies toward downtown Moscow, and the reader can keep exploring from there.

{% include essay/feature/scrolly-end.html %}

**Copy this:**
```liquid
{% raw %}{% include essay/feature/scrolly-map.html objectid="demo_001" layout="sidecar" zoom="14" %}

**This map is explorable.** Try dragging or scrolling to zoom — sidecar's smaller, inset frame makes that safe without hijacking the page scroll. (Interactivity is automatically disabled on narrow/mobile screens, where sidecar collapses to a stacked overlay.)

{% include essay/feature/scrolly-step.html map-lat="46.714253" map-lng="-116.983777" map-zoom="13" %}

**Steps still drive the map** even in sidecar mode — this panel flies toward downtown Moscow, and the reader can keep exploring from there.

{% include essay/feature/scrolly-end.html %}{% endraw %}
```

---

## 8. `objectid`-seeded block

Instead of raw coordinates, `scrolly-map.html` can seed its center and an initial marker straight from a collection item's `latitude`/`longitude` — the same convenience `feature/mini-map.html` offers.

{% include essay/feature/scrolly-map.html objectid="demo_008" zoom="13" %}

**Centered automatically on Hell's Half Acre Lookout**, with a marker for `demo_008` already plotted, just from passing `objectid="demo_008"` — no coordinates typed by hand.

{% include essay/feature/scrolly-step.html map-zoom="16" %}

**A step can still move the map** even when the block was seeded by `objectid` — this panel zooms in further without changing the center.

{% include essay/feature/scrolly-end.html %}

**Copy this:**
```liquid
{% raw %}{% include essay/feature/scrolly-map.html objectid="demo_008" zoom="13" %}

**Centered automatically on Hell's Half Acre Lookout**, with a marker for `demo_008` already plotted, just from passing `objectid="demo_008"` — no coordinates typed by hand.

{% include essay/feature/scrolly-step.html map-zoom="16" %}

**A step can still move the map** even when the block was seeded by `objectid` — this panel zooms in further without changing the center.

{% include essay/feature/scrolly-end.html %}{% endraw %}
```

---

## All Parameters

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

**[→ Scrolly Media Gallery](scrolly-media-gallery.html)** — every animation, layout, and video variant.

**[← Back to Scroll-Based Features](05-scroll-features.html)**
