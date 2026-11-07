# Multi-Course Readiness Review: Can the Grader Take On CS 212? — 2026-11-04

**Reviewer:** Claude Opus 5.5 (AI), at the maintainer's request
**Question:** Is the codebase structured to accommodate grading lab submissions from other
courses, in particular CS 212 (AI Programming 1, Python)?
**Builds on:** `docs/code_review_2026-07-24.md`. Findings from that review (the implicit
`student` contract, duplicated helpers, fail-open paths) are not repeated here.

**Method:** Every CS 212 lab write-up in `CS212-CourseMaterials/docs/Labs` was read for what
students submit and how it runs (Lab01–Lab08 plus TermProject). The rubric `.xlsm` files and all
ten code-review `.docx` forms were run through the grader's own parsers. Then the grader's
course/term/config plumbing, the Python adapter, `sandbox.js`, `runtime_check.js`,
`extract_code_canvas.js`, `read_code_review.js`, `analyze_code.js` and `generate_grades.js` were
read against those needs. Claims marked **verified** were reproduced by running the grader's code.

---

## Verdict

**The architecture is ready. The Python-specific details are not.**

The course and term tiers, the language-adapter layer, the phase registry, the mapping-handler
registry and Canvas acquisition generalize as intended. CIS195 has already proven that a second
course drops in cleanly. Nothing in the layering needs redesigning for CS 212, and there are
almost no hard-coded CS233JS values left in `src/`. The leftovers are cosmetic:
`citstudent`/`'Computer'` defaults and the `cs233-*` bin names.

The gaps are concentrated in four places that were built around CS233JS's specific way of
working (zipped or GitHub-hosted JS projects, `npm`, and "Prod." review forms):

1. **Acquisition:** loose-file Canvas uploads produce no code.
2. **Python execution model:** `requirements.txt`/`pip`/system interpreter/empty working directory,
   vs. CS 212's `pyproject.toml`/`uv`/project venv/`Data/` relative paths.
3. **Code-review form parsing:** CS 212's forms use different headers and have spacer rows.
4. **Per-group (A/B/C) configuration:** CS 212's groups solve *different problems*, not
   differently named versions of the same app.

Three findings in sections 1 and 3 below would **silently zero or misgrade students** on the first CS 212
run, so fix them before the first CS 212 lab goes through.

---

## 1. Blockers: would mis-score students on the first run

### 1.1 Loose-file Canvas uploads are never extracted — HIGH (verified by reading) — ✅ FIXED 2026-11-04

> **Fixed:** `acquireCode` now copies a submission's loose uploaded files (hidden files, archives and Word docs skipped) into `extracted_code/` when there's no zip and no repo, and merges loose files uploaded alongside a zip into its extracted contents (the zip wins a name collision). This covers both Canvas and Moodle.

`extract_code_canvas.js:37-47` `downloadAttachments` downloads every attachment but records only
`.zip` files. `importOneSubmission` then calls `acquireCode`, which has no zip and no GitHub
URL, so it reaches its final branch (`extract_code.js:228-231`) and sets
`student.error = 'No ZIP file or GitHub URL found'`. `extractedDir` stays `null`, so every
downstream phase skips the student.

CS 212 Lab01 ("This will be a total of 3 files": two `.py` plus the review `.docx`), Lab02
RuleBasedSystems (`.py` files plus a `.csv`) and Lab02 ConstraintSolvers (`.py` files plus an
`unsolvable_data` folder) all ask for bare uploads. Every one of those students would score 0.

**Fix direction:** when there's no zip and no repo but non-review attachments exist, copy the
non-`.docx` attachments into `extracted_code/` and treat that as the code directory. Leave the
review `.docx` in `canvas_files/`, where `read_code_review.js` already looks. Also handle a
student who zips only part of the work and uploads the rest loose. The idempotence check
(`extract_code_canvas.js:77-81`) already keys off `extracted_code/` being non-empty, so this fits
the existing layout.

### 1.2 Code-review forms headed "Release" never count as production-completed — HIGH (verified) — ✅ FIXED 2026-11-04

> **Fixed:** the production column now matches `/prod|release|final/i`. All 10 CS212 forms parse with `productionCompleted: true` when filled in.

