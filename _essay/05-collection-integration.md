---
title: Collection Integration
order: 5
---

CB-Essay's real power emerges when you integrate collection items with your narrative. This essay explains the **dual-collection model** and shows you how to weave digital objects seamlessly into your writing using real examples from this site's demo collection.

---

## The Dual-Collection Model

CB-Essay manages two parallel collections that work together:

### 1. Essay Collection (`_essay/` folder)
- Your Markdown essay files
- Sequential navigation (prev/next buttons)
- Narrative content
- Controlled by `order` field in front matter

### 2. Object Collection (CSV metadata in `_data/`)
- Digital items: images, PDFs, audio, video
- Metadata-driven item pages
- Powers Browse, Map, Timeline, Search features
- Referenced in essays by `objectid`

**The magic:** Reference any collection item within your essays using its `objectid`.

---

## Understanding CollectionBuilder Metadata

Your collection items are defined in a CSV file. This demo uses `demo-compoundobjects-metadata.csv` in the `_data/` folder.

### Required Fields

**`objectid`**
- Unique identifier (lowercase, no spaces)
- Used in essay includes: `{% raw %}{% include essay/feature/aside.html objectid="demo_001" %}{% endraw %}`

**`title`**
- Item's name/description

{% include essay/feature/aside.html text="**Learn more:** See the [CB-CSV Metadata Guide](https://collectionbuilder.github.io/cb-docs/docs/metadata/csv_metadata/) for complete field documentation." %}

### Fields for Visualizations

Different CB features require specific metadata fields:

**For Maps:** `latitude`, `longitude`

**For Timeline:** `date` (at minimum: `yyyy` format)

**For Subjects Page:** `subject` (semicolon-separated values)

**For Locations Page:** `location` (semicolon-separated values)

### Display Template Field

The `display_template` field tells CB how to display each item:
- `image` - Photo or illustration
- `pdf` - PDF document
- `video` - Video file or YouTube/Vimeo
- `audio` - Audio recording
- `record` - Metadata-only record
- `compound_object` - Parent item with children

---

## Referencing Items in Essays

Once you have metadata, reference items using their `objectid`:

### Asides with Collection Items

Asides are the most common way to integrate collection items into essays. The aside include is incredibly flexible - let's explore what it can do:

#### Text-Only Aside (No Collection Item)

Here's a simple margin note.{% include essay/feature/aside.html text="This aside contains only text - useful for brief explanations, definitions, or commentary." %} The aside appears in the margin on desktop and inline on mobile.

**Copy this:**
```liquid
{% raw %}{% include essay/feature/aside.html
   text="Your margin note text here" %}{% endraw %}
```

---

#### Aside with Image Item

Moscow's Administration Building{% include essay/feature/aside.html objectid="demo_001" text="Built in 1909, this building still stands on the University of Idaho campus." %} was one of the first permanent structures on campus.

**Copy this:**
```liquid
{% raw %}{% include essay/feature/aside.html
   objectid="demo_001"
   text="Context about this item" %}{% endraw %}
```

The aside automatically shows the item's thumbnail and links to its full page.

---

#### Aside with PDF Item

Court records from Spokane{% include essay/feature/aside.html objectid="demo_002" text="Click to view the full PDF postcard" gallery="false" %} provide historical context for legal proceedings in the early 1900s.

**Copy this:**
```liquid
{% raw %}{% include essay/feature/aside.html
   objectid="demo_002"
   text="PDF description"
   gallery="false" %}{% endraw %}
```

Setting `gallery="false"` links directly to the item page instead of opening a viewer.

---

#### Aside with Audio Item

Psychiana radio broadcasts{% include essay/feature/aside.html objectid="demo_003" text="Listen to this excerpt from a 1947 radio program" %} reached audiences across America in the 1940s.

**Copy this:**
```liquid
{% raw %}{% include essay/feature/aside.html
   objectid="demo_003"
   text="Audio description" %}{% endraw %}
```

Audio and video items show an icon and open in a spotlight viewer when clicked.

---

#### Aside with Custom Caption

You can override the item's title:

The courthouse{% include essay/feature/aside.html objectid="demo_002" caption="Historic Spokane Courthouse" text="Custom caption replaces the default title" %} dominated Spokane's downtown.

**Copy this:**
```liquid
{% raw %}{% include essay/feature/aside.html
   objectid="demo_002"
   caption="Your custom caption"
   text="Additional context" %}{% endraw %}
```

---

#### Aside with Image Height Control

For taller images, control the display height:

