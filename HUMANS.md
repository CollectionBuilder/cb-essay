# HUMANS.md — Working with AI on CollectionBuilder-Essay

This guide is for *you*, the human. Its companion, `AGENTS.md`, is written for the AI coding assistant. Coding agents (Cursor, Copilot, Codex, and others) read `AGENTS.md` automatically at the start of a session, so the framework's architecture rules already reach the AI without you pasting them into every prompt. This file covers what the AI can't do for you: setting intent, prompting well, and reviewing what it produces.

CollectionBuilder-Essay (**CB-Essay**) is built on top of CollectionBuilder-CSV, so most of this is identical to working with CB-CSV. The differences are an essay/monograph content layer (`_essay/`), a richer theming system, and print/PDF output — all of which this guide flags as they come up.

## What the two files do

- **`AGENTS.md`** teaches the agent the framework's rules — the customization hierarchy, what never to edit, the essay includes, the theming system. It is the single source of truth.
- **`HUMANS.md`** (this file) teaches you how to direct and check an agent that already knows those rules.

If a rule about the architecture ever needs updating, change it in `AGENTS.md`. Treat that file as authoritative so the files don't drift apart. (Claude Code and Cowork read `CLAUDE.md`, which the repo ships as a one-line pointer importing `AGENTS.md` — so they get the same rules with no setup on your part.)

## The mental model

CB-Essay is **data-driven**, like CB-CSV: almost every change happens in a CSV or YAML file, or in an essay's Markdown — not in HTML or Liquid. When working with AI, your job is mostly to:

1. Say what you want in terms of **outcomes** ("switch the site to the Doves theme," "add a margin note here"), not file edits.
2. Watch the diff for the handful of moves that signal the AI ignored the architecture.
3. Rebuild and check **one change at a time**.

The agent knows the rules. You own the intent and the review.

## Prompting: outcomes, not implementations

The agent already knows which file controls what, so describe the result you want and let it route the change to the right layer.

| Instead of | Try |
|---|---|
| "Edit the essay layout to add a sidebar note" | "Add a margin aside next to the third paragraph explaining the source" |
| "Change the SCSS to use a green palette" | "Switch the site to the `idaho` color theme" |
| "Edit the homepage template" | "Use the half-image homepage style with the book cover" |
| "Hand-code a gallery in the essay" | "Add an image gallery of `demo_001;demo_002;demo_003` after this section" |

Name objectids, essay titles, theme names, and front-matter fields when you know them. Vague verbs like "show," "fix," and "update" force the agent to guess.

## Reviewing the diff: red flags

Because the architecture has only a few hard rules, you can review most AI changes by scanning **which files were touched**. For routine work, any of these usually means the agent took a shortcut it shouldn't have — stop and ask it to redo the change at the config level:

- **Edited anything in `_layouts/` or `_includes/`** (including the essay templates like `essay-content.html` or `collection-nav.html`) — a config CSV, `theme.yml`, or an essay include almost always does the job.
- **Created a file under `items/`** — item pages are auto-generated from the metadata CSV; manual ones break the build.
- **Edited `_base.scss`, `_pages.scss`, `_theme-colors.scss`, `_color-tokens.scss`, `_essay.scss`, or `_print-paged.scss`** — custom styles belong only in `_sass/_custom.scss`; color and font changes belong in `_data/theme.yml`.
- **Recolored or re-fonted by editing SCSS** instead of changing `color-theme` / `base-font-family` in `_data/theme.yml`.
- **Reordered essays by renaming files** instead of changing the `order` front-matter field.
- **Added `.csv` to the `metadata:` pointer** in `_config.yml`, **wrote `site.data.metadata`** (must be `site.data[site.metadata]`), **used Bootstrap 4 classes** (`ml-`/`mr-`, `data-toggle=`), or **prefixed a `display_template`** with `item/`.

A clean change, by contrast, touches `_config.yml`, a `_data/*.csv`, `_data/theme.yml`, a file in `_essay/`, a page in `pages/`, or `_sass/_custom.scss` — and nothing else. (Deliberate larger changes are the exception — see "Going bigger" below.)

## When to slow the agent down