`read_code_review.js:186-191` finds the production column with `h.includes('prod')`. Five of
CS 212's ten forms head that column **"Release"** (Lab02-RuleBased, Lab05, Lab06, Lab07, Lab08).
The positional fallback only fires when *both* headers are missing, and "Beta" is found, so
`prodCol` stays `-1`.

Verified with a synthetic filled table: header `Prod.` gives `productionCompleted: true`, while
header `Release` gives `false`. Every `code_review` mapping on those labs awards **half credit**
even when the student filled the column in.

**Fix direction:** match `/prod|release|final/i`, and/or make the header regex configurable via
`config.codeReview.prodHeader` so a course can declare its own wording.

### 1.3 Spacer rows in CS 212 forms misalign `manual` mappings — HIGH (verified) — ✅ FIXED 2026-11-04

> **Fixed:** review items now come from every Beta/Prod-headed table (multi-table forms such as CS233JS Lab03/Lab04 were invisible beyond the densest table) and carry their criterion `label`. A `manual` mapping selects its row with `reviewRow` (substring, or an array for a rubric row spanning several questions, plus `reviewRowOccurrence` for repeated questions). Positional matching was removed: without `reviewRow` a `manual` mapping is a pure placeholder. Every CS233JS `manual` mapping was reviewed against its course-materials review form. 22 now carry a verified `reviewRow`; 6 have no matching review question and stay placeholders (Lab04 TODOs, TermProject error handling, styling, UI friendliness, folder structure, and DevEnv layout). Lab02's mapping also lacked a `maxScore`, which would have scored a review "Yes" as `undefined`; it's now 6, matching the rubric.

`parseTableScores` pushes **every** table row as an item, and `generate_grades.js:1022-1027`
maps the *n*-th `manual` mapping to `items[n]`. CS 212 forms have blank continuation rows under
questions that ask the reviewer to list errors or missing items. Running the parser on the real forms:

| Form | Labeled criteria | Parsed items |
|---|---:|---:|
| Lab06 | 9 | 24 |
| Lab02 ConstraintSolvers | 18 | 29 |

The CS233JS forms have no spacer rows, which is why this has never surfaced.

**Fix direction:** skip rows whose first (criteria) cell is empty. Better still, let a
`manual` mapping name its review row by a label substring (`reviewRow: "interactive"`) instead
of relying on position. Position-based alignment is fragile even for CS233JS whenever a form is edited.

### 1.4 `developer_comments` passes almost every Python submission — HIGH (inflates scores) — ✅ FIXED 2026-11-04

