# Group A check scripts

Run these on your own programs before you submit. They are the same scripts the grader uses to
score "Has all functionality", so if every line says PASS you have met that requirement.

## How to run

Put `check_shipping.py`, `check_recommend.py` and `probe.py` anywhere, open a terminal **in the
folder that holds your two programs**, and run:

```
python /path/to/check_shipping.py
python /path/to/check_recommend.py
```

(Use `python3` on macOS/Linux, or `uv run` if you use uv.) Each case prints one line:

```
PASS Zone A 5 kg costs $10
FAIL Zone B 10 kg costs $20 (got 25.0)
```

- **Part 1 (`check_shipping.py`)** finds your shipping program (the file that mentions zones) and
  tries every zone and weight tier, the boundaries (5, 5.01, 10, 10.01 kg), a lowercase zone and an
  invalid zone. It works with a function that takes a weight and a zone and returns or prints the cost.
- **Part 2 (`check_recommend.py`)** finds your recommender (the file that mentions horizon, invest
  or risk) and tries all four horizon/risk combinations. It accepts a function taking a horizon and
  a risk, or a program that reads them with `input()` in either order.

A FAIL means the program gave a different answer than the table in the lab instructions, or the
checker could not find or call it. Read the message, fix your program and run it again.

## For the instructor (grader)

`probe.py` holds the shared helpers. To wire these into the AI grader, give each group's
`testCheck` entries `supportFiles` `{ "from": "<this folder>", "to": "grader_checks" }` and entries
`grader_checks/check_shipping.py` / `grader_checks/check_recommend.py` (see `lab01_config.json`'s
`_note` in the grading repo, which keeps a copy of this folder).
