---
title: Collection Integration
order: 4
---

CB-Essay's real power emerges when you integrate collection items with your narrative. This essay shows you how the **dual-collection model** works and how to weave primary sources seamlessly into your writing.

## The Dual-Collection Model

CB-Essay manages two parallel collections:

**1. Essay Collection** (`_essay/` folder)
- Your Markdown essay files
- Sequential navigation
- Narrative content

**2. Object Collection** (CSV metadata)
- Collection items (images, documents, media)
- Metadata-driven
- Browse, map, timeline pages

These collections work together to create rich, multimodal scholarship.

## How Collection Metadata Works

Your collection items are defined in a CSV file in `_data/`. The default is `demo-compoundobjects-metadata.csv`, but you can use any CSV.

### Essential Metadata Fields

```csv
objectid,title,format,filename,description
demo_001,Historic Manuscript,image/jpeg,demo_001.jpg,A 19th century manuscript
demo_002,Audio Recording,audio/mp3,demo_002.mp3,Oral history interview
demo_003,Research Document,application/pdf,demo_003.pdf,Survey results
```

**Required fields:**
- `objectid` - Unique identifier (no spaces, use underscores)
- `title` - Item title
- `format` - MIME type (image/jpeg, application/pdf, etc.)

**Recommended fields:**
- `filename` - File in `objects/` folder
- `description` - Item description
- `date` - For timeline features
- `latitude`/`longitude` - For map features
- `subject` - For subject clouds and filtering

{% include essay/feature/aside.html text="See the [CollectionBuilder Metadata Guide](../docs/metadata.md) for complete field documentation." %}

### Configuring Your Metadata

In `_config.yml`, specify which CSV file to use:

```yaml
metadata: your-metadata-filename
```

Omit the `.csv` extension. The file must be in `_data/`.

## Referencing Items in Essays

Once your metadata is set up, reference items using their `objectid`:

### In Asides

{% include essay/feature/aside.html
   objectid="demo_001"
   text="This manuscript demonstrates early annotation practices" %}

The aside automatically pulls the item's thumbnail, title, and creates a link.

### In Item Cards

```liquid
{% raw %}{% include feature/card.html
   objectid="demo_001"
   width="50"
   centered=true %}{% endraw %}
```

Item cards display larger previews with full metadata.

### In Galleries

```liquid
{% raw %}{% include essay/feature/image-gallery.html
   objectid="demo_001;demo_005;demo_012" %}{% endraw %}
```

Galleries let you show multiple related items together.

## Embedding Media Types

CB-Essay handles different media types automatically:

### Images

```liquid
{% raw %}{% include feature/image.html
   objectid="demo_012"
   width="75" %}{% endraw %}
```

Images display with captions pulled from metadata.

### PDFs

For PDFs, asides show an icon and link:

```liquid
{% raw %}{% include essay/feature/aside.html
   objectid="document_001"
   text="Read the full survey report" %}{% endraw %}
```

### Video and Audio

Media items can open in a spotlight viewer:

```liquid
{% raw %}{% include essay/feature/aside.html
   objectid="interview_001"
   text="Listen to the oral history interview"
   gallery="true" %}{% endraw %}
```

## Advanced Integration

### Using Collection Features

Embed CollectionBuilder visualizations directly in essays:

**Full Timeline:**
```liquid
{% raw %}{% include feature/timeline.html %}{% endraw %}
```

**Subject Cloud:**
```liquid
{% raw %}{% include feature/cloud.html fields="subject" %}{% endraw %}
```

**Location Map:**
```liquid
{% raw %}{% include feature/map.html %}{% endraw %}
```

### Filtering Items

Show only specific items in visualizations:

```liquid
{% raw %}{% include feature/timeline.html filters="subject:manuscripts" %}{% endraw %}
```

### Compound Objects

CB-Essay supports compound objects (items with multiple files):

```csv
objectid,parentid,title
parent_001,,Collection of Letters
child_001,parent_001,Letter 1
child_002,parent_001,Letter 2
```

Reference the parent, and children are accessible automatically.

## Workflow: Building an Integrated Essay

### 1. Gather Your Sources

Collect your primary sources:
- Images → `objects/`
- PDFs → `objects/`
- Media files → `objects/` or external URLs

### 2. Create Metadata

Build your CSV in `_data/`:

```csv
objectid,filename,title,creator,date,description,subject
letter_1875,letter01.jpg,Letter to Margaret,R. Walton,1875-12-11,Letter from St. Petersburgh,correspondence
manuscript_draft,draft.jpg,Draft Manuscript,M.W. Shelley,1816,Original draft pages,manuscripts
```

### 3. Write Your Essay

Draft in Markdown, using objectids for references:

