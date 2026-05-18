# CB-Essay: Add a New Color Theme

Use this prompt to generate a new color theme for a CB-Essay site. You can run it in two ways:
- **Claude Code (local)**: read this file, then follow the instructions below
- **Claude.ai (online)**: paste the contents of this file into the chat, then attach `_sass/_color-tokens.scss`, `_data/theme.yml`, and `_layouts/print.html` as file context

---

## Your Task

You are adding a new named color theme to a CB-Essay Jekyll site. The color system uses OKLCH custom properties defined in `_sass/_color-tokens.scss`.

**Start by asking the user:**
1. What should the theme be called? (single slug: e.g. `crimson`, `dusk`, `coral`)
2. Describe the color personality — what colors should it use? (can give hex values, or a description like "warm coral pinks and dusty rose")
3. Is it earthy/academic or vibrant/playful? (affects surface visibility and energy)
4. Should the navbar be dark (strong color background + white text) or light (surface-tinted, dark text)?

Once you have answers, generate the theme and make the changes described below.

---

## Color System Architecture

The site uses OKLCH (perceptual color space) for all UI tokens. OKLCH values are:
`oklch(Lightness% Chroma Hue)` where:
- Lightness: 0–100% (0=black, 100=white)  
- Chroma: 0–0.4 (0=gray, 0.1=moderate, 0.2+=vivid)
- Hue: 0–360 degrees

**Token palette for each theme:**

```
Surface palette (page backgrounds, sidebars, navbars):
  --cb-surface-100   lightest surface (97–98% lightness)
  --cb-surface-200   second surface (95–96%)
  --cb-surface-300   third surface (93–94%)
  --cb-border-100    lighter border (90–91%)
  --cb-border-200    stronger border (85–86%)
  --cb-muted         scrollbar/muted element (70–74%)

Text scale (all use low chroma 0.003–0.005 for readability):
  --cb-text-500   60% lightness — metadata, labels
  --cb-text-600   50% — secondary text
  --cb-text-700   45% — body-adjacent text
  --cb-text-800   35% — body text
  --cb-text-900   20% — headings, strong elements
  --cb-text-950   13% — maximum contrast

Accent and navigation:
  --cb-hue            primary hue in degrees (for reference)
  --cb-accent-hue     accent hue (can differ for two-color themes)
  --cb-accent-chroma  accent chroma value

  --cb-navbar-bg      navbar/off-canvas background
  --cb-navbar-text    navbar text color (usually #ffffff for dark, #191919 for light)
  --cb-navbar-border  navbar border (transparent for dark navbars, surface token for light)

  --cb-primary-color  links, aside reference numbers
  --cb-accent-color   aside flag buttons, HR rules (can equal primary, or differ for 2-color)
  --cb-hr-color       horizontal rule color in essay body (usually lighter/muted version)
  --cb-print-accent   color for HR rules in print/PDF output
```

**Chroma guidelines:**
- Earthy/academic surfaces: 0.015–0.022 (visible but not overwhelming)
- Vibrant/playful surfaces: 0.010–0.016 (tinted but still very readable)
- Dark navbar (academic): oklch(22–28% 0.07–0.10 hue)
- Dark navbar (vibrant): oklch(12–18% 0.05–0.08 hue)
- Primary color (links): oklch(38–46% 0.12–0.17 hue) — dark enough to pass WCAG AA on white
- Accent color (flags/buttons): same as primary, or a second hue for two-color themes
- HR color: oklch(70–75% 0.06–0.10 hue) — muted, decorative
- Print accent: oklch(28–40% 0.08–0.13 hue) — visible on white paper

---

## Files to Edit

### 1. `_sass/_color-tokens.scss`

Find the last `} @else {` block (the default theme, at the bottom of the `:root { }` block) and insert a new `@else if` block **immediately before it**.

