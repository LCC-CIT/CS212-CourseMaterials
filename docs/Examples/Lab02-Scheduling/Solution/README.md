# Lab 2 Class Example Solution

Solution for the [Lab 2 class example](../CS212_Lab02_Example.md): scheduling auto repair jobs with the Z3 constraint solver. It covers all of the requirements and both options in Challenge 2. It doesn't include Challenge 1.

| File | What it does |
| --- | --- |
| `data_loader.py` | Loads the CSV files into lists of dictionaries |
| `scheduler.py` | The Z3 model, solving, the unsat core, and Challenge 2 |
| `main.py` | Prints the schedule, the unsolvable data reports, and Challenge 2 results |
| `test_scheduler.py` | A plain Python schedule checker and the tests |
| `*.csv` | The data files from the lab instructions |
| `unsolvable_data/` | Three data sets that each break a different rule |

Run the program and the tests from this folder:

```bash
uv run main.py
uv run test_scheduler.py
uv run pytest           # the same tests, run with pytest
```

## Unsolvable Data Sets

| Folder | What was changed | Expected group in the core |
| --- | --- | --- |
| `uncertified_service` | Job J122 is a `diesel` job, and no mechanic is certified for diesel | `qualification` |
| `reversed_time_window` | Job J105 has `earliest_slot` 5 and `latest_slot` 3 | `time_window` |
| `too_many_jobs` | Only Fatima Noor (part-time, max 2) is certified for `air_conditioning`, which 3 jobs need | `workload` |

Keep a workload conflict small. In testing, a version with 14 jobs for 13 openings timed out instead of proving it was `unsat`.

## Notes on Challenge 2

- Option A (the `push()`/`pop()` loop) continues from the count in each schedule it finds, instead of lowering the limit by 1 each time, so it needs fewer checks.
- Option B (`Optimize`) turns the constraint groups on by adding the flags as constraints. Passing them to `check()` as assumptions made the optimizer time out in testing.
