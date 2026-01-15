---
title: Welcome to CB-Essay
order: 1
---

CB-Essay is a Jekyll-based framework that combines **long-form essay writing** with **digital collection features**. Built on CollectionBuilder, it enables you to create multimodal scholarly narratives that seamlessly integrate primary sources, archival materials, and multimedia items directly into your writing.

## What Makes CB-Essay Different?

Traditional digital publishing tools treat essays and collections as separate entities. CB-Essay unifies them, allowing you to:

- Write in **simple Markdown** with specialized features for scholarly work
- **Reference collection items** using simple includes
- Create **asides and margin notes** that link to primary sources
- Build **interactive timelines, maps, and visualizations** from your metadata
- Publish beautiful, accessible sites with **zero JavaScript complexity**

{% include essay/feature/blockquote.html
   quote="CB-Essay bridges the gap between narrative scholarship and archival presentation, enabling truly multimodal digital humanities work."
   size="lg"
   align="center" %}

## How It Works

CB-Essay operates on a **dual-collection model**:

1. **Essay Collection** - Your narrative content lives in `_essay/` as Markdown files
2. **Object Collection** - Primary sources and items defined in a CSV metadata file

The magic happens when you combine them using specialized includes.

## See Examples


### Frankenstein; Or, The Modern Prometheus

{% include feature/image.html objectid="assets/img/FrankensteinDraft.jpg" alt="Frankenstein edition preview" link="https://dcnb.github.io/frankenstein/"%}

A digital edition of Mary Shelley's classic novel demonstrating the **monograph theme**. Features chapter-by-chapter navigation, integrated scholarly apparatus, and historical context from Project Gutenberg.

**View:** [dcnb.github.io/frankenstein](https://dcnb.github.io/frankenstein) *(coming soon)*

### The Wreck of the Deutschland

{% include feature/image.html objectid="/assets/img/deutschland.jpg" alt="Wreck of the Deutschland poem edition preview" link="https://dcnb.github.io/wreck-of-the-deutschland"%}

Gerard Manley Hopkins's poem presented in the **essay theme** with scrolling transitions and visual breaks. Shows how CB-Essay handles poetry and single-page essays with dramatic effect.

**View:** [dcnb.github.io/wreck-of-the-deutschland](https://dcnb.github.io/wreck-of-the-deutschland) 

CB-Essay powers a variety of digital humanities projects:

### Tender Spaces: Intimacy in Queer Idaho

{% include feature/image.html objectid="/assets/img/tender_spaces.png" alt="Tender Spaces screenshot" link="https://cdil.lib.uidaho.edu/tender-spaces/"%}


An extensively customized multimodal essay exploring queer intimacy in Idaho through personal narratives and archival materials. This project demonstrates CB-Essay's flexibility for highly designed, custom presentations.

**View:** [cdil.lib.uidaho.edu/tender-spaces](https://cdil.lib.uidaho.edu/tender-spaces/)

## Key Features at a Glance

### For Writers
- **Markdown-first** authoring
- Sequential **prev/next navigation**
- Flexible **essay or monograph** themes
- Built-in **footnotes and citations** support

### For Scholars
- **Margin notes** with collection item integration
- **Blockquotes** with full attribution
- **Image galleries** and **mini-maps**
- Integration with **timelines** and **subject clouds**

### For Collections
- All **CollectionBuilder features**: Browse, Map, Timeline, Subjects
- **Compound objects** support
- **Metadata-driven** item pages
- **Search and filtering**

### Bonus: Project Gutenberg Extractor

Want to publish a public domain book? Use our **GitHub Action** to extract any of **60,000+ books** from Project Gutenberg directly into your `_essay/` folder - pre-formatted and ready to publish.

## Who Should Use CB-Essay?

CB-Essay is ideal for:

- **Digital humanists** creating annotated editions or critical apparatus
- **Historians** presenting narrative alongside primary sources
- **Educators** building interactive course readers
- **Archivists** creating context around collections
- **Writers** publishing long-form digital scholarship

## Philosophy: Copy and Replace

This demo site is designed to teach through demonstration. Every feature you see can be **copied directly into your own essays**. See a blockquote you like? Copy the code, replace the content with yours. Find a useful margin note? Same approach.

**You don't need to understand the technical details** - just copy what works and replace the content.

## Next Steps

Ready to get started? The remaining essays walk you through everything:

- **[Getting Started](02-getting-started.html)** - Set up your first essay in 10 minutes
- **[Essay Features](03-essay-features.html)** - Learn and copy all available features
- **[Collection Integration](04-collection-integration.html)** - Blend essays with collection items

Or jump straight to the [documentation](https://github.com/CollectionBuilder/cb-essay/tree/main/docs/cb-essay) for reference guides.

---

**Let's create something remarkable together.** The next essay will get you writing your first CB-Essay in minutes.
