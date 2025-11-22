# CB-Essay Development Guidelines for AI Agents

## Overview
CB-Essay extends CollectionBuilder-CSV with essay/monograph authoring capabilities. This document outlines best practices for customizing CB-Essay repositories, helping you work WITH the framework's dual collection system (essays + digital objects) while maintaining compatibility with CollectionBuilder's infrastructure.

## Essential Commands

### Quick Command Reference:
- **Local development**: `bundle exec jekyll serve`
- **After config changes**: Restart Jekyll server (crucial!)
- **Generate thumbnails**: `rake generate_derivatives`
- **Large collections**: `rake generate_json`
- **Troubleshoot build**: `bundle exec jekyll build --verbose`
- **Test site**: Visit `http://localhost:4000`

## Quick Reference for AI Agents

### CB-Essay Specific Tasks:
- **Add essay content**: Create markdown in `_essay/` with front matter (`title`, `order`, `byline`)
- **Essay features**: Use `_includes/essay/feature/` includes (blockquote, map, item spotlight)
- **Theme mode**: Change `base-theme` in `_data/theme.yml` (essay or monograph)
- **Homepage**: Customize `_layouts/home-essay.html` or `_data/theme.yml` (featured-image, image-style)
- **Essay navigation**: Sequential prev/next via `order` field in front matter

### Most Common CollectionBuilder Tasks:
- **Navigation change**: Update `_data/config-nav.csv`
- **Browse customization**: Modify `_data/config-browse.csv`
- **Styling**: Use Bootstrap classes → `_sass/_custom.scss` → `_data/config-theme-colors.csv` for bootstrap color changes
- **New component**: Create in `_includes/` → Use `_includes/feature/` components first
- **New item type**: Add `display_template` to CSV → Create layout in `_layouts/item/` → Extend `_layouts/item/item-page-base.html`

### File Priority Order:
1. Essay markdown files (`_essay/*.md`)
2. CSV config files (`_data/*.csv`)
3. Existing feature includes (`_includes/feature/*.html` and `_includes/essay/feature/*.html`)
4. `_data/theme.yml` settings
5. Custom includes (`_includes/`)
6. Custom CSS (`_sass/_custom.scss`)

### ⚠️ Critical Don'ts:
- **DON'T** create monolithic layouts - extend existing base layouts
- **DON'T** rebuild Bootstrap components or media embed components - use options in `_includes/feature/`
- **DON'T** modify `_layouts/essay-content.html` without understanding scrollama integration

## 🚨 Emergency Troubleshooting

### Site Won't Build:
1. **Check YAML syntax**: `_config.yml:1` (YAML is space-sensitive - no tabs!)
2. **Verify metadata**: No duplicate `objectid` values in `_data/[metadata-file].csv:1`
3. **Check layouts exist**: All `display_template` values must have matching files in `_layouts/item/`
4. **Restart server**: After ANY config file changes, restart `bundle exec jekyll serve`

### Pages Not Generating:
- Item pages generate at `/items/{objectid}.html` via `_plugins/cb_page_gen.rb:34`
- Check `objectid` values are URL-safe (no spaces, special chars)
- Verify `display_template` matches layout filename in `_layouts/item/`

### Navigation Broken:
- Navigation processes in `_includes/nav/nav.html:15`
- Check `_data/config-nav.csv:1` format: `display_name,stub,dropdown_parent`
- Ensure stub URLs start with `/`

### Search/Browse Issues:
- Search config: `_data/config-search.csv:1`
- Browse config: `_data/config-browse.csv:1`
- Metadata config: `_data/config-metadata.csv:1`
- Clear browser cache and restart server

---

## Core Principles

### 1. **Work WITH the Framework, Not Against It**
- Leverage existing CollectionBuilder and OHD components instead of rebuilding functionality
- Extend existing layouts rather than creating entirely new ones
- Use the modular include system for reusable components

### 2. **Configuration-Driven Customization**
- Use `_data/theme.yml:1` for display and styling options on specific pages -- Homepage, browse, subjects, locations, map, timeline, data exports, compound objects behavior and some styles
- Minimize custom code when configuration can achieve the same result

### 3. **Modular Architecture**
- Keep layouts small and focused
- Use `_includes` for reusable components
- Build on existing base layouts

## CB-Essay Architecture

### Dual Collection System
CB-Essay manages two types of collections simultaneously:

**1. Essay Collection** (`_essay/` directory)
- Long-form narrative content with sequential ordering
- Front matter fields: `title`, `order`, `byline`, optional `featured-image`
- Uses `essay-content` layout by default
- Sequential navigation (prev/next) based on `order` field
- URL pattern: `/essay/:slug`

**2. Object Collection** (CSV-based)
- Digital collection items from metadata CSV in `_data/`
- Specified via `metadata` field in `_config.yml`
- Generated as `/items/{objectid}.html` pages
- Can be embedded in essays using `{% include feature/... %}` includes

### Essay-Specific Features

