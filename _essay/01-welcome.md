---
title: Welcome to CB-Essay
order: 1
---

**Let's all stop writing digital scholarship pieces in Microsoft Word.** And let's start encouraging students writing for digital projects to do the same. 

So many times, during the 15 years I've been doing this, I've given up at the end of a project and allowed this to happen, capitulating to the dominant, bloated, ugly and overwrought writing technology of the time in order to *make it easy* for faculty or students who are ostensibly producing writing for projects that are meant for the web and meant to improve the digital literacy of those completing them. 

I think it's time we stopped doing that, and in order to make that easier, we are introducing here a tool that we hope helps us digital humanists truly ***write with, on, and for*** the web. 

## What Is It?

CB-Essay is a Jekyll-based framework that combines **long-form essay writing** with **digital collection features**. Built on CollectionBuilder, it enables you to create multimodal scholarly narratives, written in Markdown, that integrate primary sources, archival materials, and multimedia items directly into your texts.

## What Makes CB-Essay Different?

Traditional digital publishing tools treat essays and collections as separate entities. CB-Essay unifies them, allowing you to:

- Write in **simple Markdown** with specialized features for scholarly work
- **Reference collection items** using simple includes
- Create **asides and margin notes** that link to primary sources {% include /essay/feature/aside.html text="Like this!" %}
- Build **interactive visualizations** from your metadata
- **Publish your work for free** on GitHub 
- Fashion the readers' experience through **scroll-based interactions and custom typography/fonts** {% include /essay/feature/aside.html text="Keep scrolling to see the next section magically appear!" %}"

{% include essay/new-section.html %}

## How It Works

CB-Essay operates on a **dual-collection model**:

1. **Essay Collection** - Your narrative content lives in `_essay/` as Markdown files
2. **Object Collection** - Primary sources and items defined in a CSV metadata file

CB-Essay allows you to write ***with*** this collection of sources, allowing you to integrate your references, images, documents, recordings, and videos seamlessly into your writing and into the web. 

## Key Features at a Glance

- Sequential **prev/next navigation**
- Flexible **essay or monograph** themes
- Built-in **footnotes and citations** support
- **Margin notes** with collection item integration
- **Blockquotes** with full attribution
- **Image galleries** and **mini-maps** 
- Integration with **timelines** and **subject clouds**
- You can also **build your own features!** --> CB-Essay is all yours and totally customizable. 

### CollectionBuilder Features
- All **CollectionBuilder pages**: Browse, Map, Timeline, Subjects
- **Compound objects** support
- **Metadata-driven, SEO-enhanced** item pages  
- **Search and filtering**




## Who Should Use CB-Essay?

CB-Essay is ideal for anyone who wants to write ***write with, on, and for*** the web, including:

- **Digital humanists** creating annotated editions or critical apparatus
- **Historians** presenting narrative alongside primary sources
- **Educators** building interactive course readers
- **Archivists** creating context around collections
- **Writers** publishing long-form digital scholarship




## See Examples

CB-Essay powers a variety of digital humanities projects:

### Tender Spaces: Multimodal, Multilingual 5-Part Essay

{% include feature/image.html objectid="/assets/img/tender_spaces.png" alt="Tender Spaces screenshot" link="https://cdil.lib.uidaho.edu/tender-spaces/"%}

This extensively customized multimodal and multilinqual essay explores artist Gaëtane Buttigieg's life, art, and forced institutionalization in the 1970s through personal narratives and video interviews. This project demonstrates CB-Essay's flexibility for highly designed, custom presentations.

**View:** [cdil.lib.uidaho.edu/tender-spaces](https://cdil.lib.uidaho.edu/tender-spaces/)


### Frankenstein: Extracted Book from Project Gutenberg

{% include feature/image.html objectid="Frankenstein1910.jpg" alt="A still from the film Frankenstein (1910), showing Charles Stanton Ogle as the monster." link="https://dcnb.github.io/frankenstein/"%}

A digital edition of Mary Shelley's classic novel demonstrating the **monograph theme**. Features chapter-by-chapter navigation, integrated scholarly apparatus, and historical context from Project Gutenberg.

**View:** [dcnb.github.io/frankenstein](https://dcnb.github.io/frankenstein) 

### The Wreck of the Deutschland: Single-page, scrollytold poem

{% include feature/image.html objectid="/assets/img/deutschland.jpg" alt="Wreck of the Deutschland poem edition preview" link="https://dcnb.github.io/wreck-of-the-deutschland"%}

Gerard Manley Hopkins's poem presented in the **essay theme** with scrolling transitions and visual breaks. Shows how CB-Essay handles poetry and single-page essays with dramatic effect.

**View:** [dcnb.github.io/wreck-of-the-deutschland](https://dcnb.github.io/wreck-of-the-deutschland) 


### Bonus: Project Gutenberg Extractor

Want to publish a public domain book? Use our **GitHub Action** to extract any of **60,000+ books** from Project Gutenberg directly into your `_essay/` folder - pre-formatted and ready to publish. 


## Next Steps

Ready to get started? The remaining essays walk you through everything:

- **[Getting Started](02-getting-started.html)** - Set up your first essay in 10 minutes
- **[Essay Features](03-essay-features.html)** - Learn and copy all available features
- **[Collection Integration](04-collection-integration.html)** - Blend essays with collection items

Or jump straight to the [documentation](https://github.com/CollectionBuilder/cb-essay/tree/main/docs/cb-essay) for reference guides.

---


