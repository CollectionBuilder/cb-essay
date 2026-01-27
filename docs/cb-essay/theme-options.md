# Theme Options

CB-Essay supports two presentation themes for your essays: **Essay** and **Monograph**. These themes affect the homepage layout, navigation style, and overall reading experience.

## Choosing Your Theme

Set the theme in `_data/theme.yml`:

```yaml
base-theme: essay  # or monograph
```

---

## Essay Theme

**Best for:** Traditional essays, article collections, blog-like presentations

### Features
- Clean, minimalist homepage
- Linear reading experience
- Simple navigation
- Focus on continuous reading flow

### Homepage Layout

The essay theme presents a featured image with a prominent "Read the Essay" button:

```yaml
# In _data/theme.yml
base-theme: essay
image-style: full-image  # or half-image, or no-image
featured-image: /assets/img/banner.jpg
```

### Navigation
- Essays accessible through "Read the Essay" button
- Prev/Next buttons at bottom of each essay
- No table of contents on homepage

### When to Use
- Single continuous essay with multiple sections
- Essay collection with loose connections
- Blog-style presentation
- When you want readers to discover essays sequentially

---

## Monograph Theme

**Best for:** Book-like publications, multi-chapter works, collected volumes

### Features
- Table of contents on homepage
- Chapter-style organization
- Book-like presentation
- Easy random access to any section

### Homepage Layout

The monograph theme includes a formatted table of contents below the featured image:

```yaml
# In _data/theme.yml
base-theme: monograph
```

### Table of Contents

Automatically generates from your essays:

- Displays all essays in order
- Shows title and optional byline
- Links directly to each essay
- Scrolls user to TOC from hero banner

### Navigation
- Table of contents on homepage
- "Contents ↓" button on banner
- Prev/Next buttons on essay pages
- Chapter-like structure

### When to Use
- Multi-chapter books
- Edited volumes with multiple contributors
- Reference works
- Any content benefiting from overview/direct access

---

## Homepage Image Options

Both themes support three image display styles:

### Full Image (`full-image`)

Full-screen banner with overlaid title and buttons:

```yaml
image-style: full-image
featured-image: /assets/img/banner.jpg
home-banner-image-position: center  # or top, bottom
```

**Best for:** Dramatic, immersive presentations

### Half Image (`half-image`)

Split layout with image on one side, text on other:

```yaml
image-style: half-image
featured-image: /assets/img/cover.jpg
```

**Best for:** Book covers, portrait images, formal presentations

### No Image (`no-image`)

Text-only homepage with elegant typography:

```yaml
image-style: no-image
```

**Best for:** Minimalist presentations, text-focused work

---

## Customizing Your Theme

### Site Metadata

Settings in `_config.yml` control your homepage cover page:

```yaml
# In _config.yml
title: "Your Essay Title"
author: "Your Name"  # Displays as "by Your Name" on cover
tagline: "A brief description"  # Only shows if author is empty
description: "Longer description for search engines"
```

**Cover Page Display:**
- `title`: Main title (always displayed)
- `author`: Appears as "by [Author Name]" beneath title
  - If provided, replaces the tagline on the cover page
  - Use HTML for multi-line attribution: `author: "Author Name<br>Edited by Editor<br>Translated by Translator"`
- `tagline`: Subtitle/description (only displays if author is empty)
  - Can also use HTML: `tagline: "A Digital Edition<br>Published 2024"`

### Featured Image

```yaml
# In _data/theme.yml
featured-image: /assets/img/your-image.jpg
featured-image-credit: "Image credit: Source Name"
featured-image-alt-text: "Description for accessibility"
```

**Image Tips:**
- Full image: 1920x1080px or larger
- Half image: 800x1200px (portrait) or 1200x800px (landscape)
- Optimize images before adding
- Add credits in `featured-image-credit`

### Colors and Typography

```yaml
# In _data/theme.yml
base-font-size: 1.3em
text-color: "#191919"
link-color: "#0d6efd"
base-font-family: Georgia  # or any web-safe font
```

### Navigation Colors

```yaml
navbar-color: navbar-light    # or navbar-dark
navbar-background: bg-light   # Bootstrap color classes
```

---

## Theme Comparison

| Feature | Essay Theme | Monograph Theme |
|---------|-------------|-----------------|
| Homepage TOC | No | Yes |
| Best for | Essays, articles | Books, chapters |
| Navigation | Linear | Direct access |
| Reading flow | Continuous | Modular |
| Contributors | Single author | Multiple authors |

---

## Advanced Customization

### Home Title Positioning

For full-image style:

```yaml
home-title-y-padding: 20em  # Distance from top
home-banner-image-position: center  # Image position
```

### Custom CSS

Add custom styles in `assets/css/custom.scss`:

```scss
// Custom essay styles
.essay-main {
  max-width: 800px;
}

// Custom blockquote styling
.blockquote {
  border-left: 4px solid #333;
}
```

### Bootstrap Themes

Apply a Bootswatch theme:

```yaml
bootswatch: journal  # or cerulean, flatly, etc.
```

See [Bootswatch](https://bootswatch.com/) for options.

---

## Examples

### Essay Theme Example

```yaml
# _data/theme.yml
base-theme: essay
image-style: full-image
featured-image: /assets/img/landscape.jpg
home-banner-image-position: center

# _config.yml
title: "Digital Memories"
author: "Jane Scholar"
tagline: "An essay on digital preservation"
```

**Result:** Full-screen image, dramatic entrance, linear reading

### Monograph Theme Example

```yaml
# _data/theme.yml
base-theme: monograph
image-style: half-image
featured-image: /assets/img/book-cover.jpg

# _config.yml
title: "Essays on Digital Humanities"
author: "Multiple Contributors"
```

**Result:** Book cover layout, table of contents, chapter navigation

---

## Switching Themes

To switch between themes:

1. Edit `_data/theme.yml`
2. Change `base-theme` value
3. Adjust `image-style` if desired
4. Save and rebuild site

```bash
bundle exec jekyll s
```

Your essays don't change - only the presentation!

---

## Theme-Specific Features

### Essay Theme Only
- Streamlined homepage
- Focus on "start reading" action
- Minimal distractions

### Monograph Theme Only
- Table of contents generation
- "Contents ↓" navigation button
- Byline display in TOC
- Chapter numbering support

---

## Best Practices

### Choosing a Theme
- **Essay:** 2-8 connected sections, single narrative
- **Monograph:** 8+ chapters, multiple authors, reference work

### Featured Images
- Use high-quality images
- Ensure proper licensing/attribution
- Test on mobile devices
- Consider file size

### Typography
- Larger fonts for long reading (1.2em - 1.4em)
- Serif fonts (Georgia, Garamond) for traditional scholarship
- Sans-serif (Roboto, Open Sans) for modern feel

### Colors
- High contrast for readability
- Test accessibility (WCAG AA minimum)
- Match institutional branding if needed

---

## Troubleshooting

### Table of contents not appearing
- Verify `base-theme: monograph` in theme.yml
- Check essays have `order` field in front matter
- Ensure essays are building (check `_site/essay/`)

### Featured image not displaying
- Check image path is correct (relative or absolute)
- Verify image file exists
- Check `image-style` is set
- Look in browser console for 404 errors

### Navigation buttons missing
- Confirm essays have sequential `order` values
- Need at least 2 essays for prev/next
- Check essay layout is `essay-content`

---

## Next Steps

- [Essay Writing Guide](essay-writing.md) - Create your essays
- [Essay Features Reference](essay-features.md) - Add special features
- Try both themes to see which fits your content
- Explore demo site for theme examples
