# Theme Options

CB-Essay gives you three independent flags to control navigation and homepage layout. Mix and match them to suit your project.

## Navigation & Homepage Flags

Set these in `_data/theme.yml`:

```yaml
show-contents-nav: true    # "Contents" button in navbar opens chapter list panel
show-homepage-toc: true    # chapter table of contents on the homepage
show-section-nav: false    # floating sidebar TOC built from H2s on each essay page
```

---

## `show-contents-nav`

Controls which navbar style is used and whether the off-canvas chapter list panel is available.

**`true`** — Navbar shows a centered site title with a "Contents" button on the left and a menu toggle on the right. The Contents button opens a slide-in panel listing all essays in order.

**`false`** — Navbar shows the site title on the left with only a menu toggle on the right. Simpler, lower-profile navigation.

---

## `show-homepage-toc`

Controls whether a table of contents appears on the homepage beneath the banner.

**`true`** — Homepage renders a chapter list with titles and optional bylines. The banner image also gains a "Contents ↓" button linking to it. Only displays when the site has more than one essay.

**`false`** — Homepage shows only the banner image and "Read" button. Best for single essays or when you want the homepage to focus on the entry point rather than the full chapter list.

---

## `show-section-nav`

Controls a floating sidebar on essay pages that is auto-built from the H2 headings within the essay.

**`true`** — A fixed sidebar appears on the left side of essay pages (visible on screens wider than 1400px). It shows the essay title at the top, a link to print/PDF, and one entry per H2 heading. The active section highlights as the reader scrolls. Hash URLs update automatically.

**`false`** — No sidebar (default). Works best when essays have few H2s or you prefer a clean, uninterrupted reading experience.

---

## Common Configurations

### Simple essay — single narrative, minimal nav

```yaml
show-contents-nav: false
show-homepage-toc: false
show-section-nav: false
```

Homepage shows a banner with a "Read" button. Navbar is title + menu only.

### Multi-chapter monograph

```yaml
show-contents-nav: true
show-homepage-toc: true
show-section-nav: false
```

Homepage shows the full chapter list. Navbar has a Contents button opening the chapter panel.

### Long single essay with in-page navigation

```yaml
show-contents-nav: false
show-homepage-toc: false
show-section-nav: true
```

Readers on wide screens get a fixed sidebar that tracks their position through the essay's H2 sections.

### Collection with per-chapter section navigation

```yaml
show-contents-nav: true
show-homepage-toc: true
show-section-nav: true
```

Full monograph setup plus per-essay section sidebars.

---

## Homepage Image Options

All configurations support three image display styles:

### Full image (`full-image`)

Full-screen banner with overlaid title and buttons:

```yaml
image-style: full-image
featured-image: /assets/img/banner.jpg
home-banner-image-position: center  # or top, bottom
```

### Half image (`half-image`)

Split layout with image on one side, text on the other:

```yaml
image-style: half-image
featured-image: /assets/img/cover.jpg
```

### No image (`no-image`)

Text-only homepage:

```yaml
image-style: no-image
```

---

## Color Themes

CB-Essay includes 8 built-in color themes inspired by historical printing presses. Each theme is designed for accessibility and long-form reading, providing coordinated colors for the navbar, links, accents, and UI elements.

Set in `_data/theme.yml`:

```yaml
color-theme: aldine  # default, idaho, lyre, nonesuch, aldine, doves, kelmscott, gregynog, ashendene
```

### Built-in Themes

**`default`** - Warm cream neutral with purple accents

**`idaho`** - Douglas-fir green on aged paper (dark navbar)

**`lyre`** - Faded indigo cloth with gilt spine (dark navbar)

**`nonesuch`** - Cream cloth with red rules (light navbar)

**`aldine`** - Marine blue in the Venetian tradition (dark navbar)

**`doves`** - Severe black-on-white minimalism (dark navbar)

**`kelmscott`** - Holland blue boards with rubric red (light navbar)

**`gregynog`** - Slate buckram with three-color printing (dark navbar)

**`ashendene`** - Faded brown calf leather (dark navbar)

Each theme automatically sets navbar style, text colors, link colors, accent colors, and print output styling.

### Custom Color

Generate an accessible color palette from any hex color:

```yaml
color-theme: custom
custom-color: "#8B4513"
navbar-style: dark  # dark (white text) or light (dark text)
```

The system extracts the hue and generates a complete, accessible palette with proper contrast ratios.

---

## Typography & Fonts

CB-Essay offers three font systems that work independently or together:

### 1. Theme Fonts (Recommended)

Automatically pairs fonts with your color theme:

```yaml
base-font-family: theme       # Body text
display-font-family: theme    # Headings
```

Each color theme ships with a carefully selected Google Font pairing chosen for long-form reading. Fonts are free, openly licensed, and include regular, italic, and medium weights.

### 2. Georgia (Offline)

Use system Georgia for offline-first sites with no CDN requests:

```yaml
base-font-family: Georgia
display-font-family: Georgia
```

### 3. Custom Google Font

Specify your own font with a Google Fonts CDN link:

```yaml
base-font-family: "'Literata', Georgia, serif"
display-font-family: "'Literata', Georgia, serif"
font-cdn: "https://fonts.googleapis.com/css2?family=Literata:ital,opsz,wght@0,7..72,400;0,7..72,500;1,7..72,400&display=swap"
```

### Mix and Match

Use theme fonts for body text with a custom display font for headings:

```yaml
base-font-family: theme
display-font-family: "'Playfair Display', Georgia, serif"
font-cdn: "https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600&display=swap"
```

### Font Size

```yaml
base-font-size: 1.2em  # 1.2em - 1.4em recommended for long-form reading
```

---

## Creating Custom Themes

Want to add a new color theme to the system? See `_prompts/add-theme.md` for detailed instructions on adding themes to `_sass/_color-tokens.scss`.

---

## Troubleshooting

**Table of contents not appearing:**
- Check `show-homepage-toc: true` in `_data/theme.yml`
- Verify essays have an `order` field in their front matter
- Rebuild the site

**Section sidebar not showing:**
- Check `show-section-nav: true` in `_data/theme.yml`
- The sidebar only appears on screens wider than 1400px
- Verify the essay has H2 headings (the sidebar is built from those)

**Featured image not displaying:**
- Check image path is correct
- Verify the file exists in the repository
- Check `image-style` is set
- Look for 404 errors in the browser console

**Navigation buttons (prev/next) missing:**
- Confirm essays have sequential `order` values in front matter
- Need at least 2 essays for prev/next
- Check that the essay layout is `essay-content`

---

## Next Steps

- [Essay Writing Guide](essay-writing.md) — Create your essays
- [Essay Features Reference](essay-features.md) — Add special features
