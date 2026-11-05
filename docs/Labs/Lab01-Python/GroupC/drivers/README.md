# Group C check scripts

Run these on your own programs before you submit. They are the same scripts the grader uses to
score "Has all functionality", so if every line says PASS you have met that requirement.

## How to run

Put the files in this folder anywhere, open a terminal **in the folder that holds your two
programs**, and run:

```
python /path/to/check_compat.py
python /path/to/check_athlete.py
```

(Use `python3` on macOS/Linux, or `uv run` if you use uv.) Each case prints one line:

```
PASS Speed 90, strength 80: Elite
FAIL LGA1700 with DDR3 is Incompatible
```

- **Part 1 (`check_compat.py`)** finds your PC compatibility program and tries each socket and RAM combination, other sockets, and lowercase input.
- **Part 2 (`check_athlete.py`)** finds your athlete rating program and tries every tier, including the 90/80, 70 and 50 boundaries.

The scripts call a function in your file that takes the two inputs (they match parameter names
such as `socket_type, ram_type / speed, strength`); they also accept a function that prints its answer instead of returning it.
A FAIL means the program gave a different answer than the table in the lab instructions, or the
checker could not find or call a function. Read the message, fix your program and run it again.

## For the instructor (grader)

`probe.py` holds the shared helpers (the same file is in each group's `drivers` folder). The
grader config (`lab01_config.json` in the grading repo) keeps a copy of this folder and runs it for each group's
`testCheck` entries (this folder is the master; re-copy it when it changes).
