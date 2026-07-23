---
title: Extracting a Book from Project Gutenberg
order: 35
part: Documentation
---

Here's the fastest way to see everything CB-Essay can do: skip writing altogether and pull in a finished book. Project Gutenberg hosts more than 60,000 public domain texts, and CB-Essay ships a tool that turns any one of them into a working, styled, chapter-by-chapter site in a few minutes — pre-formatted, front-matter and all. It's also just fun to play with.

This essay walks through running the extractor, shows exactly what it produces, and points you toward where to take the result from there.

---


## Running the Extractor

1. Make sure GitHub Pages is enabled first — see [Get Started, Step 7](03-get-started.html#step-7-deploy-to-github-pages) if you haven't done this yet.
2. Go to your repository's **Actions** tab.
3. Click **"Extract Gutenberg Book"** in the workflow list.
4. Click **"Run workflow"** and fill in three inputs:
   - **`book_id`** — the Gutenberg ebook ID, found in its URL (`gutenberg.org/ebooks/84` → `84` for *Frankenstein*; `1342` for *Pride and Prejudice*).
   - **`clear_existing`** (default: checked) — deletes everything currently in `_essay/` before extracting. Uncheck this if you have existing essays you want to keep.
   - **`generate_about`** (default: checked) — also generates `pages/about.md` with a catalog-card include and an "About This Edition" note.
5. Click **"Run workflow"** and wait a few minutes for it to extract, commit, and rebuild your site.

---

## What You Get

- Chapter-by-chapter Markdown files in `_essay/`, each with `title`, `order`, and `chapter` front matter already set.
- The book's cover image and interior illustrations, downloaded where available.
- Author, title, and publication metadata pulled from the book's Dublin Core data.
- `_config.yml` and `_data/theme.yml` updated automatically — site title, author, description, a matching `half-image` homepage layout with the cover as the featured image, and print metadata.
- If `generate_about` was checked, a populated `pages/about.md` crediting Project Gutenberg and linking back to the extraction script.

---

## See It Live

*Frankenstein* is CB-Essay's own extraction demo — chapter navigation, historical context, and a scholarly apparatus, all starting from the same public domain text shown above.

{% include feature/video.html objectid="https://www.lib.uidaho.edu/collectionbuilder/cb-essay/frankenstein.mp4" caption="Building the Frankenstein site end to end, from a blank template to a published book." %}

**View:** [dcnb.github.io/frankenstein](https://dcnb.github.io/frankenstein)

---

## Now Make It Yours

Extracted chapters are a starting point, not a finished essay. Once you've got a book's worth of clean Markdown, treat it the way you would any other CB-Essay content:

- Add asides that link a passage to a related archival item or historical note — see [Essay Writing Features](04-essay-features.html).
- Break a long chapter into a scrollytelling sequence with a relevant illustration pinned in view — see [Scroll-Based Features](05-scroll-features.html).
- Adjust `order` values if you want to reorganize chapters, or add your own introductory essay ahead of Chapter 1.

---

## For the Curious: How It Works

The extractor pattern-matches against the consistent boilerplate markers, chapter heading conventions, and metadata formats that Project Gutenberg uses across its catalog. For the technical detail — useful if you're debugging an unusual book or extending the script — see the **[Gutenberg Extraction Guide](https://github.com/CollectionBuilder/cb-essay/blob/main/docs/cb-essay/gutenberg-extraction.md)** (technical/maintainer reference, not another tutorial).

---

## Next Steps

**[Essay Writing Features →](04-essay-features.html)**

{% include essay/feature/cta.html text="Use This Template →" link="https://github.com/new?template_name=cb-essay&template_owner=CollectionBuilder" description="Ready to extract your own book? Start your own copy of CB-Essay." %}
