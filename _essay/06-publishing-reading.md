---
title: Publishing, Printing & Reading
order: 50
part: Documentation
---

Writing an essay is only half of it — this page covers every way a reader can actually encounter your finished work: on the web, in search results, in print, and on paper or an e-reader.

---

## Print & PDF

Every essay generates a print-ready page automatically using [Paged.js](https://pagedjs.org/), no separate export step required. Visit the **[Print Hub](/print/)** to print an individual essay or build a custom multi-essay book, in Letter, A4, or 6×9″ trim sizes.

Configure what's available in the `print:` block of `_data/theme.yml` — author and institution for the cover page, whether individual-essay and full-book printing are offered, and whether margin notes render as floating gutter asides (`aside-style: margin`) or inline callout blocks (`aside-style: inline`). See the [Print Guide]({{ '/docs.html#print-pdf' | relative_url }}) for the complete option list.

Most content prints beautifully — blockquotes, asides, images, and section breaks all render. Mini-maps and videos are web-only and won't appear in the PDF.

---

## Search

Every essay gets full-text search automatically at **[/search/](/search/)**, powered by [FlexSearch](https://github.com/nextapps-de/flexsearch) running entirely in the reader's browser — no server required, and it works the same on GitHub Pages as anywhere else.

Search results are grouped by chapter with occurrence counts and highlighted context snippets, sortable by relevance, alphabetically, or by reading order. From an essay page, search can be scoped to just that essay or across the whole site; clicking a result jumps straight to the match and highlights it on arrival.

Any page opts in with `text_search: true` in its front matter — essays have this on by default. The index is chunked by heading (`##`, `###` by default), so results point to the specific section a match was found in, not just the top of the essay.

---

## Publishing Options

You have the same options as you would for any CollectionBuilder site: 

**Publish free, on GitHub Pages.** The default path — push to your repository and GitHub builds and hosts the site for free at `username.github.io/repository-name`. Covered step by step in [Get Started, Step 7](03-get-started.html#step-7-deploy-to-github-pages).

**Use your own domain.** Add a `CNAME` file with your domain name to the repository root and point your DNS at GitHub Pages — the site keeps building for free, just under your own URL. See [GitHub's custom domain docs](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site).

**Use your own server.** CB-Essay is a static site — nothing about it requires GitHub. Run `rake deploy` and upload the resulting `_site/` folder to any web host, institutional server, or storage bucket that serves static files.

For more information, see our [CollectionBuilder documentation pages](https://collectionbuilder.github.io/cb-docs/docs/deploy/).

---

## Reading on an E-Reader

CB-Essay doesn't generate EPUB files directly; if you need one, the print PDF is the best starting point for conversion. These PDFs however, are designed for a solid reading experience and can be shared with a Kindle or other e-reader. 

---

## Sharing & Discovery

In production, every essay and item page gets Open Graph and Schema.org metadata automatically, so links shared on social media and in messaging apps show a proper title, description, and preview image. Set `title` and `description` in `_config.yml` and `featured-image` in `_data/theme.yml` to control how the site itself appears in search results and link previews.


---

## Next Steps

You've reached the end of the tour — you now know how to write, illustrate, style, and publish a CB-Essay project. For anything not covered here, the [online documentation]({{ '/docs.html' | relative_url }}) is comprehensive and searchable.


{% include essay/feature/cta.html text="Use This Template →" link="https://github.com/new?template_name=cb-essay&template_owner=CollectionBuilder" description="You've seen everything CB-Essay can do. Now build something of your own." %}
