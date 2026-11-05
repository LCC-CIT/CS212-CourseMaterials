# Group B check scripts

Run these on your own programs before you submit. They are the same scripts the grader uses to
score "Has all functionality", so if every line says PASS you have met that requirement.

## How to run

Put the files in this folder anywhere, open a terminal **in the folder that holds your two
programs**, and run:

```
python /path/to/check_rooms.py
python /path/to/check_server.py
```

(Use `python3` on macOS/Linux, or `uv run` if you use uv.) Each case prints one line:

```
PASS 6 attendees, no projector: Room Gamma
FAIL Health 2, 4 hours: MEDIUM
```

- **Part 1 (`check_rooms.py`)** finds your meeting room reservation program and tries every headcount tier (1, 5, 6, 15, 16 and more), with and without a projector, plus 0 and negative headcounts.
- **Part 2 (`check_server.py`)** finds your server status program and tries every health code and time combination, including the 4-hour and 10-hour boundaries.

The scripts call a function in your file that takes the two inputs (they match parameter names
such as `attendees, projector_needed / health_code, hours`); they also accept a function that prints its answer instead of returning it.
A FAIL means the program gave a different answer than the table in the lab instructions, or the
checker could not find or call a function. Read the message, fix your program and run it again.

## For the instructor (grader)

`probe.py` holds the shared helpers (the same file is in each group's `drivers` folder). The
grader config (`lab01_config.json` in the grading repo) keeps a copy of this folder and runs it for each group's
`testCheck` entries (this folder is the master; re-copy it when it changes).