**Theme Modes** (`_data/theme.yml`)
- `base-theme: essay` - Traditional essay with linear reading flow
- `base-theme: monograph` - Book format with table of contents on homepage

**Essay Includes** (`_includes/essay/feature/`)
- `blockquote.html` - Styled quotations with optional speaker attribution
- `mini-map.html` - Embedded maps with custom coordinates
- Section breaks and scrollama transitions
- All standard CollectionBuilder `feature/` includes work in essays

**Homepage Layouts**
- `home-essay.html` - Custom homepage with featured image and essay entry point
- Image styles: `full-image`, `half-image`, `no-image`
- Table of contents for monograph mode

### Decision Trees:

#### When User Asks About Essays:
1. **New essay chapter?** → Create `.md` in `_essay/` with front matter
2. **Essay feature (quote, map, etc.)?** → Use `_includes/essay/feature/` includes
3. **Embed collection item?** → Use `{% include feature/image.html objectid="..." %}` or similar
4. **Essay styling?** → Adjust `base-font-size`, `text-color`, `font-family` in `theme.yml`
5. **Change essay/monograph mode?** → Update `base-theme` in `theme.yml`
6. **Homepage customization?** → Modify `featured-image`, `image-style` in `theme.yml`

#### When User Asks About Styling:
1. **Is it a color change?** → `config-theme-colors.csv`
2. **Is it Bootstrap-available?** → Use Bootstrap classes
3. **Is it component-specific?** → `_sass/_custom.scss`
4. **Is it a new feature?** → Inline styles in include

#### When User Asks About Data Display:
1. **Browse page?** → `config-browse.csv`
2. **Item metadata?** → `config-metadata.csv`
3. **Search functionality?** → `config-search.csv`
4. **Navigation?** → `config-nav.csv`
5. **Map pop up?** → `config-map.csv`

#### When User Asks About Adding Content:
1. **In an essay?** → Use essay-specific includes in `_includes/essay/feature/`
2. **Need an image/video/audio?** → `feature/image.html`, `feature/video.html`, `feature/audio.html`
3. **Need a card/modal/alert?** → `feature/card.html`, `feature/modal.html`, `feature/alert.html`
4. **Need interactive elements?** → `feature/accordion.html`, `feature/button.html`
5. **Truly custom component?** → Create in `_includes/` (last resort)

#### When User Asks About New Item Types:
1. **Similar to existing type?** → Copy and modify existing `_layouts/item/` file
2. **Needs audio/video?** → Extend from existing audio/video layouts
3. **Basic display?** → Extend from `item.html`
4. **Complex features?** → Extend from `item-page-base.html`

#### When User Asks About Site Structure:
1. **New essay chapter?** → Add markdown to `_essay/` directory
2. **New standard page?** → Create in `pages/` with existing layout
3. **Homepage changes?** → Modify `_layouts/home-essay.html` or `theme.yml` settings
4. **Collection organization?** → Update metadata CSV `display_template` field
5. **Site-wide settings?** → `theme.yml` configuration


## Key Configuration Files in `_data/`

### Essential CSV Configuration Files

#### `config-nav.csv`
Controls site navigation structure:
```csv
display_name,stub,dropdown_parent
About,/about.html
Episodes,/episodes.html
Browse by
Subjects,/subjects.html,Browse by
Map,/map.html,Browse by
```
- `display_name`: Text shown in navigation
- `stub`: URL path (relative to site root)
- `dropdown_parent`: Groups items under dropdown menus

#### `config-browse.csv`
Configures browse/search page display:
```csv
field,display_name,btn,hidden,sort_name
interviewer,Host
date,Date,,,Date
subject,Topics,true
location,,true
```
- `field`: Metadata field name
- `display_name`: Label shown to users
- `btn`: Show as filter button (true/false)
- `hidden`: Hide from display but keep searchable
- `sort_name`: Alternative name for sorting

#### `config-metadata.csv`
Controls item page metadata display:
```csv
field,display_name,browse_link,external_link,dc_map,schema_map
title,Title,,,DCTERMS.title,headline
interviewer,Host,,,DCTERMS.creator,creator
interviewee,Guest,true,,DCTERMS.contributor,contributor
subject,Topics,true,,DCTERMS.subject,keywords
```
- `browse_link`: Make field values clickable links to browse results
- `external_link`: Make field values external links
- `dc_map` & `schema_map`: SEO and metadata mapping

#### `config-search.csv`
Defines search functionality:
```csv
field,index,display
title,true,true
description,true,true
interviewer,true,false
subject,true,true
```
- `index`: Include in search index
- `display`: Show in search results

#### `config-theme-colors.csv`
Bootstrap color theme customization:
```csv
color_class,color
primary,#FFD700
secondary,#F4D03F
warning,#B8860B
```

### `theme.yml` Configuration
Central configuration for display options:

