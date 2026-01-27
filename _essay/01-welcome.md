---
title: Welcome to CB-Essay
order: 1
---

**Let's all stop writing digital scholarship pieces in Microsoft Word.** And let's start encouraging students writing for digital projects to do the same. 

So many times, during the 15 years I've been doing this, I've given up at the end of a project and allowed this to happen, capitulating to the dominant, bloated, ugly and overwrought writing technology of the time in order to *make it easy* for faculty or students who are ostensibly producing writing for projects that are meant for the web and meant to improve the digital literacy of those completing them. 

I think it's time we stopped doing that, and in order to make that easier, we made a tool that helps one to truly ***write with, on, and for*** the web. 

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

CB-Essay allows you to write ***with*** this collection of sources, allowing you to integrate your references, images, documents, recordings, and videos seamlessly into your writing and into the web. Just follow the plan as in the below image. 

{% include essay/feature/aside.html text="Below image credits: The Miriam and Ira D. Wallach Division of Art, Prints and Photographs: Photography Collection, The New York Public Library. 'Group farm plan writing meeting. Weld County, Colorado' The New York Public Library Digital Collections. [https://digitalcollections.nypl.org/items/1b0a3fc0-1d42-0139-bac7-0242ac110003](https://digitalcollections.nypl.org/items/1b0a3fc0-1d42-0139-bac7-0242ac110003)" %}
{% include feature/image.html objectid="/assets/img/writing-plan.jpg" caption="The tool is no more complicated than following this gentleman's instructions!" alt="Group working on a farm plan writing project with man pointing at a complex plan written on a large sheet of paper at the front"%}

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



### Bonus: Project Gutenberg Extractor

Want to publish a public domain book? Use our [**GitHub Action**](https://dcnb.github.io/frankenstein/action.mp4) to extract any of **60,000+ books** from Project Gutenberg directly into your `_essay/` folder - pre-formatted and ready to publish. 


## Next Steps

Check out some examples sites, then get started. The remaining essays show off CB-Essay in the wild, and then walk you through setting up your first site and understanding the features.

- **[See Examples](02-examples.html)** - See CB-Essay as used for DH projects and in demonstration 
- **[Get Started](03-get-started.html)** - Set up your first essay in 10 minutes
- **[Essay Features](04-essay-features.html)** - Learn and copy all available features
- **[Collection Integration](05-collection-integration.html)** - Blend essays with collection items

Or jump straight to the [documentation]({{ '/docs.html' | relative_url }}) for reference guides.

---


