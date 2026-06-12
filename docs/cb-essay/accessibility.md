# CB-Essay Accessibility

CB-Essay has been built and tested to meet a high standard of web accessibility. The framework's templates, navigation, color themes, and essay features were evaluated against the [Web Content Accessibility Guidelines (WCAG) 2.1](https://www.w3.org/WAI/standards-guidelines/wcag/) using tools including [WAVE](https://wave.webaim.org/) and Lighthouse in Chrome's Developer Tools, and the framework consistently grades well in those compliance checks. **Out of the box, an unmodified CB-Essay site should be WCAG 2.1 accessible.**

CollectionBuilder, on which CB-Essay is built, is likewise designed to meet high accessibility standards. For more on that work, see [CollectionBuilder's accessibility page](https://collectionbuilder.github.io/cb-docs/docs/accessibility/).

The interface has been developed with assistive technology in mind: focus indicators are clearly visible, interactive elements (the Contents panel, section navigation, image galleries, modals) are keyboard-operable, form controls are labeled, and the built-in color themes are tuned for sufficient contrast in long-form reading.

## Your responsibility after customization

**The most important thing to understand: an accessible foundation does not guarantee an accessible published site.** Once you customize the theme, add your own essays, or bring in collection items, accessibility becomes *your* responsibility. New content and configuration changes can introduce barriers that the framework cannot prevent — a missing alt text, a custom color with poor contrast, a heading level skipped.

You must **test and verify accessibility yourself** after customizing and after adding content. Treat an accessibility check as a normal part of publishing, not a one-time step. The guidance below covers the areas most likely to need your attention in an essay project.

## WCAG at a glance

WCAG organizes accessibility around four principles. For an essay site, they translate roughly to:

- **Perceivable** — Provide text alternatives (alt text) for images, ensure sufficient color contrast, and don't rely on color alone to convey meaning.
- **Operable** — Make everything reachable and usable by keyboard; keep navigation predictable.
- **Understandable** — Write clearly, use a logical heading structure, and make link text meaningful.
- **Robust** — Use the semantic markup the framework already provides (don't replace it with raw `<div>`s) so screen readers and other assistive tech can interpret your content.

## Best practices for accessible essays

### Images and alt text

Every image needs a text alternative describing its content or function.

- Set `featured-image-alt-text` in `_data/theme.yml` for the homepage image.
- **For collection items, add an `image_alt_text` column to your metadata CSV.** Since CollectionBuilder-CSV 2023, this dedicated field supplies custom descriptive alt text for `image_small` and `image_thumb` wherever they appear in the template — including asides, galleries, and image includes inside your essays. Keeping alt text separate from `title` and `description` lets you craft a description aimed specifically at conveying the image to someone who can't see it. **Use it for any image that carries meaning.** If the column or a value is missing, the template falls back to the previous behavior (using the item's title), so populating `image_alt_text` is the recommended best practice.
- Write alt text that conveys *meaning*, not just labels: "A handwritten manuscript page with margin revisions" is better than "image1.jpg" or a bare title.
- For purely decorative images, an empty alt is appropriate so screen readers can skip them.

See the [CB-CSV metadata reference](https://collectionbuilder.github.io/cb-docs/docs/metadata/csv_metadata/#image_alt_text) for the full field definition and examples.

### Transcripts for audio and video

Audio and video objects are inaccessible to deaf, hard-of-hearing, and many other users without a text alternative, so a transcript is essential.

- **Add an `object_transcript` column to your metadata CSV** for audio and video items. Since CollectionBuilder-CSV 2023, the template renders this field as a basic transcript on the item page.
- **Provide a transcript for every audio or video object you publish**, and any time you embed one in an essay. A good transcript identifies speakers, captures spoken content accurately, and notes significant non-verbal sounds (e.g., `[laughter]`, `[applause]`).
- See the [CB-CSV metadata reference](https://collectionbuilder.github.io/cb-docs/docs/metadata/csv_metadata/#object_transcript) for details.

### Heading structure

Screen-reader users navigate by headings, so structure matters more than appearance.

- Use Markdown headings in order: the essay title is the page `<h1>`; start your in-essay sections at `##` (`<h2>`) and nest with `###` below them.
- Don't skip levels (e.g., jumping from `##` to `####`) and don't pick a heading level just because you like its size — use [theme/CSS](theme-options.md) for sizing.
- The floating section navigation (`show-section-nav`) is built from your `##` headings, so a clean heading outline also produces clean navigation.

### Color and contrast

- The built-in color themes (`default`, `idaho`, `lyre`, `nonesuch`, `aldine`, `doves`, `kelmscott`, `gregynog`, `ashendene`) are tuned for accessible contrast. If you stay on a built-in theme, you're starting from a good place.
- If you set `color-theme: custom` with your own `custom-color`, **re-check contrast** — text, links, and navbar against their backgrounds — with a tool like the [WebAIM Color Contrast Checker](https://webaim.org/resources/contrastchecker/). Aim for a contrast ratio of at least 4.5:1 for body text.
- Never use color as the *only* way to signal something (e.g., "the items in red"). Pair it with text or shape.

### Asides, galleries, and interactive features

- Keep **aside** (margin note) text concise and meaningful; it is read inline by screen readers, so it should make sense in the flow of the sentence.
- Image **galleries** open a full-screen viewer that is keyboard-operable — verify your gallery items have titles so the viewer announces them.
- After adding any interactive feature, **test it with the keyboard alone**: Tab to it, operate it, and Escape/close it without a mouse.

### Links

- Write descriptive link text. "See the [Essay Features guide](essay-features.md)" is accessible; "click [here](essay-features.md)" is not.
- Make clear when a link leaves the site or points to a large download.

### Print and PDF

The Paged.js print/PDF output carries over your structure, but PDFs have their own accessibility considerations. If you distribute PDFs, verify that headings, alt text, and reading order survive in the exported file, and tag the PDF if your audience requires it.

## Test before you publish

Build your changes locally or on a staging branch and run at least one automated check plus a manual pass before publishing:

1. **Automated** — Run [WAVE](https://wave.webaim.org/) and/or Lighthouse against your pages. Fix the errors they flag.
2. **Keyboard** — Navigate the whole site with Tab, Enter, and Escape only. Everything reachable by mouse should be reachable and operable by keyboard, with a visible focus indicator.
3. **Screen reader** — Spot-check a few pages with a screen reader (VoiceOver on macOS, NVDA on Windows) to confirm headings, alt text, and navigation read sensibly.
4. **Contrast** — If you changed colors, check them with a contrast checker.

Make this a routine step whenever you add essays or items, not just at launch.

## Resources

**Guidelines and standards**

- [Web Content Accessibility Guidelines (WCAG)](https://www.w3.org/WAI/standards-guidelines/wcag/)
- [Section 508 Standards](https://www.section508.gov/)
- [CollectionBuilder Accessibility](https://collectionbuilder.github.io/cb-docs/docs/accessibility/)

**Testing tools**

- [WAVE Accessibility Tool](https://wave.webaim.org/)
- [WebAIM Color Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [Accessibility Insights](https://accessibilityinsights.io/)

**Learning**

- [WebAIM Articles and Resources](https://webaim.org/articles/)
- [The A11Y Project](https://www.a11yproject.com/)
- [WebAIM: Alternative Text](https://webaim.org/techniques/alttext/)