```yaml
# PAGE DISPLAY OPTIONS
featured-image: demo_033                    # homepage banner image (objectid/path/URL)
advanced-search: true                      # enable advanced search modal
browse-buttons: true                       # previous/next on item pages
subjects-fields: subject;creator           # fields for subject cloud page
map-cluster: true                         # cluster map markers
year-nav-increment: 5                     # timeline year navigation

# DATA EXPORTS & SEARCH  
metadata-export-fields: "title,creator,date"    # CSV download fields
metadata-facets-fields: "subject,creator"       # search filter fields

# COMPOUND OBJECTS
browse-child-objects: false               # include child objects in browse/search
map-child-objects: true                  # show child objects on map

# BASIC STYLING
navbar-color: navbar-dark                # navbar-light or navbar-dark  
bootswatch:                             # optional Bootswatch theme name
base-font-size: 1.2em                  # custom font sizing
```

**Key Areas:** Page behavior, visualization settings, data exports, compound object handling, basic styling.  
**When to use:** Feature toggles, display logic, performance options. Use CSV config files for field-specific settings.

## Layout Architecture

### CB-Essay Layout Hierarchy
```
default.html (base HTML structure)
├── page.html (standard page wrapper)
├── home-essay.html (CB-Essay custom homepage)
├── essay-content.html (essay chapter layout with scrollama)
├── item/item-page-base.html (item page foundation)
│   ├── item/image.html (image layout)
│   ├── item/audio.html (audio file layout)
│   └── item/video.html (video layout)
└── browse.html, map.html, timeline.html, etc. (CollectionBuilder pages)
```

### Essay Front Matter Example
```yaml
---
title: Of a Monstrous Child
byline: Michel de Montaigne
order: 5
featured-image: /assets/img/custom-image.jpg  # optional
---

Essay content here with embedded collection items...

{% include essay/feature/blockquote.html quote="..." speaker="..." %}
{% include feature/image.html objectid="demo_001" width="75" %}
{% include feature/mini-map.html latitude="43.899" longitude="4.690" %}
```

### Best Practices for Layouts

#### ✅ **DO: Extend Existing Base Layouts**
```yaml
---
layout: item/item-page-base  # Build on _layouts/item/item-page-base.html:1
custom-foot: transcript/js/transcript-js.html
---
# Add custom content here
{% include transcript/item/av.html %}
{% include transcript/item/episode-metadata.html %}
```

#### ❌ **DON'T: Create Monolithic Layouts**
```yaml
---
layout: default
---
<!-- 200+ lines of mixed HTML, logic, and styling -->
<div class="massive-single-purpose-layout">
  <!-- Everything hardcoded here -->
</div>
```

#### ✅ **DO: Use Modular Includes**
```html
<!-- _layouts/item/episode.html -->
{% include transcript/item/av.html %}
{% include transcript/item/episode-metadata.html %}
{% include transcript/item/bio-modal.html %}
```

#### ✅ **DO: Create Specialized Include Components**
```html
<!-- _includes/episode-card.html -->
<div class="episode-card">
  <!-- Reusable episode card component -->
</div>

<!-- _includes/transcript/item/episode-metadata.html -->
<div class="episode-metadata">
  <!-- Custom metadata display for episodes -->
</div>
```

## Working with Metadata

### Complete Metadata Field Reference

#### Required Fields:
- `objectid`: Unique identifier (generates `/items/{objectid}.html`)
- `title`: Item title

#### Core Display Fields:
- `display_template`: Routes to layout in `_layouts/item/` (e.g., "image", "audio", "video")
- `object_location`: Path/URL to media file
- `image_thumb`: Thumbnail image path
- `image_small`: Small image path

#### Geographic Fields:
- `latitude`: For map display
- `longitude`: For map display
- `location`: Place name (searchable)

#### Metadata Fields:
- `creator`: Author/creator
- `date`: Date (YYYY-MM-DD or YYYY for timeline)
- `description`: Item description
- `subject`: Topics (semicolon-separated)
- `format`: File type
- `rights`: Rights statement
- `identifier`: Original ID

#### Custom Fields:
- Any additional columns become automatically searchable
- Configure display in `_data/config-metadata.csv:1`
- Enable browse filtering in `_data/config-browse.csv:1`

### CSV Metadata Structure
Main collection metadata in `_data/metadata.csv:1` (or configured filename in `_config.yml:37`):

```csv
objectid,title,display_template,creator,date,description,subject,object_location
episode001,Episode Title,episode,Host Name,2024-01-01,Description,topic1; topic2,/objects/audio.mp3
```

**Key Fields:**
- `objectid`: Unique identifier (generates `/items/{objectid}.html`)
- `display_template`: Determines which layout in `_layouts/item/` to use
- `object_location`: Path to media files
- Custom fields: Add any additional metadata columns

### Display Template Routing
CollectionBuilder automatically routes items based on `display_template` (via `_plugins/cb_page_gen.rb:34`):
- `display_template: episode` → `_layouts/item/episode.html:1`
- `display_template: transcript` → `_layouts/item/transcript.html:1`
- `display_template: audio` → `_layouts/item/audio.html:1`

