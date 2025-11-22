# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

CB-Essay is a Jekyll-based static site generator that extends CollectionBuilder-CSV to combine digital collection capabilities with essay/monograph writing. It allows authors to create multi-modal narratives that incorporate items from digital collections directly into essays using Liquid includes.

## Key Architecture

### Dual Collection System

The project manages two types of collections:

1. **Essay Collection** (`_essay/` directory): Long-form narrative content with sequential ordering
   - Defined in `_config.yml` under `collections.essay`
   - Uses `essay-content` layout by default
   - Supports sequential navigation (prev/next buttons)
   - URL pattern: `/essay/:slug`

2. **Object Collection** (CSV-based): Digital collection items loaded from metadata CSV
   - Metadata file specified in `_config.yml` as `metadata` field (default: `demo-compoundobjects-metadata`)
   - CSV files live in `_data/` directory
   - Items are generated via `_plugins/cb_page_gen.rb`

### Theme System

The site supports two base themes configured in `_data/theme.yml`:
- `essay`: Traditional essay format with linear reading
- `monograph`: Book-like format with table of contents on homepage

Theme selection affects navigation and homepage layout (`_layouts/home-essay.html`).

### Essay Features

Essay content can include specialized features via Liquid includes:
- `{% include essay/feature/blockquote.html %}`: Styled quotations
- `{% include feature/mini-map.html %}`: Embedded maps with custom coordinates
- `{% include essay/new-section.html %}`: Section breaks with scrollama transitions
- CollectionBuilder features: images, timelines, item cards from the metadata

These includes are located in `_includes/essay/` and `_includes/feature/`.

### Page Generation

Custom Jekyll plugin (`_plugins/cb_page_gen.rb`) generates individual pages for collection items based on metadata CSV. The plugin reads configuration from `_config.yml` (page_gen section, optional).

## Development Commands

### Initial Setup
```bash
bundle install
```

### Local Development
```bash
bundle exec jekyll s
```
- Serves at `http://127.0.0.1:4000`
- Uses "development" environment (skips analytics, some meta tags)
- Faster build time

### Production Build
```bash
rake deploy
```
or manually:
```bash
JEKYLL_ENV=production bundle exec jekyll build
```
- Outputs to `_site/` directory
- Includes all meta tags and analytics
- Significantly slower build
- Uses `url` and `baseurl` from `_config.yml` for absolute URLs

### Rake Tasks

Available tasks in `rakelib/`:
- `rake deploy`: Production build
- `rake generate_derivatives`: Process images for collection items
- `rake resize_images`: Batch resize images
- `rake download_by_csv`: Download objects from URLs in CSV
- `rake rename_by_csv`: Rename files based on CSV mapping
- `rake rename_lowercase`: Convert filenames to lowercase

See `docs/rake_tasks/` for detailed documentation on each task.

## Configuration Files

### Primary Configuration
- `_config.yml`: Site-wide settings, collection definitions, URLs, metadata source
- `_data/theme.yml`: Theme customization, colors, fonts, feature toggles, home page settings

### Metadata Configuration (CSV files in `_data/`)
- `config-browse.csv`: Browse page field display
- `config-metadata.csv`: Item page metadata display
- `config-map.csv`: Map feature configuration
- `config-nav.csv`: Navigation menu structure
- `config-search.csv`: Search page fields
- `config-table.csv`: Data table columns

## Important Notes

- When adding new essay content, create markdown files in `_essay/` with front matter including `title`, `order`, and optional `byline`
- The `order` field in essay front matter determines sequential navigation order
- Object metadata CSV must be placed in `_data/` and filename (without .csv) specified in `_config.yml`
- Compound objects (parent-child relationships) are supported through metadata structure
- Built site in `_site/` is excluded from git (see `.gitignore`)
- All feature includes expect specific parameters - check include files for required/optional parameters
- **For comprehensive development guidelines**, see [Agents.md](Agents.md) - detailed guide for AI agents including decision trees, troubleshooting, and best practices
