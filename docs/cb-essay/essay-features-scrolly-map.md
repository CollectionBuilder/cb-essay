# Scrollytelling Map Backgrounds

A scrolly block can use an interactive Leaflet map as its pinned background instead of an image or video — for narrating a journey between locations, detailing a single site as the reader scrolls, or flying around a large tiled image such as a scanned manuscript. Part of the [Essay Features Reference](essay-features.md); for the image/video version of this pattern, see [Scrollytelling Blocks](essay-features-scrolly.md).

Swap `scrolly-media.html` for `scrolly-map.html`; `scrolly-step.html` and `scrolly-end.html` are shared with the image/video blocks — call `scrolly-step.html` with `map-*` parameters instead of `objectid`/`src`, and close with the same `scrolly-end.html`.

Basemaps, center/zoom defaults, and clustering reuse the same `_data/theme.yml` and `_data/config-map.csv` settings as the full [collection map](../maps.md) — see that page for basemap options and popup field configuration.

## Basic usage

```liquid
{% include essay/feature/scrolly-map.html latitude="46.727485" longitude="-117.014185" zoom="5" %}

The map starts centered on the region.

{% include essay/feature/scrolly-step.html map-lat="46.7304" map-lng="-117.0198" map-zoom="15" %}

This panel flies the map to a specific location as it enters view.

{% include essay/feature/scrolly-end.html %}
```

## `scrolly-map.html` parameters

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

## `scrolly-step.html` map parameters

These are additive to the existing image params on `scrolly-step.html` (`objectid`, `src`, `image-focus`, `animate`, etc.) — use whichever set matches the block type you opened. A step with none of the parameters below leaves the map exactly where it was.

| Parameter | Default | Description |
|-----------|---------|-------------|
| `map-lat` / `map-lng` | — | Target coordinates for this step (geographic mode) |
| `map-x` / `map-y` | — | Target pixel coordinates for this step (image mode — see below) |
| `map-zoom` | *(keeps current zoom)* | Target zoom level |
| `map-objectid` | — | Resolve the target from a collection item instead of raw coordinates; also the marker featured by `map-open-popup` (geographic mode) |
| `map-transition` | `flyTo` | `flyTo` (animated), `setView` (instant), or `pan` (moves center only, no zoom change) |
| `map-basemap` | — | Swap the basemap tile layer on this step (geographic mode) |
| `map-open-popup` | — | objectid of a marker to open (or `true` when paired with `map-objectid`) — closes any previously open popup first (geographic mode) |
| `map-marker-label` | — | Drop a labeled pin at this step's target (image mode, `layout="sidecar"` only — see below) |
| `map-flyto-duration` | *(inherits block default)* | Per-step override of `flyto-duration` |

## Markers and the full collection