## Include Directory Organization

### CB-Essay Include Organization
```
_includes/
├── essay/             # CB-ESSAY SPECIFIC INCLUDES
│   ├── feature/       # Essay-specific feature components
│   │   └── blockquote.html  # Styled quotations
│   ├── js/            # Essay JavaScript (scrollama, etc.)
│   ├── side-nav.html  # Essay navigation
│   ├── top-cover.html # Essay cover images
│   └── off-canvas-*.html    # Essay menus
├── feature/           # Bootstrap-based reusable components (USE THESE FIRST!)
│   ├── image.html     # Responsive image display (works in essays!)
│   ├── card.html      # Bootstrap card component
│   ├── audio.html     # Audio player embed
│   ├── video.html     # Video player embed
│   ├── mini-map.html  # Embedded maps (great for essays!)
│   ├── gallery.html   # Image gallery
│   ├── accordion.html # Bootstrap accordion
│   ├── modal.html     # Bootstrap modal
│   ├── alert.html     # Bootstrap alert
│   ├── button.html    # Styled buttons
│   ├── jumbotron.html # Hero sections
│   └── nav-menu.html  # Custom navigation
├── head/              # HTML head components
├── item/              # Item page components
│   ├── audio-player.html
│   ├── download-buttons.html
│   └── metadata.html
├── index/             # Homepage components
│   ├── carousel.html
│   ├── featured-terms.html
│   └── description.html
└── js/                # JavaScript components
```

### Feature Includes - The Power of CollectionBuilder

**The `_includes/feature/` directory is your secret weapon.** These pre-built, Bootstrap-styled components should be your **first choice** for adding content. They handle responsive design, accessibility, and consistent styling automatically.

#### Essential Feature Components

**Image Display** (`feature/image.html`):
```liquid
{% include feature/image.html objectid="demo_001" %}
{% include feature/image.html objectid="demo_001;demo_002" width="50" %}
{% include feature/image.html objectid="https://example.com/image.jpg" alt="Description" caption="Custom caption" %}
```
- Supports collection objectids, external URLs, or local image paths
- Automatic responsive sizing with width options (25%, 50%, 75%, 100%)
- Built-in accessibility features and captions

**Cards** (`feature/card.html`):
```liquid
{% include feature/card.html text="Card content" header="Card Header" objectid="demo_001" %}
{% include feature/card.html text="Right-aligned card" width="50" float="end" centered="true" %}
```
- Bootstrap card styling with image caps
- Flexible positioning (float, center, width control)
- Header, title, and content areas

**Audio/Video Players** (`feature/audio.html`, `feature/video.html`):
```liquid
{% include feature/audio.html objectid="demo_audio" %}
{% include feature/video.html objectid="https://youtu.be/VIDEOID" %}
{% include feature/video.html objectid="https://vimeo.com/VIDEOID" ratio="4by3" %}
```
- Supports multiple platforms (YouTube, Vimeo, local files)
- Responsive video embedding with aspect ratio control

**Interactive Components**:
```liquid
{% include feature/modal.html title="Modal Title" text="Modal content" button="Open Modal" %}
{% include feature/accordion.html title1="Section 1" text1="Content 1" title2="Section 2" text2="Content 2" %}
{% include feature/alert.html text="Important notice" color="warning" %}
{% include feature/button.html text="Click Me" link="/page.html" color="primary" %}
```

### Essay-Specific Include Usage

**Blockquote Feature** (`essay/feature/blockquote.html`):
```liquid
{% include essay/feature/blockquote.html
   quote="Your quote text here"
   speaker="Attribution - optional" %}
```

**Embedding Collection Items in Essays**:
```liquid
{% include feature/image.html objectid="demo_001" width="50" caption="Item from collection" %}
{% include feature/mini-map.html latitude="43.899" longitude="4.690" basemap="Stadia_StamenToner" %}
{% include feature/card.html text="Custom text" objectid="demo_002" %}
```

### Creating Custom Includes

#### Component Naming Convention
- Use descriptive, hyphenated names: `essay-highlight.html`
- Group by functionality: `essay/feature/timeline.html`
- Include header comments for documentation:

```html
<!-- cb: _includes/essay/feature/essay-highlight.html -->
<!-- Essay highlight component for emphasizing key passages -->
<div class="essay-highlight">
  <!-- Component content -->
</div>
<!-- /cb: _includes/essay/feature/essay-highlight.html -->
```

## Styling Approach

### Color Customization: Use `config-theme-colors.csv`

**For Bootstrap color overrides, use `_data/config-theme-colors.csv:1`:**

```csv
color_class,color
primary,#FFD700
secondary,#F4D03F
warning,#B8860B
success,#28a745
info,#17a2b8
```

### Sass Variables: Use `assets/css/cb.scss`

**For custom Sass variables, modify `assets/css/cb.scss:1`:**