```markdown
## Chapter 1

Walton's letters{% include essay/feature/aside.html objectid="letter_1875" %}
document his journey north...

{% include essay/feature/blockquote.html
   quote="I feel a cold northern breeze..."
   source="Letter 1" %}

The manuscript reveals{% include essay/feature/aside.html objectid="manuscript_draft"
text="Notice the crossed-out passages" %} Shelley's revision process.
```

### 4. Test and Refine

- Preview locally: `bundle exec jekyll s`
- Check all objectids resolve correctly
- Verify images load
- Test navigation and links

## Example Use Cases

### Annotated Edition

Create a scholarly edition with integrated apparatus:

**Main text** → Essay content
**Footnotes** → Margin asides with references
**Images** → Manuscript pages as item figures
**Commentary** → Blockquotes with scholarly interpretation

### Digital Exhibit

Combine narrative with archival materials:

**Story** → Essay collection
**Objects** → Photographs, documents, artifacts
**Context** → Maps showing locations
**Timeline** → Chronological visualization

### Course Reader

Build interactive course materials:

**Readings** → Essay content
**Primary sources** → Collection items
**Discussion prompts** → Blockquotes
**Resources** → Links in asides

## Collection Pages

Don't forget - your collection items also generate standard CB pages:

- **Browse:** `/browse.html` - Grid view of all items
- **Map:** `/map.html` - Items with lat/long displayed
- **Timeline:** `/timeline.html` - Items with dates
- **Subjects:** `/subjects.html` - Subject cloud
- **Data:** `/data.html` - Download metadata as JSON/CSV

These pages work automatically from your metadata!

## Bonus: Project Gutenberg Integration

Want to publish a public domain book with integrated annotations?

### 1. Extract the Book

Use the GitHub Action:
1. Go to **Actions** → **"Extract Gutenberg Book"**
2. Enter book ID (e.g., `84` for Frankenstein)
3. Run workflow

The book extracts to `_essay/` as chapter files.

### 2. Add Your Annotations

Edit the generated files, adding your scholarly apparatus:

```markdown
---
title: Letter 1
order: 1
---

## Letter 1

*To Mrs. Saville, England.*

St. Petersburgh, Dec. 11th, 17—.

You will rejoice to hear{% include essay/feature/aside.html
text="The letters frame the narrative, providing distance and credibility" %}
that no disaster has accompanied...

{% include essay/feature/blockquote.html
   quote="This narrative structure creates a 'Chinese box' effect"
   speaker="Anne K. Mellor"
   source="Mary Shelley: Her Life, Her Fiction, Her Monsters" %}
```

### 3. Add Collection Items

Create metadata for relevant materials:
- Historical maps of Arctic exploration
- Contemporary illustrations
- Related manuscripts
- Critical sources

Reference them in your annotations using asides and item cards.

## Best Practices

### Metadata Quality
- Use descriptive, unique objectids
- Write clear, complete titles
- Provide thorough descriptions
- Tag with relevant subjects
- Include dates for timeline features

### Essay-Collection Balance
- Don't overwhelm text with items
- Use asides for supplementary items
- Feature key items as figures or cards
- Group related items in galleries

### Performance
- Optimize images (max 1200px width for display)
- Use external URLs for large media when possible
- Test page load times
- Consider lazy loading for image-heavy essays

### Accessibility
- Provide alt text in metadata descriptions
- Ensure sufficient color contrast
- Test with screen readers
- Include text alternatives for visual content

## Troubleshooting

### Item not displaying

**Check:**
- Objectid exists in metadata CSV
- Spelling/capitalization matches exactly
- Metadata file specified in `_config.yml`
- File exists in `objects/` folder (if using filenames)

### Image not loading

**Check:**
- Filename in metadata matches actual file
- Image is in `objects/` folder
- File format supported (JPG, PNG, GIF)
- Path is correct (case-sensitive on some systems)

### Aside shows wrong item

- Verify objectid in include matches metadata
- Check for duplicate objectids in CSV
- Clear Jekyll cache: `bundle exec jekyll clean`

## Next Steps

You now understand the complete CB-Essay system! You can:

✅ Write essays in Markdown
✅ Use specialized features (blockquotes, asides, maps)
✅ Integrate collection items
✅ Build rich, multimodal scholarship

### Keep Exploring

- Browse the [full documentation](../docs/cb-essay/)
- Explore [CollectionBuilder features](../docs/)
- Check the [GitHub repository](https://github.com/CollectionBuilder/cb-essay)
- See example projects in [Essay 1](01-welcome.html#real-world-examples)

### Get Help

- [Open an issue](https://github.com/CollectionBuilder/cb-essay/issues) on GitHub
- Join the [CollectionBuilder community](https://collectionbuilder.github.io/community.html)
- Read the [CollectionBuilder documentation](https://collectionbuilder.github.io/cb-docs/)

---

**You're ready to create remarkable digital scholarship.** Start building, and remember: every feature in these demo essays can be copied and adapted for your own work. Good luck!
