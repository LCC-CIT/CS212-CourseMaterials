# CS212-CourseMaterials
Course materials for AI Programming 1, CS 212, by <a href="https://profbird.dev" target="_blank">Brian Bird</a> at <a href="https://lanecc.edu" target="_blank">Lane Community College</a>.

Example code for this course: <a href="https://github.com/LCC-CIT/CS212-Examples/tree/main" target="_blank">LCC-CIT/CS212-Examples</a>

Course home page: <a href="https://lcc-cit.github.io/CS212-CourseMaterials/" target="_blank">https://lcc-cit.github.io/CS212-CourseMaterials</a>

## How the Site Is Built

The site is published with GitHub Pages from the `docs/` folder. GitHub builds it with Jekyll (`jekyll-theme-primer`, kramdown) when the repo is pushed to `main`, so the HTML files are generated from the `.md` files and do not appear in the repo. Relative links between `.md` files are converted to `.html` links automatically.

Customizations:

| File | What it does |
|---|---|
| `docs/_config.yml` | Site title and description, the theme, kramdown settings, and `breadcrumb_names` (labels for folder names in the breadcrumb trail, each optionally with a `url` to make it a link). |
| `docs/_layouts/default.html` | Copy of the theme's page layout. Replaces the theme's site-title link at the top of each page with a breadcrumb trail built from the page's URL: Home › folder › page title. The last item is the `breadcrumb` front matter value if a page has one, otherwise its `title`. |
| `docs/_includes/head-custom.html` | Added to the `<head>` of every page. Provides the `[TOC]` table of contents script, icons for external and download links, and Mermaid diagram rendering. |
| `.github/workflows/link-check.yaml` | Builds `docs/` and checks every link with [lychee](https://lychee.cli.rs/). Settings are in `lychee.toml` and `.lycheeignore`. |

The home page, `docs/index.html`, is plain HTML with no front matter, so it does not use the layout or the breadcrumb.