```scss
---
# base CSS for collectionbuilder
---
@charset "utf-8";

/* Custom Sass variables */
$podcast-primary: #FFD700;
$podcast-secondary: #F4D03F;
$episode-border-radius: 12px;

/* Continue with existing base variables... */
```

### Repository-Level Customization: Use `_sass/_custom.scss`

**For component styles and CSS overrides, use `_sass/_custom.scss:1`:**

```scss
/* _sass/_custom.scss */

/* Custom component styles - NO color variables here */
.episode-card {
  border: 2px solid var(--bs-warning); /* Use Bootstrap CSS variables */
  border-radius: 12px;
  transition: all 0.3s ease;

  &:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 20px rgba(0,0,0,0.15);
  }
}

/* Responsive utilities */
@media (max-width: 768px) {
  .episode-card {
    margin-bottom: 1rem;
  }
}
```

**Why this structure?**
- `config-theme-colors.csv`: Bootstrap color theme integration
- `assets/css/cb.scss`: Sass variables and Jekyll processing
- `_sass/_custom.scss`: Component styles and CSS overrides
- Maintains proper compilation order and compatibility

### Component-Level Styling: Inline for New Features

Only use inline styles for **new feature components** or **one-off custom includes**:

```html
<!-- _includes/episode-card.html -->
<div class="episode-card">
  <!-- Component content -->
</div>

<style>
/* Component-specific styles for new features only */
.episode-card-specific-feature {
  /* Styles that only apply to this component */
}
</style>
```

### Bootstrap Integration
CollectionBuilder includes Bootstrap 5. **Always prefer Bootstrap classes:**

```html
<!-- ✅ GOOD: Use Bootstrap classes -->
<div class="row g-4">
  <div class="col-lg-4 col-md-6 col-sm-12">
    <div class="card border-warning">
      <div class="card-body text-center">
        <!-- Content -->
      </div>
    </div>
  </div>
</div>

<!-- ❌ AVOID: Custom CSS when Bootstrap exists -->
<div class="custom-grid">
  <div class="custom-column">
    <div class="custom-card">
      <!-- Reinventing Bootstrap -->
    </div>
  </div>
</div>
```

### File Organization for Styling
```
_sass/
├── _custom.scss:1      # Component styles and CSS overrides
├── _base.scss:1        # CollectionBuilder base styles
├── _ohd.scss:1         # OHD-specific styles
├── _pages.scss:1       # Page-specific styles
└── _theme-colors.scss:1 # Bootstrap color overrides

_data/
└── config-theme-colors.csv:1 # Bootstrap color theme configuration

assets/css/
└── cb.scss:1          # Sass variables and Jekyll processing
```

## Generated Data Files (`assets/data/`)

CollectionBuilder automatically generates reusable data files in `assets/data/` that serve multiple purposes:

### Auto-Generated Data Outputs (DO NOT EDIT - Generated by Jekyll)
```
assets/data/
├── metadata.csv:1     # Downloadable metadata export
├── metadata.json:1    # JSON version for APIs
├── subjects.csv:1     # Subject terms and counts
├── subjects.json:1    # Subject data for visualizations
├── locations.csv:1    # Location data export
├── geodata.json:1     # Geographic data for maps
├── timelinejs.json:1  # Timeline.js compatible data
├── facets.json:1      # Search facet data
└── collection-info.json:1 # Collection statistics
```

### How These Files Are Used

**Download Features:**
- `metadata.csv` - Provides "Download Data" functionality on data page
- `subjects.csv`, `locations.csv` - Specialized data exports
- Generated from `metadata-export-fields` in `theme.yml`

**Visualization Features:**
- `geodata.json` - Powers map visualizations
- `timelinejs.json` - Timeline.js integration
- `subjects.json` - Subject cloud displays
- `facets.json` - Advanced search filtering

**API Integration:**
- All `.json` files provide API endpoints for external tools
- Used by some advanced CollectionBuilder features
- Enable integration with external visualization tools

## CollectionBuilder's Data-Driven Page Patterns

CollectionBuilder uses a powerful pattern of combining Liquid/Jekyll data processing with Bootstrap components and JavaScript libraries to create dynamic, interactive pages.

### Pattern 1: Pure Liquid/Jekyll (Server-Side)

**Example: Timeline Navigation**
```liquid
{%- assign items = site.data[site.metadata] | where_exp: 'item','item.objectid' -%}
{%- assign items = items | where_exp: 'item','item[field]' | sort: field -%}
{%- assign raw-dates = items | map: field | compact | uniq -%}
{%- capture clean-years -%}
  {% for date in raw-dates %}
    {% if date contains "-" %}{{ date | strip | split: "-" | first }}
    {% elsif date contains "/" %}{{ date | strip | split: "/" | last }}
    {% else %}{{ date | strip }}{% endif %}
    {% unless forloop.last %};{% endunless %}
  {% endfor %}
{%- endcapture -%}
{%- assign uniqueYears = clean-years | split: ";" | compact | uniq | sort -%}
```

