---
title: Get Started with CB-Essay
order: 20
part: Documentation
---

This guide walks you through creating your first CB-Essay project from scratch. You'll have a working essay site in about 10 minutes.

## Philosophy: Copy and Replace

This entire demo site is designed to teach through demonstration. Every feature you see can be **copied directly into your own essays**. See a blockquote you like? Copy the code, replace the content with yours. Find a useful margin note? Same approach.

**You don't need to understand the technical details** - just copy what works and replace the content.

## Prerequisites

You'll need:

- A **GitHub account** (free) -- [Sign up now!](https://www.github.com/)
- A willingness to learn


## Step 1: Use This Template

CB-Essay is a GitHub template repository. This means you can create your own copy with one click:

1. Navigate to [github.com/CollectionBuilder/cb-essay](https://github.com/CollectionBuilder/cb-essay)
2. Click the green **"Use this template"** button
3. Name your repository (e.g., `my-essay-project`){% include essay/feature/aside.html
   text="**Tip:** Use a descriptive repository name. It will become part of your site's URL: `username.github.io/repository-name`" %}
4. Choose **Public** or **Private** (If you'd like to publish the site on GitHub's free GitHub Pages web hosting, it will need to be Public)
5. Click **"Create repository"**

**That's it!** You now have your own CB-Essay repository.

## Step 2: Choose Your Editing Workflow

You have several options for working with your essays. **Most CB-Essay users work directly on GitHub** without installing anything locally.

### Option A: Edit on GitHub.com (Easiest!)

Work entirely in your browser - **no local installation needed**:

1. Navigate to your repository on GitHub
2. Click into the `_essay/` folder
3. Open `01-welcome.md`  and replace it's content with your own!
4. Do the same with the other `.md` files in the folder, renaming the filenames and replacing the "frontmatter" {% include /essay/feature/aside.html text="**Frontmatter** is the information at the top of each `.md` file that includes information like `title` and `order`; it's separated by `---` lines at the top and bottom." %} with your own info.  
   - See Step 3 below for more information on how to edit these files.
5. Edit the `_config.yml` file and the `_data/theme.yml` file to change the site's title, theme, featured image, and typography
6. Click **"Commit changes"**

### More Development Options 

{% capture option_b %}
Get [a full VS Code editor](https://docs.github.com/en/codespaces/the-githubdev-web-based-editor) without leaving your browser:

1. Go to your repository on GitHub
2. Press the `.` (period) key **OR** change the URL from `github.com` to `github.dev`
3. Edit files in a full-featured code editor
   - Replace the content in the `_essay` folder with your own
   - Edit the `_config.yml` file and the `_data/theme.yml` file to change the site's title, theme, featured image, and typography
4. Use [Source Control panel](https://docs.github.com/en/codespaces/the-githubdev-web-based-editor#commit-your-changes) (third option from the top on the far left) to stage and commit changes

**Good for:** Multiple file edits, search/replace, file management

{% endcapture %}
{% capture option_c %}
Get a complete development environment in the cloud:

1. Click **Code** → **Codespaces** → **Create codespace**
2. Wait for environment to load (includes Jekyll!)
3. Edit files in VS Code interface
4. Preview with `bundle exec jekyll s`
5. Use terminal, extensions, and full IDE features

**Good for:** Testing features, previewing locally, advanced work

{% endcapture %}
{% capture option_d %}
For local development with Git and Jekyll installed on your computer, follow the [CollectionBuilder-CSV walkthrough](https://collectionbuilder.github.io/cb-docs/docs/walkthroughs/csv-walkthrough/). CB-Essay uses the same setup process.

**Good for:** Offline work, full control, fastest preview cycle
{% endcapture %}

{% include feature/accordion.html  title1="Option B: GitHub.dev (VS Code in Browser)" text1=option_b title2="Option C: GitHub Codespaces (Cloud Development)" text2=option_c title3="Option D: Local Development (Advanced)" text3=option_d %}


## Step 3: Create Your First Essay

Now that you've chosen your workflow, let's add your content. Create a file in `_essay/` named `my-first-essay.md` with this content:

```yaml
---
title: My First Essay
order: 1
---

## Introduction

This is my first essay using CB-Essay. I can write in **Markdown** with _formatting_.

Here's a paragraph with a [link](https://example.com).

## Another Section

- Bullet points work
- As expected{% include essay/feature/aside.html text="So do asides!"%}

### Subsections too

I can add blockquotes:

{% raw %}{% include essay/feature/blockquote.html
   quote="This is a quotation"
   speaker="Someone Important" %}{% endraw %}
```

Notice the **front matter** (between `---` lines):
- `title`: Your essay's title
- `order`: Controls navigation sequence (1, 2, 3...)

### Quick Option: Project Gutenberg

Want to start with a complete book? Extract one from Project Gutenberg:

1. Enable [GitHub Pages]({{ 'docs.html#2-enable-github-pages' | relative_url }})
1. Go to your repository's **Actions** tab
2. Click **"Extract Gutenberg Book"** workflow
3. Click **"Run workflow"** and enter a book ID (e.g., `84` for Frankenstein)

Your `_essay/` folder will be populated with chapter files automatically. Find books at [gutenberg.org](https://www.gutenberg.org/).

## Step 4: Customize Configuration

Edit two main configuration files:

### `_config.yml` - Site Settings

These settings control what appears on your homepage cover page:

```yaml
title: "Your Essay Title"
author: "Your Name"  # Displays as "by Your Name" on cover page
tagline: "A brief description"  # Only shows if author is empty
description: "Longer description for search engines (160 chars)"
```

**Cover Page Display:**
- **title**: Your main title (always displays)
- **author**: Shows as "by [Author Name]" beneath the title
  - If you provide an author, it displays *instead of* the tagline
  - You can use HTML for multiple lines: `author: "Author Name<br>Edited by Editor Name"`
- **tagline**: Only displays if author field is empty
  - Use for subtitle or project description
  - Can also use HTML: `tagline: "A Digital Edition<br>Published 2024"`

### `_data/theme.yml` - Appearance

```yaml
# Navigation & Homepage
show-contents-nav: false  # true: navbar shows "Contents" button + chapter panel
show-homepage-toc: false  # true: homepage displays chapter table of contents
show-section-nav: false   # true: floating H2 sidebar on essay pages (wide screens)

# Homepage image
image-style: full-image  # full-image, half-image, or no-image
featured-image: /assets/img/your-image.jpg

# Color theme
color-theme: aldine  # default, idaho, lyre, nonesuch, aldine, doves, kelmscott, gregynog, ashendene

# Typography
base-font-size: 1.2em
base-font-family: theme       # theme (auto-matched) | Georgia | custom Google Font
display-font-family: theme    # theme | Georgia | custom
```

**Color themes:** Choose from 8 built-in accessible themes inspired by historical printing, or use `custom` with your own hex color.

**Fonts:** Set to `theme` for automatic pairing with your color theme, `Georgia` for offline use, or provide a custom Google Font with `font-cdn`.

You can edit these files directly on GitHub or in any of the editors mentioned in Step 2.

## Step 5: Add More Essays

Create additional essay files in `_essay/`:

```
_essay/
├── 01-introduction.md   (order: 1)
├── 02-chapter-one.md    (order: 2)
└── 03-conclusion.md     (order: 3)
```

Essays will appear in navigation based on their `order` value, **not** the filename.{% include essay/feature/aside.html text="**Pro tip:** Use order values like 10, 20, 30 instead of 1, 2, 3. This makes it easy to insert essays later without renumbering everything." %}

## Step 6: Configure Print/PDF Output (Optional)

CB-Essay includes sophisticated print and PDF generation using Paged.js. Configure it in `_data/theme.yml`:

```yaml
print:
  author: "Your Name"           # Author shown on cover and in PDF metadata
  institution: "Your Org"        # Institution on cover page
  cover-subtitle: ""             # Optional subtitle for book cover
  show-individual: true          # Show individual essay print cards
  show-book: true                # Show book builder
  aside-style: margin            # margin or inline
```

**Aside styles:**
- `margin`: Margin notes float into page gutter (requires wider right margin)
- `inline`: Margin notes appear as indented callout blocks

Once configured, access the **Print Hub** at `/print/` to:
- Print individual essays in Letter, A4, or 6×9″ formats
- Build custom PDF books by selecting specific essays
- Generate print-ready PDFs directly from your browser{% include essay/feature/aside.html text="**Tip:** The Print Hub is automatically added to your site navigation via `_data/config-nav.csv`" %}

## Step 7: Deploy to GitHub Pages

When you're ready to publish, set up GitHub Pages:

1. Go to your repository → **Settings** → **Pages**
2. Under **Source**, select **GitHub Actions**
3. Click **Configure** on the Jekyll workflow
4. Change `ruby-version: '3.1'` to `'3.4'` (line 40)
5. Click **Commit changes**

After 2-3 minutes, visit `https://YOUR-USERNAME.github.io/YOUR-REPO-NAME/`

**Your essay is live!** 🎉

For other deployment options, see [CollectionBuilder's Deployment Documentation](https://collectionbuilder.github.io/cb-docs/docs/deploy/).


## Next Steps

Now that your site is running, explore what you can do:
- **[Essay Features](04-essay-features.html)** - Learn all available features with copy-paste examples
- **[Collection Integration](05-collection-integration.html)** - Add collection items to your essays

Or dive into the [documentation]({{ '/docs.html' | relative_url }}).

---

**You're ready to write!** The next essay will show you every available feature with working examples you can copy.
