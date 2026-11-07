# Hand-off: CS212 Lab01 drivers and grading (Fall 2026)

Written 2026-11-04 so a new chat can continue the work done after Brian asked how to check
that students' Python programs "have all the required functionality" when no unit tests were
supplied. Earlier work in the same session (file picker, Canvas, model manager, etc.) is already
committed and not covered here. Full raw transcript:
`/Users/brian/.claude/projects/-Volumes-DataCard-Repos-CS233JS-Repos-CS233JS-AI-Grading/27adf9e1-9045-4a1c-8790-9d59bf8e6045.jsonl`.

## Decisions
- Approach: run the students' programs against instructor "drivers" (scripts that print one `PASS`/`FAIL` line per case) and score proportionally with `test_check`; use `llm_check` (AI suggestion, always marked NEEDS REVIEW) only for judgement rows. Boundary logic is tested deterministically, not by an LLM.
- Students were never given an I/O spec, so the drivers are tolerant: they call the student's function by parameter name (also objects with attributes, enum members, strings for booleans), or for Group A Part 2 feed stdin in several styles; keyword matches are partial so typos ("Coporate", "advance", "Denined") don't fail.
- Drivers are shared with students (Brian wants that): each group's folder is self-contained and has a student-facing README.

## Where things are
- Drivers (course materials repo, `/Volumes/DataCard/Repos/CS212-Repos/CS212-CourseMaterials/docs/Labs/Lab01-Python/`):
  - `GroupA/drivers/` — `check_shipping.py` (23 cases), `check_recommend.py` (4), `probe.py`, README
  - `GroupB/drivers/` — `check_rooms.py` (18), `check_server.py` (15), `probe.py`, README
  - `GroupC/drivers/` — `check_compat.py` (11), `check_athlete.py` (14), `probe.py`, README
  - `probe.py` is duplicated in each folder (keep in sync): runs student code in a child process, `run_cases()` tries every candidate function/variant.
- Grader repo (`/Volumes/DataCard/Repos/CS233JS-Repos/CS233JS-AI_Grading`):
  - `configs/CS212/Lab01/lab01_config.json` — rows C10/C18 are `test_check` with `testId` part1/part2. Base `testCheck` is a placeholder (NEEDS MANUAL CHECK); `variations.A/B/C.overrides.testCheck` run each group's drivers via `supportFiles` from a relative path to the course-materials repo (both repos must sit side by side as on Brian's machine). Note in `_note`.
  - `src/adapters/python.js` — script-mode `testCheck.entry` may now be a path inside a `supportFiles` `to` folder (an instructor-supplied checker is run as supplied). Test: `test/python_supplied_checker.spec.mjs`.
  - `src/lib/student_group.js` + `src/pipeline/run_pipeline.js` — `Artifacts/group_overrides.json` (`{"Student Name": "A"}`) assigns a group by hand, winning over the review form and code detection. Test in `test/student_group.spec.mjs`. Documented in CLAUDE.md.
  - `configs/local-config.json` (gitignored) — `toolchains.python` set to uv's Python 3.14 (`/Users/brian/.local/share/uv/python/cpython-3.14-macos-aarch64-none/bin/python3.14`) because the system Python is 3.9 and Josha Chapman-Dodson's `match` statement is a false syntax error there.
- Student data: `/Volumes/DataCard/Repos/CS212/Lab01/` (`SubmissionsAndAssessment/<Student>/extracted_code`, `Artifacts/`). Backup of the folder before the first regrade: `/tmp/Lab01-backup-before-regrade` (may be gone).
- Regrade command (term prompt answered on stdin): `printf 'Fall 2026\n' | node bin/grade.js CS212 Lab01 --regrade` (writes the `*_Grade.xlsm` files; graderCell "Computer" means they are overwritten, a changed value makes a versioned copy). `node bin/rubric-to-md.js <file>_Grade.xlsm` dumps a sheet (delete the `.md` it leaves).

