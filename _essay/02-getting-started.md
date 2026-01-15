---
title: Getting Started with CB-Essay
order: 2
---

This guide walks you through creating your first CB-Essay project from scratch. You'll have a working essay site in about 10 minutes.

## Prerequisites

You'll need:

- A **GitHub account** (free)
- Basic **Markdown** knowledge (learn as you go)
- **Git** installed (for local development)
- **Ruby and Jekyll** (for local preview - optional but recommended)

Don't worry if this seems technical - we'll walk through each step.

## Step 1: Use This Template

CB-Essay is a GitHub template repository. This means you can create your own copy with one click:

1. Navigate to [github.com/CollectionBuilder/cb-essay](https://github.com/CollectionBuilder/cb-essay)
2. Click the green **"Use this template"** button
3. Name your repository (e.g., `my-essay-project`)
4. Choose **Public** or **Private**
5. Click **"Create repository"**

**That's it!** You now have your own CB-Essay repository.

{% include essay/feature/aside.html
   text="**Tip:** Use a descriptive repository name. It will become part of your site's URL: `username.github.io/repository-name`" %}

## Step 2: Choose Your Editing Workflow

You have several options for working with your essays. **Most CB-Essay users work directly on GitHub** without installing anything locally.

### Option A: Edit on GitHub.com (Easiest!)

Work entirely in your browser - **no local installation needed**:

1. Navigate to your repository on GitHub
2. Click into the `_essay/` folder
3. Click **"Add file"** → **"Create new file"**
4. Name it `my-first-essay.md`
5. Add your content (see Step 3 below)
6. Click **"Commit changes"**

**That's it!** GitHub Pages will automatically rebuild your site.

{% include essay/feature/aside.html
   text="**Bonus:** Use the **Project Gutenberg extractor** (Actions tab) to populate your `_essay/` folder with a complete book automatically!" %}

### Option B: GitHub.dev (VS Code in Browser)

Get a full VS Code editor without leaving your browser:

1. Go to your repository on GitHub
2. Press the `.` (period) key **OR** change the URL from `github.com` to `github.dev`
3. Edit files in a full-featured code editor
4. Use Source Control panel to commit changes

**Perfect for:** Multiple file edits, search/replace, file management

### Option C: GitHub Codespaces (Cloud Development)

Get a complete development environment in the cloud:

1. Click **Code** → **Codespaces** → **Create codespace**
2. Wait for environment to load (includes Jekyll!)
3. Edit files in VS Code interface
4. Preview with `bundle exec jekyll s`
5. Use terminal, extensions, and full IDE features

**Perfect for:** Testing features, previewing locally, advanced work

### Option D: Local Development (Advanced)

For local development with Git and Jekyll installed on your computer, follow the [CollectionBuilder-CSV walkthrough](https://collectionbuilder.github.io/cb-docs/docs/walkthroughs/csv-walkthrough/). CB-Essay uses the same setup process.

**Perfect for:** Offline work, full control, fastest preview cycle

{% include essay/feature/blockquote.html
   quote="Most CB-Essay users never install anything locally. The GitHub web interface and Gutenberg extractor provide everything needed to publish essays."
   align="center" %}

## Step 3: Add Content (Two Options)

### Option A: Use the Gutenberg Extractor (Quickest!)

Want to start with a complete book? Extract one from Project Gutenberg:

1. Go to your repository's **Actions** tab
2. Click **"Extract Gutenberg Book"** workflow
3. Click **"Run workflow"**
4. Enter a book ID (e.g., `84` for Frankenstein, `1342` for Pride and Prejudice)
5. Click **"Run workflow"** button

Wait a minute - your `_essay/` folder will be populated with chapter files automatically!

**Find books:** Browse [gutenberg.org](https://www.gutenberg.org/) and get the ID from the URL.

### Option B: Write Your Own Essay

No matter which editing method you chose in Step 2, essays use the same format.

Create a file in `_essay/` named `my-first-essay.md` with this content:

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
- As expected

### Subsections too

I can add blockquotes:

{% raw %}{% include essay/feature/blockquote.html
   quote="This is a quotation"
   speaker="Someone Important" %}{% endraw %}
```

Notice the **front matter** (between `---` lines):
- `title`: Your essay's title
- `order`: Controls navigation sequence (1, 2, 3...)

## Step 4: Customize Configuration

Edit two main configuration files:

### `_config.yml` - Site Settings

```yaml
title: "Your Essay Title"
author: "Your Name"
tagline: "A brief description"
description: "Longer description for search engines (160 chars)"
```

### `_data/theme.yml` - Appearance

```yaml
base-theme: essay  # or monograph for book-style

# Homepage image
image-style: full-image  # full-image, half-image, or no-image
featured-image: /assets/img/your-image.jpg

# Typography
base-font-size: 1.3em
base-font-family: Georgia
```

You can edit these files directly on GitHub or in any of the editors mentioned in Step 2.

## Step 5: Add More Essays

Create additional essay files in `_essay/`:

```
_essay/
├── 01-introduction.md   (order: 1)
├── 02-chapter-one.md    (order: 2)
└── 03-conclusion.md     (order: 3)
```

Essays will appear in navigation based on their `order` value, **not** the filename.

{% include essay/feature/aside.html
   text="**Pro tip:** Use order values like 10, 20, 30 instead of 1, 2, 3. This makes it easy to insert essays later without renumbering everything." %}

## Step 6: Deploy to GitHub Pages

When you're ready to publish your site:

### Set Up GitHub Pages with Jekyll Action

CB-Essay requires a GitHub Action to build properly. Follow the complete setup guide:

**[GitHub Pages Deployment Guide](https://collectionbuilder.github.io/cb-docs/docs/deploy/actions/)**

**Quick summary:**
1. Go to your repository **Settings** → **Pages**
2. Under **Source**, select **GitHub Actions**
3. GitHub will suggest the Jekyll workflow - click **Configure**
4. **Important:** Check the Ruby version in the workflow file
   - Look for `ruby-version:` (usually around line 35)
   - Change from `3.1` to `3.4` if needed
   - CB-Essay requires Ruby 3.4 or higher
5. Commit the workflow file (saves as `.github/workflows/jekyll.yml`)

That's it! Every time you commit changes, GitHub Actions will automatically build and deploy your site.

### Commit Your Changes

- **GitHub.com:** Changes are already committed when you click "Commit changes"
- **GitHub.dev / Codespaces:** Use the Source Control panel to commit and sync
- **Local development:** Run `git add .`, `git commit -m "Add essay"`, `git push`

### View Your Live Site

After the GitHub Action completes (usually 2-3 minutes), visit:

```
https://YOUR-USERNAME.github.io/YOUR-REPO-NAME/
```

**Your essay is live!** 🎉

{% include essay/feature/aside.html text="**Tip:** Watch the Actions tab to see the build progress. A green checkmark means your site deployed successfully!" %}

## Common First Steps

### Change Homepage Theme

Edit `_data/theme.yml`:

```yaml
# Essay theme - linear reading
base-theme: essay

# Monograph theme - table of contents on homepage
base-theme: monograph
```

### Add a Featured Image

1. Add your image to `assets/img/`
2. Update `_data/theme.yml`:

```yaml
featured-image: /assets/img/my-banner.jpg
```

### Adjust Typography

```yaml
base-font-size: 1.4em  # Larger text
base-font-family: Georgia  # Serif font for traditional feel
text-color: "#191919"
link-color: "#0d6efd"
```

## Workflow Tips

### GitHub.com Workflow (Most Common)

1. Navigate to `_essay/` folder
2. Edit existing file or create new one
3. Make your changes
4. Commit directly to main branch
5. Wait 2-5 minutes for GitHub Pages to rebuild
6. Visit your site URL to see changes

**That's it!** No git commands needed.

### GitHub.dev / Codespaces Workflow

1. Edit multiple files as needed
2. Open Source Control panel (git icon)
3. Review changes
4. Write commit message
5. Click ✓ to commit
6. Click sync/push button
7. GitHub Pages rebuilds automatically

### Local Development Workflow

See the [CollectionBuilder-CSV walkthrough](https://collectionbuilder.github.io/cb-docs/docs/walkthroughs/csv-walkthrough/) for complete local setup instructions.

### File Organization

Keep your project organized:

```
your-project/
├── _essay/           # Your essay content (Markdown)
├── _data/            # Metadata CSV for collection items
├── assets/
│   └── img/          # Your images
├── _config.yml       # Site configuration
└── _data/theme.yml   # Theme settings
```

## Troubleshooting

### Essay doesn't appear on site

- Check front matter has `title` and `order`
- Verify file is in `_essay/` directory
- Check for YAML syntax errors

### Changes not showing

- **Local:** Wait for Jekyll to rebuild (watch terminal)
- **GitHub Pages:** Wait 2-5 minutes after pushing
- Try hard refresh: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)

### Navigation broken

- Ensure essays have sequential `order` values
- Check no duplicate order numbers
- Verify front matter is valid YAML

## Next Steps

Now that your site is running, explore what you can do:

- **[Essay Features](03-essay-features.html)** - Learn all available features with copy-paste examples
- **[Collection Integration](04-collection-integration.html)** - Add collection items to your essays

Or dive into the [documentation](https://github.com/CollectionBuilder/cb-essay/tree/main/docs/cb-essay):
- [Essay Writing Guide](../docs/cb-essay/essay-writing.md) - Detailed reference
- [Theme Options](../docs/cb-essay/theme-options.md) - Customization options
- [Essay Features Reference](../docs/cb-essay/essay-features.md) - Complete feature list

---

**You're ready to write!** The next essay will show you every available feature with working examples you can copy.
