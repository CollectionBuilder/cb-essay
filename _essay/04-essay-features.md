---
title: Writing Features
order: 40
part: Documentation
---

CB-Essay provides specialized includes that extend Markdown for scholarly writing. This essay **demonstrates every feature** with working examples you can copy directly into your own work.

**The copy-and-replace principle:** Find a feature you like, copy the code block, paste it into your essay, and replace the content with yours. That's it!

## Basic Markdown

Like all CollectionBuilder content pages, CB-Essay uses markdown for basic writing options: 

### Headings

```markdown
## Heading 2
### Heading 3
#### Heading 4
```

### Text Formatting

**Bold text** with `**bold**`

*Italic text* with `*italic*`

***Bold italic*** with `***bold italic***`

### Links

[Link text](https://example.com) with `[text](url)`

Check out CB's [Markdown glossary entry](https://collectionbuilder.github.io/cb-docs/docs/glossary/#markdown) for resources and tutorials!



## Asides (Margin Notes)

Margin notes appear beside your text on desktop, inline on mobile.

### Text-Only Aside

Here's a paragraph with a margin note.{% include essay/feature/aside.html text="This is a margin note providing additional context or commentary." %} The text continues naturally, and the aside appears in the margin.

**Copy this:**
```liquid
{% raw %}{% include essay/feature/aside.html
   text="Your margin note text here" %}{% endraw %}
```

### Aside with Collection Item

Collection items can appear in asides with thumbnails.{% include essay/feature/aside.html objectid="demo_001" text="This manuscript shows early draft revisions." %} The aside shows a preview of the item with a link to view it.

**Copy this:**
```liquid
{% raw %}{% include essay/feature/aside.html
   objectid="demo_001"
   text="Context about this item" %}{% endraw %}
```

**Note:** The `objectid` must exist in your collection metadata CSV file.

---

## Media Galleries

Display collection items that, when clicked, appear in modal galleries.

{% include essay/feature/image-gallery.html
   objectid="demo_033;demo_031;demo_017" caption=false%}

**Copy this:**
```liquid
{% raw %}{% include essay/feature/image-gallery.html
   objectid="item1;item2;item3" %}{% endraw %}
```

Separate multiple object IDs with semicolons. Items must exist in your metadata.

## Filtered Collection Galleries

Below is another type of gallery, one that is filtered from the collection based on liquid logic (here it is `item.format contains 'image' and item.date > '1920'`) with an optional header.

{% include feature/gallery.html 
   heading="Items Dated after 1920"  
   captions=false 
   filter="item.date > '1920'" %}

**Copy this:**
```liquid
{% raw %}{% include feature/gallery.html 
   heading="Items Dated after 1920"  
   captions=false 
   filter="item.date > '1920'" %}{% endraw %}
```

---


## Blockquotes

Styled quotations with optional attribution and source links.

### Basic Blockquote

{% include essay/feature/blockquote.html
   quote="Knowledge comes, but wisdom lingers"
   speaker="Alfred Lord Tennyson" %}

**Copy this:**
```liquid
{% raw %}{% include essay/feature/blockquote.html
   quote="Knowledge comes, but wisdom lingers"
   speaker="Alfred Lord Tennyson" %}{% endraw %}
```

### With Source Citation

{% include essay/feature/blockquote.html
   quote="It is a truth universally acknowledged, that a single man in possession of a good fortune, must be in want of a wife."
   speaker="Jane Austen"
   source="Pride and Prejudice" %}

**Copy this:**
```liquid
{% raw %}{% include essay/feature/blockquote.html
   quote="Your quote text here"
   speaker="Author Name"
   source="Book or Article Title" %}{% endraw %}
```

### Large Centered Quote w/ No Border

{% include essay/feature/blockquote.html
   quote="The best way out is always through"
   size="xl"
   speaker="Robert Frost"
   align="center" 
   border=false %}

**Copy this:**
```liquid
{% raw %}{% include essay/feature/blockquote.html
   quote="Your dramatic quote"
   speaker="Famous Person"
   size="xl"
   align="center"
   border=false  %}{% endraw %}
```

**Size options:** `sm`, `md`, `lg`, `xl`, `xxl`

**Align options:** `left`, `center`, `right`

---


## Section Transitions

Create visual breaks between major sections using scrollama transitions.

{% include essay/new-section.html %}

## New Major Section

The section break above creates a visual pause and scroll-triggered transition effect. This helps structure long essays into distinct parts.

**Copy this:**
```liquid
{% raw %}{% include essay/new-section.html %}

## Your New Section Title

Content continues here...{% endraw %}
```

**Use sparingly** - 3-4 sections per essay maximum for best effect.

---

## Scrollytelling Blocks

Pin an image (or series of images) while multiple narrative text panels scroll over it — the StoryMaps / scrolly-explainer pattern. Great for manuscript walkthroughs, archival photo essays, site surveys, or any story where you want an image to anchor the reader while text builds around it.

### Immersive layout (image fills viewport)

Below is a live demo. Scroll through the panels to see the image swap:

{% include essay/feature/scrolly-media.html objectid="demo_001" alt="Administration Building, University of Idaho, ca. 1910" %}

**Panel 1.** An archival postcard of the University of Idaho's Administration Building, taken around 1910. The image fills the screen while your text scrolls over it — no JavaScript wiring required on your end.

{% include essay/feature/scrolly-step.html objectid="demo_009" %}

**Panel 2.** When this panel scrolls into view, the image cross-fades to a different collection item. You can keep adding panels, each optionally swapping to a new image.

{% include essay/feature/scrolly-step.html objectid="demo_031" position="right" text-background="dark"  %}

**Panel 3.** Panels can appear on the `left` (default), `center`, or `right`. Use `text-background="dark"` for a dark semi-transparent card instead of white.

{% include essay/feature/scrolly-step.html objectid="demo_011" animate="ken-burns" image-focus="75% 40%" %}

**Panel 4.** This panel swaps to a new image and starts a slow zoom toward its center. Add `animate="zoom-in"` to any step to trigger the effect when that panel enters view. Pair with `image-focus` to zoom toward a specific part of the image instead of the center.

{% include essay/feature/scrolly-end.html %}

**Copy this:**
```liquid
{% raw %}{% include essay/feature/scrolly-media.html objectid="your_first_image" alt="Description" %}

First panel text. Explains the pinned image.

{% include essay/feature/scrolly-step.html objectid="your_second_image" %}

Second panel text. Image swaps when this enters view.

{% include essay/feature/scrolly-step.html position="right" text-background="dark" %}

Third panel — dark card, no image swap, image stays as second image.

{% include essay/feature/scrolly-step.html objectid="your_third_image" animate="zoom-in" %}

Fourth panel — image swaps and zooms slowly toward the center.

{% include essay/feature/scrolly-end.html %}{% endraw %}
```

Scrolling back up restores the correct image automatically — each panel tracks which image it belongs to in both scroll directions.

### Image focus and animation

Use `image-focus` to control which part of the image stays in view when using `cover` mode, and `animate` to add slow motion to the pinned image.

**`image-focus`** — any CSS `object-position` value. Also sets the zoom target for `zoom-in` / `zoom-out`.

```liquid
{% raw %}{% include essay/feature/scrolly-media.html objectid="your_image" image-focus="80% 30%" %}{% endraw %}
```

**`animate`** options: `zoom-in`, `zoom-out`, `pan-left`, `pan-right`, `ken-burns`

```liquid
{% raw %}{% include essay/feature/scrolly-media.html objectid="your_image" animate="ken-burns" %}

Opening panel with a slow diagonal zoom and drift.

{% include essay/feature/scrolly-step.html objectid="detail_image" image-focus="75% 40%" animate="zoom-in" %}

This panel swaps to a detail image and zooms toward the upper-right subject.

{% include essay/feature/scrolly-end.html %}{% endraw %}
```

Animations restart fresh each time a panel enters view. Pan animations (`pan-left`, `pan-right`) sweep the full width of the image; `image-focus` controls the zoom target for `zoom-in` and `zoom-out`. `ken-burns` uses a preset diagonal drift.

### Sidecar layout (image right, text left)

The `sidecar` layout keeps the image fixed on the right while text panels scroll on the left — good for comparing visuals to detailed analysis. Collapses to the stacked style on mobile.

{% include essay/feature/scrolly-media.html objectid="demo_019" layout="sidecar" %}

This is the front of the postcard. The image is pinned on the right while this text panel scrolls on the left.

{% include essay/feature/scrolly-step.html objectid="demo_020" %}

This is the back of the postcard. When this panel scrolls into view, the image on the right swaps to the reverse side.

{% include essay/feature/scrolly-end.html %}

```liquid
{% raw %}{% include essay/feature/scrolly-media.html objectid="your_image" layout="sidecar" %}

Text panel beside the image.

{% include essay/feature/scrolly-step.html objectid="another_image" %}

Second panel; image swaps on the right.

{% include essay/feature/scrolly-end.html %}{% endraw %}
```

### Controlling scroll speed with `step-height`

The `step-height` parameter sets the minimum scroll distance for each panel — how long a reader must scroll before the next panel triggers. The default is `300vh`. Set it on `scrolly-media.html` to apply across the whole block, or on individual `scrolly-step.html` calls to control specific panels.

```liquid
{% raw %}{% include essay/feature/scrolly-media.html objectid="your_image" step-height="100vh" %}

Slow panel — reader scrolls a full screen before anything changes.

{% include essay/feature/scrolly-step.html objectid="another_image" step-height="50vh" %}

Quick transition — this panel triggers after half a screen of scrolling.

{% include essay/feature/scrolly-end.html %}{% endraw %}
```

**`scrolly-media.html` parameters:**

| Param | Default | Description |
|-------|---------|-------------|
| `objectid` | — | Collection item ID (resolves to its display image) |
| `src` | — | Direct image path, e.g. `/assets/img/photo.jpg` |
| `alt` | — | Image alt text |
| `caption` | — | Small credit line overlaid bottom-right |
| `layout` | `immersive` | `immersive` (full-screen overlay) or `sidecar` (image right, text left) |
| `position` | `left` | Default panel position: `left`, `center`, `right` |
| `text-background` | `light` | Panel style: `light` or `dark` |
| `step-height` | `300vh` | Minimum scroll height per panel for the whole block |

**`scrolly-step.html` parameters:** same as above except `layout` (inherits from block) — plus `step-height` overrides the block default for that panel only.

---

## CollectionBuilder Features

Beyond essay-specific includes, you can use any standard CollectionBuilder feature:

### Item Cards

**Copy this:**
```liquid
{% raw %}{% include feature/card.html
   objectid="demo_001"
   width="50"
   centered=true %}{% endraw %}
```

Shows a card with the item image and metadata.


### Timelines

For essays with chronological elements, embed the full timeline:

```liquid
{% raw %}{% include feature/timeline.html %}{% endraw %}
```

### Subject Clouds

Visualize subject keywords from your collection:

```liquid
{% raw %}{% include feature/cloud.html fields="subject" %}{% endraw %}
```

---


## Mini Maps

Embed small maps at specific coordinates.

{% include feature/mini-map.html
   latitude="46.727485"
   longitude="-117.014185"
   map-zoom="18" 
   caption="This is the library where I work!" %}

**Copy this:**
```liquid
{% raw %}{% include feature/mini-map.html
   latitude="46.727485"
   longitude="-117.014185"
   map-zoom="18" 
   caption="This is the library where I work!" %}{% endraw %}
```

**Finding coordinates:**
- Right-click location on Google Maps → Click coordinates to copy
- Or use [LatLong.net](https://www.latlong.net/)

**Zoom levels:** 1 (world) to 18 (street level)

---


## Combining Features

You can combine multiple features for rich, scholarly presentations:

### Example: Blockquote + Aside + Map

{% include essay/feature/blockquote.html
   quote="I went to the woods because I wished to live deliberately"
   speaker="Henry David Thoreau"
   source="Walden" %}

Thoreau's cabin was located on the shores of Walden Pond{% include essay/feature/aside.html text="The cabin measured 10 feet by 15 feet and cost $28.12 to build." %} in Concord, Massachusetts, where he lived from 1845 to 1847.

{% include feature/mini-map.html
   latitude="42.4407"
   longitude="-71.3428"
   map-zoom="14" %}

The location provided the solitude Thoreau sought for his philosophical experiment in simple living.

---

## Print & PDF Output

Most features work in print PDFs. **Blockquotes, asides, images, and section breaks** all render beautifully. **Mini-maps and videos** are web-only and won't appear in print.

Visit the **[Print Hub](/print/)** to generate PDFs in Letter, A4, or 6×9″ formats. See the [Print Guide]({{ '/docs.html#print-pdf' | relative_url }}) for complete details including margin note styles, page formats, and accessibility features.

---

## Best Practices

### Blockquotes
- Use for significant quotations only
- Always attribute with `speaker` parameter
- Keep quotes focused and relevant
- Don't nest blockquotes

### Asides
- Maximum 3-4 per essay
- Keep text brief (1-3 sentences)
- Ensure objectids exist in metadata
- Test display on mobile AND in print preview

### Maps
- Verify coordinates are accurate
- Choose appropriate zoom level (12-14 for cities)
- Add context about the location in text
- Note: Maps won't appear in print PDFs (web-only feature)

### Section Breaks
- Use for major structural divisions
- 3-4 maximum per essay
- Ensure sections are substantial
- Works best with longer essays (1000+ words)

---

## Next Steps

To see all scroll-based effects demonstrated live — zoom, pan, ken-burns, sidecar, and focus point — scroll through the next essay:

**[Scroll-Based Features →](05-scroll-features.html)**

Or skip ahead to **[Collection Integration →](05-collection-integration.html)** to learn how to weave your items into the narrative.

You can also get answers to your questions with our [online documentation]({{ '/docs.html' | relative_url }}) .
---

{% include essay/feature/cta.html text="Use This Template →" link="https://github.com/new?template_name=cb-essay&template_owner=CollectionBuilder" description="Ready to put these features to use? Start your own project." %}