> **Fixed:** the check now reads comment text only, using a new `extractComments` on every adapter built from the same grammar as `stripComments`; Python docstrings count. Per file it records name, date and AI-use disclosure (AI disclosure only in the file's first 40 lines). A mapping can `require` any of `name`/`date`/`ai` and set `scope: "each"`; the default stays name-or-date in any file. A boolean `requireAiDisclosure` turns the AI requirement on or off per assignment (on for CS233JS Lab01–04, whose forms ask for it), and `ignoreCommentsBy` keeps the instructor's starter-file header from counting as the student's. Two fixes along the way: a submitted `.venv`/`venv`/`__pycache__` is excluded from analysis, and source files with "dist" in their name (e.g. `distance.py`) are no longer dropped.

`analyze_code.js:436-440` sets `hasDeveloperComments` if **any** source file matches
`\b(name|author|date)\s*[:=]` or contains the student's first or last name as a substring. In
Python, `name = input("Name: ")` or a dict key `"date":` satisfies the first pattern. Short first
names also match common words as substrings (for example, "Al" in "algorithm"). The regex also
runs on raw content, not comment-stripped content. The CS 212 rubric line is "Developer's name, date
in **each** file", and the CS 212 review form adds "any AI used (and how)".

**Fix direction:** run the check against the *comments only* (the inverse of what the adapter's
`stripComments` removes), require it per file, and match whole words. Making the required tokens
configurable (`config.developerComments.require: ["name", "date", "ai"]`) would also cover CS 212's AI-disclosure line.

### 1.5 `run_check` can't run a CS 212 program as students are told to run it — HIGH — ✅ FIXED 2026-11-04

> **Fixed:** `execution.cwd: "copy"` (CS212's course default) runs the program in a throwaway copy of its project folder, and `runCheck.supportFiles` adds instructor files such as `Data/` where the student has none. uv projects get a cached, grader-owned environment and run with its Python. `runCheck.entry` picks the program, and the `main.py` default is now an exact match. Student processes also no longer see the grader's secrets (`CANVAS_TOKEN`, API keys) in their environment. An end-to-end test (`test/python_run_integration.spec.mjs`) covers a nested uv project, instructor data and a PASS/FAIL test driver. Per-group data and multiple entry points are step 6.

Three compounding problems:

- **Working directory.** `sandbox.js:71` always runs in a fresh, empty `mkdtemp` directory. CS 212
  programs open `Data/instructors.csv` and similar files relative to the project folder, and the
  instructions explicitly say to run from there. Every Lab02-ConstraintSolvers run fails on file
  not found.
- **Interpreter/dependencies.** `python.js:193` builds `[python3, main.py]` against the system
  interpreter. CS 212 labs need `z3-solver`, `scikit-learn`, `tensorflow` or `google-genai`, installed by
  `uv sync` into the project's `.venv`.
- **Entry point.** `/main\.py$/i` (`python.js:187`) matches `domain.py` (verified), and with no
  `main.py` it falls back to `pyFiles[0]`, which is whatever the directory walk returns first.

**Fix direction:**
- Add an opt-in `execution.cwd: "copy"` mode in `sandbox.js` that copies the project into the
  throwaway directory instead of starting it empty. That keeps the "never touches the submission tree"
  guarantee and lets relative paths work.
- Add a `runCheck.entry` config key, a glob or filename.
- Let the Python adapter build `["uv", "run", entry]` when a `pyproject.toml` exists.
- Since students often omit the `Data/` folder ("you don't need to upload the data"), add
  `runCheck.supportFiles`: a config-relative directory of instructor-supplied data copied in
  before the run.

---

## 2. Python adapter: built for a different Python workflow — ✅ FIXED 2026-11-04

> **Fixed:** everything in the table and fix list below is done:
> - `pyproject.toml` is read for the manifest, and a distribution-to-import alias map plus `packageCheck.importAliases` decide what counts as imported.
> - Dependencies install with `uv sync --no-install-project` into a cached environment keyed by `pyproject.toml`/`uv.lock`/`.python-version`. The sync runs in a scratch folder, never the submission, and has a 10-minute default timeout (`execution.installTimeoutMs`).
> - Tests run through the sandbox. `testCheck.mode: "script"` counts PASS/FAIL lines, and pytest mode adds pytest to the uv environment when needed.
> - `preflight` warns when uv is missing.
> - The requirements.txt/pip path is unchanged.
>
> Not verified against real packages: every test uses dependency-free projects offline, because syncing z3-solver or scikit-learn would download from PyPI.

The adapter in `src/adapters/python.js` is coherent, but it assumes `requirements.txt` + `pip` +
pytest. CS 212 standardized on **uv + `pyproject.toml`** from Lab02 onward.

| Area | Adapter assumes | CS 212 actually uses | Effect |
|---|---|---|---|
| Manifest (`checkManifest`) | `requirements.txt` | `pyproject.toml` `[project].dependencies` | "requirements.txt not found" for everyone |
| Package names (`extractUsedPackages`) | import name == distribution name | `scikit-learn`→`sklearn`, `z3-solver`→`z3`, `google-genai`→`google.genai` | Declared packages flagged "never imported" |
| Install | `python -m pip install -r` into the **grader's** interpreter | `uv sync` into a per-project `.venv` | Pollutes the grader's Python. Homebrew/system Python refuses because of PEP 668. 60 s timeout is far too short for TensorFlow |
| Tests (`runTests`) | `pytest -v` | Lab02 explicitly allows a plain `assert` + PASS/FAIL driver loop | Driver-style tests aren't counted, and pytest without the venv fails on imports |
| Timeouts | 10 s run / 30 s tests | Lab04 runs about 20 s; Lab05 trains for minutes; Lab03/04 download datasets on first run | Spurious timeouts |

**Fix direction (all inside the adapter, no pipeline changes):**
- `detectProject`: tag a project `python-uv` when `pyproject.toml` exists.
- `install`: run `uv sync` in the copied project directory. Cache the result by a hash of
  `pyproject.toml` plus `uv.lock` so a class of 25 identical dependency sets resolves once.
- `checkManifest`: parse `pyproject.toml`. Node has no TOML parser built in, so a small dependency or a
  minimal `[project]` table reader is needed.
- Ship a small distribution-to-import alias map, extendable from config.
- `runTests`: support a `testCheck.mode: "script"` that runs a named test module and scores by
  exit code and/or a configurable `PASS:`/`FAIL:` line count, alongside the existing pytest mode.
- `preflight`: also check for `uv` when the lab uses it.

**Lint:** `python/student.ruff.toml` selects `E, W, F, C90`. The CS 212 style checklist
explicitly grades snake_case/PascalCase/ALL_CAPS naming (ruff `N`) and import ordering (ruff `I`),
and arguably docstrings (`D`). Don't change the shipped default. Instead, add a **course-level**
lint candidate. Both adapters' `lintConfigCandidates` (`python.js:166`, `javascript.js:242`) look
only per-step, per-lab, then repo default. Add `configs/{Course}/ruff.toml` (and
`configs/{Course}/eslint.config.mjs`) between the per-lab and repo-default candidates.

> **✅ Lint item FIXED 2026-11-04:** `configs/{Course}/ruff.toml` / `eslint.config.mjs` are now looked up between the per-lab file and the shipped default (step > lab > course > shipped). `configs/CS212/ruff.toml` adds ruff `N` (pep8-naming) and `I` (import order); `D` (docstrings) was left out as too noisy for the checklist's "comments or docstrings explaining complex code". Not yet run against real ruff: ruff isn't installed on the development Mac.

---

## 3. Structural gaps that matter for CS 212 (and any third course)

### 3.1 No course-level config defaults — MEDIUM — ✅ FIXED 2026-11-04

> **Fixed:** `course_config.json` accepts a `defaults` block, merged under every lab/step config in memory before validation (lab wins; nested objects merge; arrays replace; per-assignment keys like `mappings` are rejected). `writeCourseConfig` now keeps fields it isn't updating, because the Canvas setup used to rewrite the file with only four fields, which would have deleted `defaults`. `configs/CS212/` exists with `"defaults": { "language": "python" }` and the course ruff ruleset. Choosing a course with no assignments yet now gives a clear error instead of an empty picker.

`course_config.json` holds only names, prefix and Canvas ID. Only `toolchains` is merged into a lab
config (`grade_setup.js:369`). Every CS 212 lab config would have to repeat `language: "python"`,
the runtime and execution settings, `codeReview` cells, and the lint, timeout and URL patterns. Add a
`defaults` block to `course_config.json`, deep-merged under each lab config before
`validateConfig`. It's a ~15-line change in `grade_setup.js`, and CS233JS and CIS195 would
benefit too.

### 3.2 Group variations only drive app-name detection — MEDIUM — ✅ FIXED 2026-11-04

> **Fixed:** `variations[group].overrides` holds the settings that differ for a group (`runCheck`, `testCheck`, `execution`, `analysis`, `packageCheck`, `webContent`), merged in per student by `lib/student_group.js`'s `configForStudent`. The review form is now read first, then a new `resolveGroups` phase settles each student's group (form letter, else detected from the code, now including `pyproject.toml`'s name), then the runtime check runs with that group's settings. A student whose group is unknown gets group-dependent rows flagged `NEEDS MANUAL CHECK: lab group unknown`, never scored with another group's settings. Validation checks each group's merged config on its own. The group-letter parser also accepts a lone lowercase letter, and checks confirmed it never reads the group-name cell.

`config.variations` maps a group letter to an `appName` used by `variation_detect.js`. The
detector's corpus is built from HTML titles, `package.json` and README files, and gets almost
nothing from a Python project. In CS 212, groups A, B and C solve **different problems**: Lab02 schedules
sections, flights or deliveries, and Lab01 has three different programs to translate. The group letter
is already read reliably from the review form. What's missing is per-variation overrides of
`runCheck` (stdin, expected output, supporting data), `analysis.features`, and possibly
mappings. A `variations.B.overrides: { … }` block applied after group detection would cover it.
Add `pyproject.toml`'s `name` to the variation corpus as a cheap secondary signal.

### 3.3 One entry point per submission — MEDIUM — ✅ FIXED 2026-11-04

> **Fixed:**
> - `runCheck` and `testCheck` can be lists of entries with `id`s; `run_check`/`test_check` mappings pick one with `runId`/`testId`.
> - `entry` can list several candidate filenames.
> - A program or test script that isn't found is flagged `NEEDS MANUAL CHECK` rather than scored 0.
> - An end-to-end test runs a Lab01-style submission with two programs, each given its own stdin, including the stdin-starved `EOFError` case.

`run_check` executes a single program. Lab01 has two independent programs plus tests, Lab04's flow
is `fetch_data.py` then the main program, and Lab02 has a program plus a test module. `parts[]`
matches *subdirectories*, not files, so it doesn't help with loose `.py` files. Allow
`runCheck` to be an array of `{ id, entry, stdin, expectPatterns }` with a `run_check`
mapping selecting one by `id`, the same pattern `file_count` uses with `countId`.

### 3.4 Notebooks and Colab links are invisible — scope note — ✅ FIXED 2026-11-04

> **Fixed:**
> - `.ipynb` is one of the Python adapter's source extensions. Analysis reads notebooks as Python scripts (`src/lib/notebook.js`: code cells as code, markdown cells as comments), so feature checks, the developer-comment check and import scanning see them, and ruff lints them.
> - A submission whose only code is a Colab link has its notebook downloaded through Google Drive's public download URL. That works only when the notebook is shared as "Anyone with the link"; otherwise a clear error tells the instructor to add it by hand.
> - CS212's course defaults now recognize Colab links (`urlPatterns.colab`).
> - Notebooks are analyzed and linted, never run.

Lab05 submits a `.ipynb` file or a Colab URL. `sourceExtensions` is `['.py']`, so analysis and lint
see nothing. A Colab link is a Google Drive resource that can't be fetched without auth.
Short term: add `colab: "colab.research.google.com"` to `urlPatterns` and use `url_check` +
`path_exists` (`\.ipynb$`). Treat real notebook analysis, extracting code cells to a temp `.py`,
as a separate feature if Lab05 is worth automating.

### 3.5 Web-only dependencies are loaded for every course — LOW — ✅ FIXED 2026-11-04

> **Fixed:** `run_pipeline.js` imports the HTML-validation, CSS-validation and web-content phases only when they run. HTML/CSS validation now runs for web-language labs (JavaScript/TypeScript) or labs with an `html_validate`/`css_validate` row. A Python lab never loads html-validate, csstree-validator or jsdom, and a test enforces that by failing if any of them is loaded.

`run_pipeline.js:31` statically imports `check_web_content.js`, which imports `jsdom`. On this Mac
`jsdom` is declared in `package.json` but **not installed** in `node_modules`, so 3 test files fail
to load (696 pass) and `bin/grade.js` can't run for any course. Running `npm install` fixes the
immediate problem, probably a two-machine sync leftover. Structurally, phases gated by
`when` should `await import()` their module lazily so a Python-only course never loads
jsdom, Puppeteer or html-validate.

### 3.6 `rubric-to-md.js` drops CS 212 rubrics — LOW (verified) — ✅ FIXED 2026-11-04

> **Fixed:** rendering moved to `src/lib/rubric_markdown.js`, built on `detectRubricLayout`. The bug also hit CS233JS: Lab01, Lab02 and the TermProject Final rubric say "Points" and came out as just a title, and sub-rows labeled in column B (Lab06, TermProject) and comments one column right of the header were dropped. The `-o`/`--output` flag is now handled, and any other `-…` argument is an error instead of a file name. The committed `CS233JS_Lab05_Rubric.md` and `CS233JS_Lab06_Rubric.md` weren't regenerated; Lab06's differs from its spreadsheet, so it may be hand-edited.

`bin/rubric-to-md.js:44` looks for a header cell that is exactly `Possible`. CS 212 rubrics say
`Points`, so the tool writes only the title line. `lab_config.js` already has
`POSSIBLE_HEADER_RE` / `detectRubricLayout`, so reuse them. (While testing this, note that
`rubric-to-md` writes its `.md` next to the input by default. Running it on the CS 212
course-materials repo created untracked files there, which were removed.)

---

## 4. What's out of scope for automation (say so explicitly in the configs)

- **Lab08** submits only screenshots. Use `path_exists` for image files at most, and grade manually.
- **Lab07** "AI prompt effectiveness", "secure API-key management" and "effectiveness of the AI
  feature" are judgment calls. Key handling can be partly automated, for example a `feature` that
  flags a hard-coded `AIza…`/`sk-…` literal plus `env_file_check`. The rest is `manual`.
- **Running Lab07 apps** calls a paid external API and needs a key, so don't `run_check` them.
- **Term project** has no rubric content yet beyond the title.

Much of CS 212's rubric is qualitative ("rule design", "moderately complex", "explanations in
comments"). The grader's regex/feature model can't score that. The repo already has an LLM client
(`llm_client.js`). A future `llm_check` mapping type that scores one rubric row against a prompt,
and **always** sets `keepComment` with a "NEEDS REVIEW" flag the way `deploy_check` does, would
fit the existing handler registry without new architecture. It's worth considering after the
blockers, not before.

> **✅ Built 2026-11-04 (step 8):** `llm_check` rows (`src/lib/llm_check.js`) take a `criterion`,
> with optional `guidance` and a `files` regex. The model reads the student's code (notebooks
> included) and suggests a score. The comment is always `NEEDS REVIEW (AI suggestion, <model>): <reason>`
> with `keepComment`, and any failure scores 0 with `NEEDS MANUAL CHECK: AI check unavailable`.
> The default model is a local Ollama one, so student code stays on the machine. A cloud
> provider is used only when `llmCheck.provider` sets one, never from the wizard's
> `local-config.json` setting. Tested with a fake model only; no real model ran during
> development (Ollama wasn't running).

---

## 5. Housekeeping noticed along the way

- ✅ **Done 2026-11-04:** the leftover folders below were deleted. They held only empty directories and `.DS_Store` files. The `Lab06/Volumes/…/26Sp/Lab06/ArtifactsAndRubrics` nesting was created on June 2 by pre-June-8 code, back when artifacts lived in `ArtifactsAndRubrics`. Today's rubric copy uses `path.basename()` before joining under `configs/`, so it can't recur.
- `configs/Lab05`, `configs/Lab06/Volumes/DataCard/Repos/CS233JS-Repos/…` (empty dirs),
  `configs/Lab08` and `configs/TermProject` are pre-course-tier leftovers. `getExistingCourses()`
  correctly ignores them, but delete them. The `Lab06/Volumes/...` nesting suggests an absolute path was
  once joined as a relative one somewhere; it's worth a grep if it reappears.
- ✅ **Checked 2026-11-04:** `configs/CIS195/course_config.json` has `canvasCourseId: 680`, the same number the CLAUDE.md
  example used for CS233JS. It's correct: CIS195 Lab03 has Canvas assignment 22147 saved by the same `--canvas`
  setup, which shows the course name for confirmation and lists only that course's assignments. The CLAUDE.md and
  DEVELOPER_GUIDE examples now use a placeholder ID instead.
- CS 212 `CS212_Lab01_Rubric.xlsm`: the *Rubric* sheet's title still reads "Lab 5: HTML5
  Canvas--Meme Creator", and the *Grade* sheet has a stale "New feature options" block (meme text,
  font, color) below the canned comments. `CS212_Lab06` has both an `.xlsm` and an `.xlsx` rubric.

---

## Suggested order of work

1. ✅ Loose-file Canvas extraction (1.1). Without it, nothing else matters for Lab01/02.
2. ✅ Review-form parsing: "Release" header and spacer rows (1.2, 1.3). Small, with high scoring impact.
3. ✅ `developer_comments` comment-only, per-file check (1.4).
4. ✅ Course-level `defaults` + course-level lint config (3.1, section 2's lint item).
5. ✅ Python uv workflow: `pyproject.toml`, `uv sync` in a copied directory, `runCheck.entry`,
   `supportFiles`, script-mode tests (1.5, section 2).
6. ✅ Per-variation overrides and multi-entry `runCheck` (3.2, 3.3).
7. ✅ Lazy phase imports, `rubric-to-md` header reuse, housekeeping (3.5, 3.6, 5).
8. ✅ Optional: `llm_check` mapping type; notebook extraction.

Steps 1–3 are independent bug fixes that also make CS233JS and CIS195 more robust. Steps 4–6 are
the CS 212 enablement work and should come with a pilot config for one lab, such as
Lab02-ConstraintSolvers, which exercises data files, z3, groups and tests, plus a
scratch-tree integration test like the existing `multi_step_integration.spec.mjs`.
