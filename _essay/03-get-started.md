---
title: Get Started with CB-Essay
order: 2
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

**That's it!** 

{% include essay/feature/aside.html
   text="**Bonus:** Use the **Project Gutenberg extractor** (Actions tab) to populate your `_essay/` folder with a complete book automatically!" %}

### Option B: GitHub.dev (VS Code in Browser)

Get [a full VS Code editor](https://docs.github.com/en/codespaces/the-githubdev-web-based-editor) without leaving your browser:

1. Go to your repository on GitHub
2. Press the `.` (period) key **OR** change the URL from `github.com` to `github.dev`
3. Edit files in a full-featured code editor
   - Replace the content in the `_essay` folder with your own
   - Edit the `_config.yml` file and the `_data/theme.yml` file to change the site's title, theme, featured image, and typography
4. Use [Source Control panel](https://docs.github.com/en/codespaces/the-githubdev-web-based-editor#commit-your-changes) (third option from the top on the far right) to stage and commit changes

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


## Step 3: Add Content (Two Options)

### Option A: Use the Gutenberg Extractor (Quickest!)

Want to start with a complete book? Extract one from Project Gutenberg:

1. Go to your repository's **Actions** tab
2. Click **"Extract Gutenberg Book"** workflow
3. Click **"Run workflow"**
4. Enter a book ID (e.g., `84` for Frankenstein, `1342` for Pride and Prejudice)
5. Click **"Run workflow"** button

Wait a minute - your `_essay/` folder will be populated with chapter files automatically! And your config files (`_config.yml` and `_data/theme.yml`) will be updated with the title, author, and cover image from Project Gutenberg.

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

When you're ready to publish your site, you have several options, as detailed here on our [CollectionBuilder's Deployment Documentation](https://collectionbuilder.github.io/cb-docs/docs/deploy/). You can build and publish these sites wherever you have access to a web server. 

### Set Up GitHub Pages with Jekyll Action

The most common way to publish these sites is using GitHub pages below. CB-Essay requires a GitHub Action to build properly. The action is already built in so you don't need to create one, but you should follow the steps below to enable GitHub to publish your site: 

1. Go to your repository and click the **Settings** menu item at the end of the second row on the page
2. Click on the **Pages** section on the left-hand side. 
2. Under **Source**, select **GitHub Actions**
3. GitHub will suggest the Jekyll workflow - ignore it! You've already got that file. 
4. Go to your readme.md file in the root of your repository. 
5. Make and commit a small change -- just add space! 
6. Once you commit the change, the site will properly rebuild!

That's it! Every time you commit changes from there on out, GitHub Actions will automatically build and deploy your site.

### View Your Live Site

After the GitHub Action completes (usually 2-3 minutes), visit:

```
https://YOUR-USERNAME.github.io/YOUR-REPO-NAME/
```

**Your essay is live!** 🎉

{% include essay/feature/aside.html text="**Tip:** Watch the Actions tab to see the build progress. A green checkmark means your site deployed successfully!" %}


## Next Steps

Now that your site is running, explore what you can do:
- **[Essay Features](04-essay-features.html)** - Learn all available features with copy-paste examples
- **[Collection Integration](05-collection-integration.html)** - Add collection items to your essays

Or dive into the [documentation](https://github.com/CollectionBuilder/cb-essay/tree/main/docs/cb-essay).

---

**You're ready to write!** The next essay will show you every available feature with working examples you can copy.
