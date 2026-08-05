<!--
Guidance for AI coding agents working on the CS212-CourseMaterials repository.
Keep this concise and focused on observable, repo-specific patterns and workflows.
-->

# Copilot instructions for CS212-CourseMaterials

Short summary (what this repo is): Course materials for an Intro to AI class — mostly static web content, lecture notes, labs and Jupyter notebooks. Primary artifacts are static HTML/Markdown pages, images, and notebooks organized for publication (GitHub Pages). The repo is authored and maintained by the course instructor.

What an agent should know to be useful
- Primary content lives under these paths:
  - `index.html` — course landing page (example of site layout and navigation).
  - `LectureNotes/` — lecture HTML/MD pages; follow naming pattern `CS123-TopicXX-...`.
  - `Labs/` — lab folders containing example solutions in multiple languages (Python, JS, C#).
  - `JupyterNotebooks/` — interactive examples and exercises (`.ipynb`).
  - `Images/` — course images and assets referenced from pages.

- Site is static HTML that appears intended for GitHub Pages. Do not add server-side frameworks or change the publishing model unless the change is explicit.

Conventions and patterns to follow
- Keep changes minimal and content-focused. Most files are human-authored static pages; preserve the existing markup style and Bootstrap-based layout in `index.html` when adding new pages or components.
- Filenames: lecture pages and links use exact paths (e.g., `LectureNotes/CS123-Topic06-2-PromptEngineering.html`). If you add files, ensure links use that directory structure and naming pattern so they appear on the site without extra build steps.
- Multiple language examples: labs include `.py`, `.js`, and `.cs`. When adding code samples, keep language-specific files together in the lab subfolder.
- Notebooks: Jupyter notebooks are used directly. Avoid altering notebook structure unless you update outputs consistently and preserve metadata (don't reformat cells unnecessarily).

Build / run / test guidance (discoverable from repo contents)
- There is no explicit build system (no package.json, no Makefile, no SSG). The repo appears intended to be served as-is via GitHub Pages. To preview locally:
  - Use a static file server from the project root (platform example): `python -m http.server 8000` and open `http://localhost:8000`.
  - For notebook preview/editing use Jupyter or VS Code's notebook support.

Integration points & external dependencies
- Pages include CDN-hosted Bootstrap and FontAwesome (see `index.html`). Don't vendor these libraries unless explicitly requested.
- The course chatbot iframe in `index.html` points to Copilot Studio — do not remove or hard-code credentials. Treat third-party embeds as read-only references.

Examples to copy patterns from
- To add a new lecture page, follow the existing pattern in `LectureNotes/` and add a link on `index.html` using the same list-group structure and Bootstrap classes.
- To add a new lab, create a folder under `Labs/` and mirror the structure used in `Lab01-Python/` (include `README` or an example HTML page linking to language-specific files).

Safety and minimal-impact rules for agents
- Don't change license, author metadata, or attribution blocks without explicit instruction. The footer contains Creative Commons licensing and author credit—preserve it.
- Avoid large-scale refactors (replacing site generator, reorganizing lecture names, or mass renaming) without a maintainer-confirmed issue.
- If adding automated tooling (CI, build), include a compact README note and keep changes confined to a single commit with clear intent.

When to ask for clarification
- If a requested change touches publishing (branch to use for GitHub Pages), navigation structure (index.html layout), or content licensing.

Files worth checking first when assessing a task
- `index.html` — navigation and global layout.
- `LectureNotes/` — examples of page naming and content style.
- `Labs/` — structure for multi-language examples and instructor-provided solutions.
- `JupyterNotebooks/` — examples where interactive content is expected.

If you update this file
- Merge existing human-written guidance and preserve instructor tone. Keep content short (20–50 lines) and repository-specific.

---
After you review these instructions, ask the repository owner which branch serves GitHub Pages and whether they'd like automated previews for PRs (optional follow-up).
