# Mini Map & Reusing CollectionBuilder Features

A small embedded map for a single coordinate, plus a reminder that every standard CollectionBuilder feature include is still available inside an essay. Part of the [Essay Features Reference](essay-features.md).

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

For a map that flies between locations (or around a large tiled image) as the reader scrolls, see [Scrollytelling Map Backgrounds](essay-features-scrolly-map.md) instead.

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

## Best Practices

- Verify coordinates are correct
- Choose appropriate zoom level
- Keep maps relevant to content
- Consider performance impact

---

**[← Back to Essay Features Reference](essay-features.md)**
