---
title: Collection Integration
order: 50
part: Documentation
---

CB-Essay's power comes from integrating collection items with your narrative. This essay shows you how to add your first collection item to an essay using a simple aside (margin note).

---

## The Dual-Collection Model

CB-Essay manages two collections that work together:

1. **Essay Collection** (`_essay/` folder) - Your Markdown essay files with sequential navigation
2. **Object Collection** (CSV in `_data/`) - Digital items (images, PDFs, audio, video) you reference in essays

Reference any collection item in your essays using its `objectid`.

---

## Your First Collection Item

Collection items are stored in a CSV file in `_data/`. Each item needs at minimum:
- `objectid` - Unique identifier (lowercase, no spaces)
- `title` - Item name
- `format` - File type (image/jpeg, application/pdf, etc.)

For complete metadata requirements, see [Collection Integration docs]({{ '/docs.html#collection-integration' | relative_url }}).

---

## Asides with Collection Items

The most common way to add collection items to essays is through asides (margin notes). Let's look at two examples:

### Text-Only Aside

Here's a simple margin note.{% include essay/feature/aside.html text="This aside contains only text - useful for brief explanations or commentary." %} The aside appears in the margin on desktop and inline on mobile.

**Copy this:**
```liquid
{% raw %}{% include essay/feature/aside.html
   text="Your margin note text here" %}{% endraw %}
```

---

### Aside with Collection Item

Moscow's Administration Building{% include essay/feature/aside.html objectid="demo_001" text="Built in 1909, this building still stands on the University of Idaho campus." %} was one of the first permanent structures on campus.

**Copy this:**
```liquid
{% raw %}{% include essay/feature/aside.html
   objectid="demo_001"
   text="Context about this item" %}{% endraw %}
```

The aside automatically shows the item's thumbnail and links to its full page.

**Note:** The `objectid` must exist in your metadata CSV file in `_data/`.

---

## More Aside Options

You can also use asides with:
- **PDFs** - Display document thumbnails
- **Audio/Video** - Show media icons with playback
- **Custom captions** - Override item titles
- **Height control** - Adjust image display size

See the [Essay Features docs]({{ '/docs.html#essay-features' | relative_url }}) for complete aside options and other CollectionBuilder features like item cards, image galleries, timelines, maps, and subject clouds.

---

## Example: Compound Objects

Some items have multiple parts (like a photo album with many images). These are called compound objects.

When you reference a parent objectid, CB automatically knows about its children:{% include essay/feature/aside.html objectid="demo_009" caption="This lookout tower has multiple associated media files" %}

```liquid
{% raw %}{% include essay/feature/aside.html
   objectid="demo_008"
   text="This lookout tower has multiple associated media files" %}{% endraw %}
```

The item page will show all child items together. See the [Compound Objects docs](https://collectionbuilder.github.io/cb-docs/docs/objects/compound-objects/) for details.

---

## Collection Pages

Your CSV metadata automatically creates these pages:
- **Browse** - Grid view of all items
- **Map** - Items with lat/long displayed geographically
- **Timeline** - Items with dates shown chronologically
- **Subjects** - Subject keyword cloud
- **Locations** - Location keyword cloud
- **Data** - Download metadata as CSV/JSON

No additional configuration needed - they work automatically!

---

## Quick Start Workflow

To add collection items to your essays:

1. **Add items to your CSV:** Create or edit `_data/your-metadata.csv` with objectids, titles, and formats
2. **Reference in essays:** Use objectids in asides or other includes
3. **Preview:** Check that objectids resolve correctly

For detailed metadata setup, see the [Get Started guide](03-get-started.html) and [Collection Integration docs]({{ '/docs.html#collection-integration' | relative_url }}).

---

## Best Practices

- Use **descriptive objectids** (`admin_building_1909` not `img001`)
- **Don't overwhelm** your text - 3-5 asides per essay maximum
- Use asides for **supplementary items**, not primary content
- **Optimize images** - 1200px max width recommended
- Provide **alt text** in your metadata for accessibility

---

## Print Considerations

Collection items work beautifully in print PDFs. Asides with images display as margin notes (if using `aside-style: margin`) or inline callouts.

See the [Print Guide]({{ '/docs.html#print-pdf' | relative_url }}) for full details on print output.

---

## Next Steps

You now understand the basics of integrating collection items with CB-Essay!

### Keep Learning

- **[CB-Essay Documentation]({{ '/docs.html' | relative_url }})** - Complete reference including advanced collection features
- **[CB-CSV Documentation](https://collectionbuilder.github.io/cb-docs/)** - CollectionBuilder reference for metadata and visualizations
- **[Metadata Guide](https://collectionbuilder.github.io/cb-docs/docs/metadata/csv_metadata/)** - Detailed field specifications

### Get Help

- **[CB Discussion Forum](https://github.com/CollectionBuilder/collectionbuilder.github.io/discussions)** - Community support
- **[Open an issue](https://github.com/CollectionBuilder/cb-essay/issues)** - Report bugs or request features


---

{% include essay/feature/cta.html text="Use This Template →" link="https://github.com/new?template_name=cb-essay&template_owner=CollectionBuilder" description="You've seen everything CB-Essay can do. Now build something of your own." %}