**Key Techniques:**
- **Data filtering**: `where_exp` for complex conditions
- **Data transformation**: `map`, `split`, `join` for processing
- **Liquid capture**: Build strings dynamically
- **Bootstrap integration**: Generate dropdown navigation

### Pattern 2: Liquid + JavaScript (Hybrid)

**Example: Interactive Map**
```liquid
<!-- _layouts/map.html -->
---
layout: default
custom-foot: js/map-js.html
---
<div id="map"></div>

<!-- _includes/js/map-js.html -->
{%- assign items = site.data[site.metadata] | where_exp: 'item','item.latitude != nil and item.longitude != nil' -%}
{%- assign fields = site.data.config-map -%}

<script>
var geodata = { "type": "FeatureCollection", "features": [
{% for item in items %}
{ "type":"Feature",
  "geometry":{ "type":"Point", "coordinates":[{{ item.longitude }},{{ item.latitude }}] },
  "properties": {
    {% for f in fields %}
      {% if item[f.field] %}{{ f.field | jsonify }}:{{ item[f.field] | strip | escape | jsonify }},{% endif %}
    {% endfor %}
    "objectid": {{ item.objectid | jsonify }}
  }
}{% unless forloop.last %},{% endunless %}
{% endfor %}
]};

// Initialize Leaflet map with generated data
var map = L.map('map').setView([{{ site.data.theme.latitude }}, {{ site.data.theme.longitude }}], {{ site.data.theme.zoom-level }});
// Add markers from geodata...
</script>
```

**Key Techniques:**
- **Liquid preprocessing**: Filter and transform data on build
- **JSON generation**: Create JavaScript data structures with `jsonify`
- **Configuration integration**: Use `config-map.csv` for field display
- **JavaScript libraries**: Leaflet maps, clustering, search
- **Bootstrap components**: Modals, cards for map popups

### Pattern 3: Bootstrap Component Integration

**Example: Dynamic Carousel**
```liquid
<!-- _includes/index/carousel.html -->
{%- assign carousel-max = include.max | default: 9 -%}
{%- if include.child-objects == true -%}
  {%- assign items = site.data[site.metadata] | where_exp: 'item','item.objectid' -%}
{%- else -%}
  {%- assign items = site.data[site.metadata] | where_exp: 'item','item.objectid and item.parentid == nil' -%}
{%- endif -%}

{% if include.filter-field and include.filter-value %}
  {%- assign items = items | where_exp: 'item', 'item[include.filter-field] contains include.filter-value' -%}
{% endif %}

{%- assign items = items | where_exp: 'item','item.image_thumb' | sample: carousel-max -%}

<div id="carouselFade" class="carousel slide carousel-fade" data-bs-ride="carousel">
  <div class="carousel-inner">
    {% for item in items %}
      <div class="carousel-item{% if forloop.first %} active{% endif %}">
        <img class="d-block w-100" src="{{ item.image_thumb | relative_url }}" alt="{{ item.title | escape }}">
        <div class="carousel-caption">
          <h5>{{ item.title }}</h5>
          <a href="{{ '/items/' | append: item.objectid | append: '.html' | relative_url }}" class="btn btn-{{ include.btn-color | default: 'primary' }}">
            {{ include.btn-text | default: 'View Item' }}
          </a>
        </div>
      </div>
    {% endfor %}
  </div>
</div>
```

**Key Techniques:**
- **Flexible filtering**: Runtime filters via include parameters
- **Random sampling**: `sample` filter for variety
- **Bootstrap carousel**: Native component with Liquid data
- **Configurable styling**: Bootstrap color classes via parameters

### Best Practices for Data-Driven Pages

#### ✅ **DO: Follow CollectionBuilder Patterns**
```liquid
<!-- 1. Define data processing at top -->
{%- assign items = site.data[site.metadata] | where_exp: 'item','item.objectid' -%}
{%- assign filtered_items = items | where: 'display_template', 'episode' -%}

<!-- 2. Use configuration files -->
{%- assign fields = site.data.config-browse -%}

<!-- 3. Generate clean JSON for JavaScript -->
var episodes = [
{% for item in filtered_items %}
{
  "id": {{ item.objectid | jsonify }},
  "title": {{ item.title | escape | jsonify }},
  "date": {{ item.date | jsonify }}
}{% unless forloop.last %},{% endunless %}
{% endfor %}
];

<!-- 4. Integrate with Bootstrap -->
<div class="row">
  {% for item in filtered_items %}
    <div class="col-md-4">
      <div class="card">
        <!-- Bootstrap card with Liquid data -->
      </div>
    </div>
  {% endfor %}
</div>
```

#### ❌ **DON'T: Fight the System**
```liquid
<!-- Don't hardcode data -->
var episodes = [
  {"id": "ep1", "title": "Episode 1"},
  {"id": "ep2", "title": "Episode 2"}
];

<!-- Don't bypass configuration -->
<div class="custom-grid">
  <!-- Custom HTML instead of Bootstrap -->
</div>

<!-- Don't ignore CollectionBuilder filters -->
{% for item in site.data.metadata %}
  <!-- Processing ALL items instead of using CB patterns -->
{% endfor %}
```