Forest patrols{% include essay/feature/aside.html objectid="demo_031" height="300px" text="Increased height shows more detail" %} monitored Idaho's wilderness areas.

**Copy this:**
```liquid
{% raw %}{% include essay/feature/aside.html
   objectid="demo_031"
   height="300px"
   text="Description" %}{% endraw %}
```

Default height is `205px`. Adjust as needed for your images.

---

### CollectionBuilder Feature Includes

Beyond asides, you can use any standard CB feature include. See the [CB Features documentation](https://collectionbuilder.github.io/cb-docs/docs/features/) for complete details.

#### Card Include

Display an item as a card with image and metadata:

```liquid
{% raw %}{% include feature/card.html
   objectid="demo_001"
   width="50"
   centered=true %}{% endraw %}
```

#### Image Include

Show an item image with caption:

```liquid
{% raw %}{% include feature/image.html
   objectid="demo_031"
   width="75" %}{% endraw %}
```

#### Button Link to Item

Create a button linking to an item page:

```liquid
{% raw %}{% include feature/button.html
   text="View the Full Collection"
   link="/browse.html"
   color="primary" %}{% endraw %}
```

---

## Using CollectionBuilder Visualizations

Embed full CB visualizations directly in your essays:

### Timeline

```liquid
{% raw %}{% include feature/timelinejs.html %}{% endraw %}
```

Shows all items with dates on an interactive timeline. See the [Timeline documentation](https://collectionbuilder.github.io/cb-docs/docs/features/timeline/).

### Mini Map

Below is a mini map centered on Lake George in Indiana: 

{% include feature/mini-map.html latitude="41.75853633769425" longitude="-85.00736307963982" map-zoom="12" %}

```liquid
{% raw %}{% include feature/mini-map.html latitude="41.75853633769425" longitude="-85.00736307963982" map-zoom="12" %}{% endraw %}
```

Displays all items with latitude/longitude on an interactive map. See the [Map documentation](https://collectionbuilder.github.io/cb-docs/docs/features/map/).

### Subject Cloud

```liquid
{% raw %}{% include feature/cloud.html fields="subject" %}{% endraw %}
```

Visualizes subject keywords from your metadata. See the [Cloud documentation](https://collectionbuilder.github.io/cb-docs/docs/features/cloud/).

---

## Workflow: Building an Integrated Essay

### Step 1: Prepare Your Collection Metadata

Create or edit your CSV file in `_data/`:

```csv
objectid,title,creator,date,description,subject,latitude,longitude,format,filename
letter_001,Letter from Moscow,J. Smith,1890-05-15,Personal correspondence,letters;family,-116.991779,46.733001,image/jpeg,letter_001.jpg
photo_001,Campus View,University,1909,Administration Building,buildings;campus,-117.009633,46.725562,image/jpeg,photo_001.jpg
```

**Key points:**
- Use unique `objectid` values (no spaces!)
- Include fields needed for your planned features (dates for timeline, lat/long for maps)
- Use semicolons to separate multiple values (subjects, creators)

### Step 2: Configure Your Metadata File

In `_config.yml`, specify which CSV to use:

```yaml
metadata: your-metadata-filename
```

Omit the `.csv` extension.

### Step 3: Write Your Essay with Integrated Items

```markdown
## Historical Context

The university campus{% include essay/feature/aside.html
objectid="photo_001" text="View the historic administration building" %}
expanded rapidly during the early 1900s.

Personal letters{% include essay/feature/aside.html
objectid="letter_001" text="Read correspondence from residents" %}
reveal daily life in Moscow, Idaho.
```

### Step 4: Test Locally or Use GitHub.dev

- **GitHub.dev:** Press `.` in your repository for instant VS Code editor
- **Codespaces:** Get full preview with Jekyll
- **Local:** `bundle exec jekyll s` to preview

Verify all objectids resolve correctly and images display.

---

## Example: Compound Objects

The demo collection includes compound objects - parent items with multiple children. Example: `demo_008` (Hell's Half Acre lookout) has child items `demo_009`, `demo_010`, `demo_011`, `demo_012`.

### Referencing Parent Items

When you reference a parent objectid, CB automatically knows about its children:

{% include essay/feature/aside.html
   objectid="demo_009"
   caption="This lookout tower has multiple associated media files" %}

```liquid
{% raw %}{% include essay/feature/aside.html
   objectid="demo_008"
   text="This lookout tower has multiple associated media files" %}{% endraw %}
```

The item page will show all child items. See the [Compound Objects documentation](https://collectionbuilder.github.io/cb-docs/docs/objects/compound-objects/) for details.

---

## Collection Pages

Your collection items automatically generate these CB pages:

- **[Browse](/browse.html)** - Grid view of all items
- **[Map](/map.html)** - Items with lat/long displayed
- **[Timeline](/timeline.html)** - Items with dates shown chronologically
- **[Subjects](/subjects.html)** - Subject keyword cloud
- **[Locations](/locations.html)** - Location keyword cloud
- **[Data](/data.html)** - Download metadata

These work automatically from your CSV - no additional configuration needed!

---

## Project Gutenberg Integration

Want to publish an annotated edition of a public domain book?

### 1. Extract the Book

Use the **GitHub Action**:
1. **Actions** tab → **"Extract Gutenberg Book"**
2. Enter book ID (e.g., `84` for Frankenstein)
3. Run workflow

Chapters extract to `_essay/` automatically.

### 2. Add Collection Items

Create metadata for related materials:
- Historical maps
- Contemporary illustrations
- Manuscript images
- Critical sources

### 3. Annotate with Asides

Edit the extracted chapter files, adding your scholarly apparatus:

```markdown
## Letter 1

St. Petersburgh, Dec. 11th, 17—.

You will rejoice{% include essay/feature/aside.html objectid="map_arctic"
text="Walton's route followed known Arctic exploration paths" %} to hear that
no disaster has accompanied the commencement of an enterprise which you have
regarded with such evil forebodings.
```

See the [Gutenberg Extraction Guide](../docs/cb-essay/gutenberg-extraction.md) for complete workflow.

---

## Best Practices

### Metadata Quality
- Use **descriptive objectids** (`admin_building_1909` not `img001`)
- Write **complete titles** and descriptions
- **Tag thoroughly** with subjects for discoverability
- Include **dates** for timeline features
- Add **lat/long** for map features

### Essay-Collection Balance
- **Don't overwhelm** text with too many asides (3-5 per essay maximum)
- Use asides for **supplementary items**, not primary content
- Feature **key items** with full image includes or cards
- **Group related items** in galleries when appropriate

### Performance
- **Optimize images** (1200px max width for display)
- Use **external URLs** for very large media when possible
- **Test page load times** on slower connections
- Consider **compound objects** to organize related items

### Accessibility
- Provide **alt text** in metadata (`image_alt_text` field)
- Ensure **color contrast** meets WCAG AA standards
- **Test with screen readers** if possible
- Include **text alternatives** for visual content

---

## Troubleshooting

### Item not displaying

**Check:**
- `objectid` exists in metadata CSV (exact match, case-sensitive)
- Spelling and capitalization match exactly
- Metadata filename specified correctly in `_config.yml`
- CSV file is in `_data/` folder

### Image not loading

**Check:**
- `filename` or `object_location` field populated in metadata
- Image file exists in `objects/` folder or at external URL
- File format is supported (JPG, PNG, GIF, PDF, MP3, MP4)
- Paths are correct (case-sensitive on some systems)

### Aside shows wrong format

**Check:**
- `display_template` field is set correctly in metadata
- `format` field matches actual file type
- For images: `image_small` and `image_thumb` paths exist

---

## Next Steps

You now understand the complete CB-Essay ecosystem:

✅ Write essays in Markdown
✅ Use essay features (blockquotes, asides, maps)
✅ Integrate collection items seamlessly
✅ Leverage CB visualizations (timeline, map, subjects)
✅ Build rich, multimodal scholarship

### Keep Learning

- **[CB-CSV Documentation](https://collectionbuilder.github.io/cb-docs/)** - Complete CollectionBuilder reference
- **[Metadata Guide](https://collectionbuilder.github.io/cb-docs/docs/metadata/csv_metadata/)** - Detailed field specifications
- **[Features Documentation](https://collectionbuilder.github.io/cb-docs/docs/features/)** - All available includes
- **[Essay Writing Guide](../docs/cb-essay/essay-writing.md)** - CB-Essay specific workflow

### Get Help

- **[CB Discussion Forum](https://github.com/CollectionBuilder/collectionbuilder.github.io/discussions)** - Community support
- **[Open an issue](https://github.com/CollectionBuilder/cb-essay/issues)** - Report bugs or request features
- **[CollectionBuilder Community](https://collectionbuilder.github.io/community.html)** - Connect with other users

---

**You're ready to create remarkable digital scholarship!** Start building, and remember: copy any feature from these demo essays and adapt it for your own work.