`markers="obj1,obj2"` plots a curated set of collection items as markers with popups (title, thumbnail, and any `_data/config-map.csv` fields, same as the full collection map's popups). `show-collection="true"` instead plots every geo-tagged item in your metadata CSV, respecting `theme.yml`'s `map-child-objects` setting, and can be clustered via `cluster="true"` (or the `theme.yml` `map-cluster` default).

Pairing a step's `map-objectid` with `map-open-popup="true"` flies to that marker and opens its popup automatically — a way to "feature" a specific collection item as the reader scrolls, rather than requiring a click.

## Interactivity

Immersive (full-bleed) map backgrounds default to `interactive="false"` — dragging and scroll-zoom are disabled so the reader's scroll gesture always scrolls the page, not the map. Sidecar map backgrounds default to `interactive="true"` instead, since the pinned map only occupies part of the viewport there and behaves more like an inset, explorable map. Either can be overridden explicitly with `interactive="true"`/`interactive="false"`; interactivity is always disabled below a 768px viewport regardless of this setting, since sidecar collapses to a stacked overlay on mobile.

## Notes

- No RAF-driven continuous scroll-scrubbed panning — map movement is discrete per step (`flyTo`/`setView`/`pan`), triggered when a step enters view, since Leaflet's `flyTo` owns its own animation loop and isn't built to be scrubbed frame-by-frame the way image `animate` zoom/pan is.
- Missing coordinates or a failed Leaflet load render a visible fallback message in place of the map rather than a blank or broken frame.
- Print/PDF output hides the map and shows a "view online" note in its place — Leaflet tiles won't load reliably in the print pipeline.
- Leaflet's CSS/JS are loaded by `scrolly-map.html` itself, only on pages that use it — not on every essay page.

## Image / Manuscript Basemap

Instead of a geographic basemap, `scrolly-map.html` can fly around a single large tiled image — a scanned manuscript page, a hand-drawn map, a large illustration — so each step lands on a specific region of the image with an explanatory panel. This mode activates when you pass `tile-path` instead of `latitude`/`longitude`.

**Generating tiles:** cut your source image into a standard XYZ tile pyramid with [libvips](https://www.libvips.org/):

```
vips dzsave source.tif assets/tiles/my-manuscript --layout google --suffix .jpg
```

Use `--layout google` (not `--layout zoomify`) so the output folder is a plain XYZ tile pyramid that Leaflet reads natively — no extra plugin required. (libvips nests these as `{z}/{y}/{x}.jpg` — folder per row, file per column — which `scrolly-map.html`'s image mode already expects.) Place the resulting folder under `assets/` so Jekyll copies it as a static asset, and note the source image's pixel `image-width`/`image-height` and the deepest zoom level `vips` produced (`max-zoom`, visible as the highest-numbered subfolder).

```liquid
{% include essay/feature/scrolly-map.html
   tile-path="/assets/tiles/my-manuscript"
   image-width="6200" image-height="4400" max-zoom="6"
   layout="sidecar" %}

The full manuscript page, before scrolling zooms in.

{% include essay/feature/scrolly-step.html map-x="1800" map-y="2600" map-zoom="4"
   map-marker-label="A later marginal correction in a different ink" %}

This panel flies to a specific region of the image, pixel-coordinates from the top-left corner.

{% include essay/feature/scrolly-end.html %}
```

| Parameter | Default | Description |
|-----------|---------|-------------|
| `tile-path` | — | Folder of `{z}/{y}/{x}.jpg` tiles, as produced by `vips dzsave --layout google` (required to activate image mode) |
| `image-width` / `image-height` | — | Native pixel dimensions of the source image (required) |
| `max-zoom` | — | Deepest zoom level present in the tile pyramid (required) |
| `min-zoom` | `0` | Shallowest zoom level |
| `tile-size` | `256` | Tile pixel size |
| `x` / `y` | image center | Initial center point, in native pixel coordinates |
| `zoom` | `min-zoom` | Initial zoom — defaults to the fully zoomed-out view so the reader sees the whole image first |

`scrolly-step.html` takes `map-x` / `map-y` in place of `map-lat` / `map-lng`; `map-zoom`, `map-transition`, and `map-flyto-duration` work the same as geographic mode. `map-basemap` and `map-open-popup` don't apply.

`map-marker-label` drops a labeled pin at that step's landing spot — but **only on `layout="sidecar"`** blocks. Immersive (full-bleed) image maps are text-panel-only by design, since a floating pin doesn't read well behind full-screen text. On sidecar, the pin follows the current step and its popup opens automatically as the reader scrolls; it's a way to call out one specific manuscript feature (a correction, a gloss, an ink change) without cluttering the whole page with permanent markers.

## Best Practices

- Verify coordinates are correct
- Choose appropriate zoom level
- Keep maps relevant to content
- Consider performance impact

## Troubleshooting

### Map doesn't load
- Verify latitude/longitude are valid decimals
- Check zoom level is between 1-18
- Ensure internet connection (uses external map tiles)
- Check browser console for errors

---

**[← Back to Essay Features Reference](essay-features.md)** · **[← Scrollytelling Blocks](essay-features-scrolly.md)**