### Customizing Generated Data

**Configure exports in `_data/theme.yml:70`:**
```yaml
# Specify which fields to include in data downloads
metadata-export-fields: "objectid,title,creator,date,description,subject,location,rights"

# Control what gets included in faceted search
metadata-facets-fields: "subject,creator,format"
```

**Important Notes:**
- These files regenerate automatically when site builds
- Don't edit them directly - they'll be overwritten
- Configure what's included via `theme.yml` and config CSV files
- For large collections, use `rake generate_json` for performance

## Data Access Patterns

### Accessing Essay Collection
```liquid
{%- assign essays = site.essay | sort: 'order' -%}
{%- assign essay_count = site.essay.size -%}

{% for essay in essays %}
  <h2>{{ essay.title }}</h2>
  <p>{{ essay.byline }}</p>
{% endfor %}
```

### Accessing Collection Data (Items)
```liquid
{%- assign items = site.data[site.metadata] | where_exp: 'item','item.objectid' -%}
{%- assign featured_count = site.data.theme.featured-items | default: 6 -%}
```

### Configuration Access
```liquid
{%- assign base_theme = site.data.theme.base-theme -%}
{% if site.data.theme.base-theme == 'monograph' %}
  <!-- Display table of contents -->
{% endif %}
```

### Filtering and Sorting
```liquid
{% assign recent_items = site.data[site.metadata]
   | where_exp: 'item','item.objectid'
   | sort: "date"
   | reverse
   | limit: 6 %}
```

## Common Customization Patterns

### Adding New Essays
1. Create markdown file in `_essay/` directory
2. Add front matter with `title`, `order`, and optional `byline`
3. Write content using markdown and CollectionBuilder includes
4. Essays automatically appear in sequential navigation

### Adding New Item Types
1. Add new `display_template` value to metadata CSV
2. Create layout in `_layouts/item/{template-name}.html`
3. Extend from `item-page-base.html`
4. Use existing includes where possible

### Customizing Browse Pages
1. Update `config-browse.csv` for field display
2. Add custom styling in page markdown file
3. Use existing browse layout with custom CSS

### Adding Navigation Items
1. Update `config-nav.csv`
2. Create corresponding page in `pages/`
3. Use appropriate existing layout

## Working with Essays and Collections Together

### Embedding Collection Items in Essays
CB-Essay's power comes from seamlessly integrating collection items into narrative essays:

```liquid
<!-- In an essay markdown file (_essay/chapter-01.md) -->

Michel de Montaigne wrote about strange phenomena in his essay collection.

{% include feature/image.html objectid="demo_012" width="75" caption="Historical illustration" %}

The concept of the "monstrous" in Renaissance thought reflects...

{% include essay/feature/blockquote.html
   quote="What we call monsters are not so to God..."
   speaker="Montaigne" %}

{% include feature/mini-map.html latitude="43.899" longitude="4.690" basemap="Stadia_StamenToner" map-zoom="9" %}
```

### Essay Configuration in theme.yml

**Essay-specific settings** (in addition to standard CollectionBuilder config):
```yaml
## CB-Essay specific
base-theme: essay  # or monograph for book-style TOC
base-font-size: 1.3em
text-color: "#191919"
link-color: "#0d6efd"
base-font-family: Georgia
image-style: full-image  # full-image, half-image, or no-image
featured-image: /assets/img/writing-instruments.jpg
home-title-y-padding: 10em
```

### Search and Browse
- **Essays are separate** from collection search/browse (essays are not indexed in site search)
- Collection items: Configure search in `config-search.csv`
- Essays: Navigate via sequential prev/next buttons or homepage TOC (if monograph mode)
- Collection browse/search pages show items only, not essay content

### Visualizations
CollectionBuilder visualization features work with collection items:
- Timeline views (items only, not essay chapters)
- Subject clouds (from collection metadata)
- Location maps (from collection geographic data)
- **Essays can embed** collection visualizations (maps, images, galleries) inline using includes

Enable through `theme.yml` configuration rather than rebuilding.

## Testing & Validation Guide

### Before Committing Changes:
1. **Build test**: `bundle exec jekyll build --verbose`
2. **Local preview**: `bundle exec jekyll serve` → test at `http://localhost:4000`
3. **Check navigation**: All menu items work
4. **Test search/browse**: Verify filtering and results
5. **Mobile test**: Check responsive design
6. **Page generation**: Verify new items appear at `/items/{objectid}.html`
7. **Configuration**: Test any CSV config changes

### Quick Validation:
- No build errors in terminal
- All pages load without 404s
- Search returns expected results
- New metadata fields display correctly

## ⚠️ Common Pitfalls

