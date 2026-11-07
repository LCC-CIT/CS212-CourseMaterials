# GradingAssistant — CS212

Grading configuration for **CS212**, used by [CS-GradingAssistant](https://github.com/ProfBird/CS-GradingAssistant), the course-neutral grading tool (clone it separately; it holds no course files).

## What is in this folder

- `course_config.json` — course name, Python as the default language, uv/Colab settings.
- `ruff.toml` — course-wide lint rules (pep8-naming and import order, matching the style checklist).
- `Lab01/lab01_config.json` — Lab 1 checks, with per-group (A/B/C) settings.
- Rubric: `../docs/Labs/Lab01-Python/CS212_Lab01_Rubric.xlsm`. Instructor check scripts: the `Group<X>/drivers` folders under `../docs/Labs/Lab01-Python/` are used in place.
- `notes/` — earlier working notes on onboarding CS212 (what is left to do, the drivers handoff).

## Using it

1. Clone [CS-GradingAssistant](https://github.com/ProfBird/CS-GradingAssistant) and run `npm install`.
2. Run `node bin/grade.js` (or `node bin/configure-lab.js`), choose **Add new course**, and browse to this folder. The path is saved in the tool's git-ignored `configs/local-config.json`, so each computer registers it once.
3. Grade a lab, e.g. `node bin/grade.js CS212 Lab03`.

The rubric spreadsheets are **not copied here**: each lab config's `rubricName` is a path relative to its config folder that points at the rubric in this repo's own lab folder, so that file is the single template. See the tool's [User Guide](https://github.com/ProfBird/CS-GradingAssistant/blob/main/USER_GUIDE.md) for the config format.
