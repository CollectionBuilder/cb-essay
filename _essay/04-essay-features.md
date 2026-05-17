---
title: Writing Features
order: 40
part: Documentation
---

CB-Essay provides specialized includes that extend Markdown for scholarly writing. This essay **demonstrates every feature** with working examples you can copy directly into your own work.

**The copy-and-replace principle:** Find a feature you like, copy the code block, paste it into your essay, and replace the content with yours. That's it!

## Basic Markdown

Start with standard Markdown formatting:

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

### Images

```markdown
![Alt text](/assets/img/image.jpg)
```

### Lists

**Bulleted:**
- Item one
- Item two
  - Nested item

**Numbered:**
1. First item
2. Second item
3. Third item

### Code Blocks

Use triple backticks for code:

````markdown
```yaml
---
title: Your Essay
order: 1
---
```
````

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

## Image Galleries

Display multiple collection items as inline galleries.

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

### Item Images

**Copy this:**
```liquid
{% raw %}{% include feature/image.html
   objectid="demo_012"
   width="75" %}{% endraw %}
```

Displays an item image with caption from metadata.

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

You now know every feature available in CB-Essay! The final essay shows how to integrate collection items more deeply:

**[Collection Integration →](05-collection-integration.html)**



---

**Remember:** Copy any feature from this page, replace the content with yours, and it will work in your essay!