### Critical Mistakes to Avoid:
- ❌ **Not restarting server** after config changes (`_config.yml`, `theme.yml`, CSV files)
- ❌ **Creating custom Bootstrap CSS** instead of using `_data/config-theme-colors.csv:1`
- ❌ **Editing auto-generated files** in `assets/data/` (they get overwritten)
- ❌ **Using tabs in YAML** files (use spaces only)
- ❌ **Duplicate `objectid` values** in metadata CSV
- ❌ **Missing layouts** for `display_template` values
- ❌ **Hardcoding paths** instead of using Jekyll variables
- ❌ **Ignoring build warnings** (they often indicate real problems)

### Performance Issues:
- Collections >1000 items: Set `json-generation: true` in `_data/theme.yml:1`
- Large images: Run `rake generate_derivatives` first
- Slow searches: Limit search fields in `_data/config-search.csv:1`

## Troubleshooting Common Issues

### Pages Not Generating
- Check `display_template` values in metadata CSV
- Ensure layout file exists in `_layouts/item/`
- Verify `objectid` values are unique and URL-safe

### Includes Not Found
- Check file paths in `_includes/`
- Verify include statements use correct path
- Ensure file extensions are `.html`

### Configuration Not Applied
- Verify CSV files have proper headers
- Check `_data/theme.yml:1` syntax (YAML is space-sensitive)
- Restart Jekyll development server after config changes

## Migration from Hardcoded Customizations

If converting existing hardcoded customizations:

1. **Extract Reusable Components** → Move to `_includes/`
2. **Identify Configuration Options** → Move to CSV files or `theme.yml`
3. **Simplify Layouts** → Use base layouts and includes
4. **Test Functionality** → Ensure all features still work

## Development Tools and Automation

### Rake Tasks (`rakelib/` directory)

CollectionBuilder includes powerful Rake tasks for common development and maintenance operations:

#### Image Processing (`rake generate_derivatives`)
```bash
rake generate_derivatives
```
- Automatically generates thumbnail and small images from objects/ directory
- Optimizes images for web delivery
- Creates PDF thumbnails from first page
- Handles large collections efficiently

#### Bulk Operations
```bash
rake rename_by_csv          # Bulk rename files using CSV mapping
rake rename_lowercase       # Convert all filenames to lowercase
rake resize_images          # Batch resize images to specific dimensions
rake download_by_csv        # Download remote files listed in CSV
```

#### JSON Generation for Large Collections (`rake generate_json`)
```bash
rake generate_json
```
- Creates optimized JSON files for visualization features
- Essential for collections with 1000+ items
- Improves page load performance
- Must set `json-generation: true` in `theme.yml` first

### Jekyll Plugins (`_plugins/` directory)

#### Page Generator (`_plugins/cb_page_gen.rb:1`)
**Core functionality**: Automatically generates item pages from CSV metadata.

- Reads metadata CSV and creates `/items/{objectid}.html` pages
- Routes pages to appropriate layouts based on `display_template` field
- Handles URL slugification and validation
- Configured via `_config.yml` `page_gen` settings

#### Helper Functions (`_plugins/cb_helpers.rb:1`)
**Liquid filters and utilities**:
```liquid
{{ item.subject | array_count_uniq }}        # Count unique values in arrays
{{ page.description | strip_html | truncate: 150 }}  # Text processing helpers
```

#### Data Processing (`array_count_uniq.rb`)
**Array manipulation filters** for processing metadata fields with multiple values.

### When to Use These Tools

#### Use Rake Tasks When:
- Setting up a new collection with many images
- Migrating from another platform
- Batch processing existing files
- Optimizing site performance

#### Modify Plugins When:
- Changing page generation logic (advanced)
- Adding custom Liquid filters
- Extending metadata processing

#### Common Rake Workflow:
```bash
# 1. Add images to objects/ directory
# 2. Generate derivatives
rake generate_derivatives

# 3. For large collections, generate JSON
rake generate_json

# 4. Test site locally
bundle exec jekyll serve
```

### Troubleshooting Development Tools

#### Rake Task Issues:
- **Images not processing**: Check file permissions and ImageMagick installation
- **Large memory usage**: Process images in smaller batches
- **JSON generation fails**: Verify CSV metadata syntax

#### Plugin Issues:
- **Pages not generating**: Check `display_template` values and layout files
- **Liquid errors**: Verify helper function syntax in templates

## Summary

CB-Essay extends CollectionBuilder-CSV to support essay and monograph authoring alongside digital collections. This approach maintains flexibility while leveraging:

- **Essay System**: Sequential narrative chapters in `_essay/` with customizable themes
- **CollectionBuilder Infrastructure**: Robust search, browse, data management for collection items
- **Seamless Integration**: Embed collection items directly into essays using includes
- **Dual Navigation**: Essay prev/next buttons + standard collection browse/search
- **Responsive Design**: Bootstrap-based styling works across essays and collection pages
- **Configuration-Driven**: Customize via `theme.yml` and CSV config files without code changes

Work WITH the framework by extending layouts, using existing includes, and following CollectionBuilder patterns.