Let the AI move freely on additive, reversible changes (a new essay aside, an image gallery, a nav link, a theme swap you can revert). Ask it to explain its plan **before** editing when a change is broad or hard to undo:

- Restructuring or reordering columns in `_data/<metadata>.csv`
- Bulk edits across many item rows or many essay files
- Renumbering `order` across the whole `_essay/` folder
- Switching `color-theme` or `image-style` site-wide
- Anything that rewrites a config CSV's structure rather than adding or removing a row

## Going bigger: new templates, pages, and redesigns

The red-flags list above assumes routine, additive work. Larger changes — a new essay feature include, a custom landing page, a full visual redesign, a brand-new color theme — legitimately leave the config layer and touch `_layouts/`, `_includes/`, or `_sass/`. That's fine. The difference is that you're directing it **deliberately**, with a clear target in mind, rather than catching the AI taking a shortcut. When you go big, your job shifts from "watch which files it touches" to "give it a sharp brief and review the result against your vision."

### Briefing the AI for a big change

The single most useful thing you can do is **point the AI at an existing example to mirror**. CB-Essay ships working patterns for every feature; an AI that copies the structure of an existing essay include or layout stays consistent with the framework far better than one inventing from scratch. A strong brief usually includes:

- **The outcome, described richly** — what it should do, look like, or feel like. Adjectives, a reference site, a sketch, or a screenshot all help.
- **An existing file or feature to base it on** — "model it on `essay/feature/aside.html`," "match the structure of the `idaho` theme."
- **The rules that still apply** — essay includes for content, theming via `_data/theme.yml`, custom CSS in `_sass/_custom.scss` only, Bootstrap 5.
- **A request to plan first** for anything non-trivial.
- **Incremental delivery** — one piece at a time, building and checking as you go.

You don't need to know which files to edit. The AI does, from `AGENTS.md`. You bring the vision and the judgment.

### Sample prompts

**A new color theme:**

> I want a new color theme called `riverside` based on a deep teal with warm cream paper. Use `_prompts/add-theme.md` and model the structure on the existing `doves` theme. Pair it with a serif display font. Show me the palette and the `theme.yml` / color-token changes before applying anything.

**A new essay feature include:**

> Create a new essay include `essay/feature/pull-quote.html` for an oversized centered pull quote with optional attribution. Base it on `essay/feature/blockquote.html`, keep the markup Bootstrap 5, put any styles in `_sass/_custom.scss`, and don't touch the other includes. Walk me through your plan first.

**Overall look and feel (a redesign):**

> I want the site to feel calmer and more editorial — generous whitespace, the `nonesuch` color theme, themed fonts, and the `no-image` homepage style. Start by proposing the `_data/theme.yml` changes since that's the right first layer, and only reach for `_sass/_custom.scss` for what theme.yml can't express. Give me the theme.yml changes first so I can see the foundation.

Notice the shape these share: a clear target, an existing pattern to anchor to, the architecture rules restated, and a "plan first" or "foundation first" gate so you stay in control.

## Working rhythm

1. **One change at a time.** Rebuild (`bundle exec jekyll serve`) and look before moving on.
2. **Eyeball the CSV row or essay front matter** the agent added — small typos break features quietly.
3. **Preview print/PDF** separately when you change the `print:` settings — it renders through Paged.js at `/print/`.
4. **Keep `AGENTS.md` current** as the framework evolves; every agent inherits the improvements you make there.
5. **Your chat instructions override `AGENTS.md`.** If you tell an agent to do something the file forbids, it may comply — so don't fight your own rules without a reason.

## Where to find documentation

Point the agent at the `docs/` folder for details it needs. CB-Essay specifics live in `docs/cb-essay/` — `index.md`, `essay-writing.md`, `essay-features.md`, `theme-options.md`, and `gutenberg-extraction.md`. The inherited CB-CSV references (`docs/metadata.md`, `docs/markup.md`, `docs/maps.md`, `docs/color_theme.md`, `docs/advanced_theme.md`, and the rest) still apply. The official docs live at <https://collectionbuilder.github.io/cb-docs/>, and framework questions belong on the [discussion forum](https://github.com/CollectionBuilder/collectionbuilder.github.io/discussions).
