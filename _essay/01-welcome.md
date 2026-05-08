---
title: Welcome to CB-Essay
order: 1
---

We've been encouraging users of CollectionBuilder to write *with* their collections since we first started promoting the framework in 2019, mainly through contextual pages like our About page. 

More recently, we worked with several [Center for Digital Inquiry and Learning (CDIL)](https://cdil.lib.uidaho.edu/) Graduate Student Fellows who wanted to flip things around so they could write essays with CollectionBuilder underneath.{% include essay/feature/aside.html text="See [Sedimentation](https://cdil.lib.uidaho.edu/sedimentation/), [Tender Spaces](https://cdil.lib.uidaho.edu/tender-spaces/), and [Fire Lines](https://cdil.lib.uidaho.edu/fire-lines/)" %} It's led to some great work, and we're excited to open up the framework we've built from those projects to more users. 

CB-Essay is  a publishing framework that lets you ***write with, on, and for*** the web{% include essay/feature/aside.html text="And if you prefer WYSIWYG editors, you can draft in Google Docs and export to Markdown!" %} while maintaining complete control over how your work appears online and in print.

For the past 10+ years, we've watched digital scholarship projects default to familiar word processors, even when publishing to the web. It makes sense—learning new tools takes time, and time is precious.{% include essay/feature/aside.html text="As my colleague Evan notes: Word is not easy! It's incredibly complicated!" %} But this compromise often means students aren't learning how to write on/with the web and potential web projects aren't being built.

CB-Essay offers a different path: write in Markdown, integrate primary sources and multimedia directly into your text, and publish sophisticated multimodal scholarship to both web and print formats.

The mini-essays below will introduce you to the system and get you started. 

## So What Is It?

***CB-Essay*** is a Jekyll-based framework that combines **long-form essay writing** with **digital collection features**. Built on [CollectionBuilder](https://collectionbuilder.github.io/), it enables you to create multimodal scholarly narratives, written in Markdown, that integrate primary sources, archival materials, and multimedia items directly into your texts.

## What Makes CB-Essay Different?

Traditional digital publishing tools treat essays and collections as separate entities. CB-Essay connects them, allowing you to:

- **Reference collection items** using simple includes
- Create **asides and margin notes** that link to primary sources {% include /essay/feature/aside.html text="Like this!" %}
- Build **interactive visualizations** from your metadata that help contextualize your work
- **Publish your work for free** on GitHub 
- Fashion the readers' experience through **scroll-based interactions and custom typography/fonts** {% include /essay/feature/aside.html text="Keep scrolling to see the next section magically appear!" %}"

{% include essay/new-section.html %}

## How It Works

CB-Essay operates on a **dual-collection model**:

1. **Essay Collection** - Your narrative content lives in `_essay/` as Markdown files
2. **Object Collection** - Primary sources and items defined in a CSV metadata file

CB-Essay allows you to write ***with*** your collection of sources, allowing you to integrate references, images, documents, recordings, and videos seamlessly into your writing and into the web. 

Just follow the plan as in the below image.{% include essay/feature/aside.html text="Below image credits: The Miriam and Ira D. Wallach Division of Art, Prints and Photographs: Photography Collection, The New York Public Library. 'Group farm plan writing meeting. Weld County, Colorado' The New York Public Library Digital Collections. [https://digitalcollections.nypl.org/items/1b0a3fc0-1d42-0139-bac7-0242ac110003](https://digitalcollections.nypl.org/items/1b0a3fc0-1d42-0139-bac7-0242ac110003)" %}

{% include feature/image.html objectid="/assets/img/writing-plan.jpg" caption="The tool is no more complicated than following this gentleman's instructions!" alt="Group working on a farm plan writing project with man pointing at a complex plan written on a large sheet of paper at the front"%}

## Key Features at a Glance

- Sequential **prev/next navigation**
- Flexible **essay or monograph** themes
- **Margin notes** with collection item integration
- **Blockquotes** with full attribution
- **Print & PDF output** with Paged.js (Letter, A4, or 6×9″ formats)
- **Image galleries** and **mini-maps**
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

Want to publish a public domain book? Use our [**GitHub Action**](https://dcnb.github.io/frankenstein/action.mp4) to extract any of **60,000+ books** from Project Gutenberg directly into your `_essay/` folder - pre-formatted for the site. 


## Next Steps

Check out some examples sites, then get started. The remaining essays show off CB-Essay in the wild, and then walk you through setting up your first site and understanding the features.

- **[See Examples](02-examples.html)** - See CB-Essay as used for DH projects and in demonstration 
- **[Get Started](03-get-started.html)** - Set up your first essay in 10 minutes
- **[Essay Features](04-essay-features.html)** - Learn and copy all available features
- **[Collection Integration](05-collection-integration.html)** - Blend essays with collection items

Or jump straight to the [documentation]({{ '/docs.html' | relative_url }}) for reference guides.

---


