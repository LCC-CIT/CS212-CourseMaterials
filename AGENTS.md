# AGENTS.md

Course materials for **CS 212, AI Programming 1** at Lane Community College, by Brian Bird. Students are beginning Python programmers, so write for them.

## Repository Layout

- `docs/`: everything published to the course website, <https://lcc-cit.github.io/CS212-CourseMaterials/>.
  - `index.html`: course home page (Bootstrap layout). New pages appear on the site only if they're linked from here or from another page.
  - `LectureNotes/`: one Markdown file per topic, named `CS212-UnitNN-M-Topic.md` (`-0-Overview` is the week overview).
  - `Labs/`: lab instructions, rubrics, and code review forms, one folder per lab.
  - `Examples/`: runnable example projects (e.g., `ConstraintSolving/`, a `uv` project with a script, a notebook, and a README).
  - `_config.yml`, `_includes/head-custom.html`: Jekyll site settings, custom CSS, and the `[TOC]` script.
- `JupyterNotebooks/`, `ResearchNotes/`, `Tutorials/`: instructor working material that isn't published.

## Publishing

- GitHub Pages builds `docs/` from `main` with Jekyll (`jekyll-theme-primer`, kramdown GFM). There is no workflow file in the repo and no local build step.
- Jekyll converts `.md` to `.html`, and relative links to `.md` files work on the site. The generated HTML isn't in the repo.
- A failed deployment with a 5xx error is a GitHub problem, not a content problem. Check githubstatus.com or re-run the job.

## Markdown Conventions (Lecture Notes and Labs)

- Files are edited in Typora. Most start with YAML front matter (`title`, `description`, `keywords`, `generator`, `author`).
- The page title is an HTML `<h1>`, usually followed by `**CS 212 AI Programming 1**`. Longer lecture notes add a `<h2>Contents</h2>` heading and a `[TOC]` line, which the script in `head-custom.html` replaces with a table of contents built from the `##`–`####` headings.
- Pages end with an AI attribution line (if AI helped), then the Creative Commons BY-SA 4.0 footer. Don't change or remove either one without being asked.
- Keep edits concise and in the existing plain, friendly teaching voice. Don't rewrite sections you weren't asked to change.

## Code in Course Materials

- Use beginner-level Python: plain `for` loops with `.append()` instead of list or dict comprehensions, and no unnecessary advanced features. Keep an example notebook and its matching `.py` script in sync.
- Run every code sample you add or change, and make sure any output shown in comments matches the real output.
- Student-facing instructions must work on Windows, macOS, and Linux. Never include absolute paths from the instructor's machine.
- Python projects use [`uv`](https://docs.astral.sh/uv/) with a `pyproject.toml`; students run them with `uv run <script>.py`.

## Link Check

`.github/workflows/link-check.yaml` builds `docs/` with `actions/jekyll-build-pages` and runs [lychee](https://lychee.cli.rs/) on the result. It runs on pull requests and pushes to `main` that touch `docs/` or the checker's settings, weekly (to catch external link rot), and on demand. It fails on any broken link.

- Settings are in `lychee.toml` (accepts 200, 403, 429) and `.lycheeignore` (one regex per line).
- Fix a broken link rather than ignoring it. Add to `.lycheeignore` only a link that works in a browser but fails in CI, and add a comment saying why.
- The workflow remaps our own published URLs (`https://lcc-cit.github.io/CS212-CourseMaterials/...`) to the local build, so a new page doesn't fail before the site has deployed.
- Only `docs/` is published. A link to a folder outside it (such as `Tutorials/`) will be broken on the site.

## Working Here

- Commit and push only when the instructor asks. Leave notebook metadata and saved outputs alone unless the change requires otherwise.