Pattern to insert:
```scss
  // ──────────────────────────────────────────────────────────────────────
  //  THEMENAME — brief description
  // ──────────────────────────────────────────────────────────────────────
  } @else if $cb-theme == 'themename' {
    --cb-surface-100: oklch(97.5% 0.0XX HUE);
    --cb-surface-200: oklch(95.5% 0.0XX HUE);
    --cb-surface-300: oklch(93.5% 0.0XX HUE);
    --cb-border-100:  oklch(90.5% 0.0XX HUE);
    --cb-border-200:  oklch(85.5% 0.0XX HUE);
    --cb-muted:       oklch(72%   0.008 HUE);
    --cb-text-500:    oklch(60%   0.003 HUE);
    --cb-text-600:    oklch(50%   0.003 HUE);
    --cb-text-700:    oklch(45%   0.004 HUE);
    --cb-text-800:    oklch(35%   0.004 HUE);
    --cb-text-900:    oklch(20%   0.005 HUE);
    --cb-text-950:    oklch(13%   0.005 HUE);

    --cb-hue:           HUEdeg;
    --cb-accent-hue:    HUEdeg;  /* change for two-color themes */
    --cb-accent-chroma: 0.XX;

    --cb-navbar-bg:     oklch(XX% 0.0X HUE);
    --cb-navbar-text:   #ffffff;  /* or #191919 for light navbar */
    --cb-navbar-border: transparent;  /* or a surface token for light navbar */

    --cb-primary-color: oklch(XX% 0.XX HUE);
    --cb-accent-color:  oklch(XX% 0.XX HUE);  /* same as primary, or different hue */
    --cb-hr-color:      oklch(72% 0.08 HUE);
    --cb-print-accent:  oklch(XX% 0.XX HUE);
```

### 2. `_data/theme.yml`

Find the `#### BUILT-IN THEMES` comment blocks and add the new theme name to the appropriate section:

```yaml
#### BUILT-IN THEMES — EARTHY / ACADEMIC
# ...existing themes...
# themename — brief description; navbar type
```

Or under `VIBRANT / PLAYFUL` if applicable.

### 3. `_layouts/print.html`

Find the `--cb-print-accent` line (inside the `<style>` block, inside the `{% case cb_theme %}` expression) and add a new `{% when %}` clause before the `{% else %}`:

```liquid
{% when 'themename' %}oklch(XX% 0.XX HUE)
```
### 4. `_includes/essay/head/theme-fonts.html` (optional)

If your theme has a recommended font pairing, add a {% when 'themename' %} clause
to the case block. Choose Google Fonts that:
  - Are free and openly licensed
  - Include at minimum: regular, italic, and 500-weight
  - Have a recognizable historical or aesthetic connection to the theme

---

## Example: A "Crimson" Theme

For a warm crimson/burgundy academic theme with a dark navbar:

Hue: ~10° (red/crimson in OKLCH)

```scss
  } @else if $cb-theme == 'crimson' {
    --cb-surface-100: oklch(97.5% 0.018 10);
    --cb-surface-200: oklch(95.5% 0.020 10);
    --cb-surface-300: oklch(93.5% 0.022 10);
    --cb-border-100:  oklch(90.5% 0.020 10);
    --cb-border-200:  oklch(85.5% 0.022 10);
    --cb-muted:       oklch(72%   0.008 10);
    --cb-text-500:    oklch(60%   0.003 10);
    --cb-text-600:    oklch(50%   0.003 10);
    --cb-text-700:    oklch(45%   0.004 10);
    --cb-text-800:    oklch(35%   0.004 10);
    --cb-text-900:    oklch(20%   0.005 10);
    --cb-text-950:    oklch(13%   0.005 10);

    --cb-hue:           10deg;
    --cb-accent-hue:    10deg;
    --cb-accent-chroma: 0.13;

    --cb-navbar-bg:     oklch(26% 0.09 10);
    --cb-navbar-text:   #ffffff;
    --cb-navbar-border: transparent;

    --cb-primary-color: oklch(43% 0.15 10);
    --cb-accent-color:  oklch(43% 0.15 10);
    --cb-hr-color:      oklch(72% 0.08 10);
    --cb-print-accent:  oklch(36% 0.11 10);
```

---

## After Making Changes

Tell the user:
1. The theme name to use in `theme.yml`: `color-theme: themename`
2. To rebuild the site: `bundle exec jekyll s`
3. Any visual tuning suggestions (e.g., "if the surfaces feel too saturated, reduce the chroma from 0.020 to 0.015")