## Findings (Fall 2026, functionality rows, Part 1 / Part 2)
- Group A (7): all full credit (5 and 12). Michael Coiner's review form says B but his code is A.
- Group B: Josha Chapman-Dodson 4/5, 11/12 (`attendees > 1` rejects 1; `h >= 4` should be `> 4`); Zoie Danison full, 14/15 (code 1 with 0 hours not HIGH); Zach Snyder 4/5, 2/12 (changed the rooms; server program uses random inputs and a different table); Shaka, Maksym, Stephanie, Tria full.
- Group C: Joseph Sutton 2/5 (unknown socket / unlisted RAM prints "Invalid input" instead of "Incompatible"), full on Part 2; Tyler Beach 4/5 (lowercase input), full on Part 2 — **Tyler Beach was listed by Brian as Group B but his files are Group C's; graded as C** (check with Brian); Blake Gilmore, Xan Kau, Steven Peltier, Tyler Urben, Cody Watkins full. Anthony Robinson is inactive (no submission).
- Groups assigned in `Artifacts/group_overrides.json`: Michael Coiner, Melina Deinum-Buck, Manuel Rojas Meza = A; Tyler Beach, Blake Gilmore, Tyler Urben = C (others come from review forms).
- Still "NEEDS MANUAL CHECK" on every sheet: the `llm_check` rows (no local Ollama model running) and the lint rows (ruff not installed).

## State at hand-off
- Committed earlier: `714370c` and `b977880` (grader repo), `eb6c2e8` (course materials, Group A drivers).
- **Uncommitted, awaiting Brian's yes:** grader repo — `CLAUDE.md`, `configs/CS212/Lab01/lab01_config.json`; course materials repo — `GroupA/drivers/probe.py` (updated), new `GroupB/drivers/` and `GroupC/drivers/`. Nothing has been pushed in either repo.
- Brian's working preference: ask before committing; commit directly on main on approval; never push unasked.

## Possible next steps
- Commit both repos once Brian approves.
- Confirm Tyler Beach's group; add groups for anyone else shown as "lab group unknown".
- Get Ollama running and ruff installed (e.g. via uv) so the AI and lint rows fill in; regrade.
- Add one line to the Lab 01 instructions fixing the input order and wording so drivers can be strict next term.

## Update (later the same day)
- The drivers are now copied into `configs/CS212/Lab01/drivers/Group{A,B,C}/` and the config's `supportFiles` use those relative paths, so nothing depends on where the repos sit. The CS212-CourseMaterials copies stay the master; re-copy after changing them.
- `llm_check` rows use DeepSeek via the new `openai` provider (`llmCheck` in the lab config; key/model from `local-config.json`). Verified with a trivial request only; not yet regraded.
- Instructions drafts with fixed function names/IO: `Group*/CS212_Lab01_Instructions_Group*_draft.md` in CS212-CourseMaterials. Tyler Beach stays Group C.

## Overnight batch (2026-11-04/05) — what changed, commit by commit
1. `51c0bd8` Lab01 config: C12/C20 `browser_check` -> `build_check` (syntax check; no more "No console errors"); `developer_comments` now needs name AND date in EACH file, ignoring "Brian Bird" headers (**zeroes the row for 15 of 22 students whose files have no header — to relax, set `"scope": "any"` and drop `require`**); `llmCheck.model` pinned; comprehensive-test guidance rewritten.
2. `c1592a9` Python preflight warns once about missing ruff / interpreter older than 3.12; phases slower than 10 s print their time; `skipStudents` config key (Lab01: "Test Student"); `test_check` comments "REVIEW: low pass rate" below 50%.
3. `df5a74d` `llm_check`: student names replaced by `[STUDENT]` for cloud models (`redactNames`); answers cached in `<student folder>/.llm_check_cache.json` (unchanged regrade 113 s -> 9 s; delete the file or set `llmCheck.cache:false` to force new AI answers).
4. Last commit: `bin/sync-drivers.js` (+ `cs233-sync-drivers`) copies/compares the drivers between the course-materials repo and `configs/CS212/Lab01/drivers`; ruff-fallback and sync tests; drivers got a strict mode (`LAB_STRICT=1`: only the function named in the `_draft` instructions is called). Also fixed `check_rooms.py`: "Reservation Denied" is now an acceptable answer for 0 or negative attendees (it was counted as recommending a room); no Fall 2026 grade changed.
All sheets were regraded after each change (Test Student is skipped now; its old sheet is still on disk).

## Follow-up batch (same night)
- `testCheck.strict` / `testCheck.env` (strict mode reachable from config; NOT turned on for Fall 2026 — students had no fixed names; turn it on per group entry next term).
- Redaction also hides e-mail addresses, GitHub/GitLab account names and `llmCheck.redactTerms` (this changed the prompts, so the next regrade re-asks the AI once; the cache then refills).
- `configure-lab.js` now asks for the AI-check provider/address (when the lab has `llm_check` rows) and for students to skip.
- USER_GUIDE / DEVELOPER_GUIDE / CLAUDE.md document all of the above. Lint now checked before every commit (the hook only runs tests; one missing import in configure-lab.js was caught by lint and fixed in 5ce02a1).
