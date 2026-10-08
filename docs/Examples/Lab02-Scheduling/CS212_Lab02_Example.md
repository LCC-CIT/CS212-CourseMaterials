---
title: Lab 2, Example
description: Class example of Lab 2, using the Z3 constraint solver to schedule auto repair jobs, mechanics and service bays
keywords: constraint solver, Z3, scheduling, constraint satisfaction, unsat core, CSV files, testing
material: Lab Instructions
generator: Typora
author: Brian Bird
---

<h1>Lab 2, Scheduling with a Constraint Solver</h1>

<h2>Example</h2>

**CS 212, AI Programming 1**

This is the class example for Lab 2. It has the same requirements as the lab assignments for each group, but a different scheduling problem. We'll work through it in class, and a complete solution is in the [Solution folder](Solution/README.md).

<h2>Contents</h2>

[TOC]

## Scheduling an Auto Repair Shop

Every day, an auto repair shop has to decide when each repair job is done, which mechanic does it and which service bay it's in. Doing this by hand is slow and it's easy to create conflicts, such as two cars scheduled for the same bay at the same time.

In this lab you will write a Python program that uses the Z3 constraint solver to build the schedule. You won't write a search algorithm. Instead, you will describe what a valid schedule looks like, as constraints, and Z3 will find one.

## The Problem

The shop has 24 repair jobs to do in one day, with 10 mechanics and 5 service bays. Each job is done in one of 8 time slots.

| What | How many | Data file |
| --- | --- | --- |
| Repair jobs | 24 | `jobs.csv` |
| Mechanics | 10 (6 full-time, 4 part-time) | `mechanics.csv` |
| Service bays | 5 | `bays.csv` |
| Time slots | 8 (numbered 0 to 7) | none, the slots are fixed (see below) |

Each time slot is one hour. Every job, including a test drive, fits in one hour, so the bay and mechanic are free again at the start of the next slot.

| Slot | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Time | 7:00 am | 8:00 am | 9:00 am | 10:00 am | 11:00 am | 12:00 pm | 1:00 pm | 2:00 pm |

To keep the problem manageable, every job takes exactly one time slot, there are no jobs that must be done in a certain order, every bay's lift can hold every vehicle, and every mechanic can work in any time slot.

### Scheduling Rules

A valid schedule must follow all of these rules. Each rule will become a group of constraints in your program.

| # | Rule | Constraint group name |
| --- | --- | --- |
| 1 | Every job gets a time slot (0 to 7), a mechanic and a bay that exist in the data. | `domain` |
| 2 | No two jobs can use the same bay in the same time slot. | `bay_conflict` |
| 3 | No mechanic can be assigned to two jobs in the same time slot. | `mechanic_conflict` |
| 4 | Each job is done by a mechanic who is certified for that kind of service, for example brakes or transmission. | `qualification` |
| 5 | No mechanic is assigned more jobs than their `max_jobs` limit: 3 for full-time mechanics and 2 for part-time mechanics. | `workload` |
| 6 | Each job is done within its allowed time window (`earliest_slot` to `latest_slot`). For example, a customer who needs their car back by 10:00 am wants slot 0, 1 or 2. | `time_window` |

## Data Files

The data files have already been created for you: [mechanics.csv](Data/mechanics.csv), [bays.csv](Data/bays.csv) and [jobs.csv](Data/jobs.csv). To download all three at once, use this link: [Download the example data files as a zip file](https://download-directory.github.io/?url=https://github.com/LCC-CIT/CS212-CourseMaterials/tree/main/docs/Examples/Lab02-Scheduling/Data). Unzip the file and move the three CSV files into your project folder. They have the columns described below. In columns that hold a list, the items are separated with semicolons, for example `brakes;engine;electrical`.

**`mechanics.csv`**

| Column | Meaning |
| --- | --- |
| `mechanic_id` | A short ID, for example `M01` |
| `name` | Mechanic's name |
| `max_jobs` | Most jobs this mechanic can do in a day: 3 for full-time, 2 for part-time |
| `certifications` | Kinds of service this mechanic is certified for |

**`bays.csv`**

| Column | Meaning |
| --- | --- |
| `bay_id` | A short ID, for example `Bay1` |

**`jobs.csv`**

| Column | Meaning |
| --- | --- |
| `job_id` | A short ID, for example `J101` |
| `service` | The kind of service this job needs, for example `brakes` |
| `earliest_slot` | Earliest allowed time slot |
| `latest_slot` | Latest allowed time slot |

## Requirements

1. **Data files.** Download the [zip file of data files](https://download-directory.github.io/?url=https://github.com/LCC-CIT/CS212-CourseMaterials/tree/main/docs/Examples/Lab02-Scheduling/Data), unzip it and put the three CSV files described above in your project folder.
2. **Loading data.** Load each CSV file into a list of dictionaries, for example with `csv.DictReader`. Convert numbers to `int` and split the semicolon lists into Python lists.
3. **Decision variables.** For each job, create three Z3 `Int` variables: its time slot, its mechanic (an index into the mechanics list) and its bay (an index into the bays list).
4. **Constraints.** Add constraints for all six scheduling rules. You will need these Z3 tools: `And`, `Or`, `Implies`, and `Sum` combined with `If` for counting (rule 5). For rules 2 and 3 you can use either `Implies` on every pair of jobs or `Distinct`.
5. **Solving.** Use a Z3 `Solver` to find a schedule. Read the values out of the model and return the schedule as a list of dictionaries. Print the schedule in a readable table sorted by time slot, showing the time, job ID, service, mechanic and bay.
6. **Explaining an impossible schedule.** Create one Boolean tracking variable per constraint group (the names in the rules table) and add each constraint as `Implies(group_flag, constraint)`. Call `check()` with all the flags as assumptions. When the result is `unsat`, print the names of the groups in `unsat_core()`. Make a folder named `unsolvable_data` with three modified copies of the data files, each of which breaks a different rule. For example: a service that no mechanic is certified for, a job whose `earliest_slot` is later than its `latest_slot`, or a service needed by 3 jobs that only one part-time mechanic (`max_jobs` of 2) is certified for. Your program must report the conflicting groups for each one. Keep each conflict small. Proving that no solution exists can take Z3 a very long time, and in testing for this lab, a larger version of the last example (14 jobs needing one service for 13 openings) timed out instead of returning `unsat`.
7. **Separation of concerns.** Keep the Z3 model and solving code in its own module, separate from file loading and from user input and output.
8. **Testing.** Write a test module with a function that checks a schedule against all six rules in plain Python, without using Z3. Use it to test that:
   - the schedule from your real data passes every rule,
   - each data set in `unsolvable_data` is reported as `unsat` with the expected constraint group in the core,
   - the checker itself catches a schedule that you broke on purpose, for example by putting two jobs in the same bay at the same time.

> **Example: a simple test driver**
>
> You don't need a testing framework for requirement 8. Write each test as a function that uses `assert`, which stops the function with an `AssertionError` if its condition is `False`. Then write a short "test driver" loop that calls each test function and reports whether it passed.
>
> This small example tests a checker for one rule, using two hand-made schedules:
>
> ```python
> # A checker for one rule, written in plain Python (no Z3)
> def has_bay_conflict(schedule):
>     """Return True if two jobs are in the same bay in the same time slot."""
>     for j in range(len(schedule)):
>         for k in range(j):
>             if (schedule[j]["slot"] == schedule[k]["slot"]
>                     and schedule[j]["bay_id"] == schedule[k]["bay_id"]):
>                 return True
>     return False
> 
> # Each test is a function. assert stops the test with an error if its condition is False.
> def test_good_schedule_has_no_bay_conflict():
>     schedule = [
>         {"job_id": "J101", "slot": 0, "bay_id": "Bay1"},
>         {"job_id": "J102", "slot": 0, "bay_id": "Bay2"},
>     ]
>     assert not has_bay_conflict(schedule)
> 
> def test_bay_conflict_is_caught():
>     schedule = [
>         {"job_id": "J101", "slot": 0, "bay_id": "Bay1"},
>         {"job_id": "J102", "slot": 0, "bay_id": "Bay1"},    # same bay and slot
>     ]
>     assert has_bay_conflict(schedule)
> 
> # The test driver: run each test function and report whether it passed
> tests = [test_good_schedule_has_no_bay_conflict, test_bay_conflict_is_caught]
> passed = 0
> for test in tests:
>     try:
>         test()
>         print("PASS:", test.__name__)
>         passed = passed + 1
>     except AssertionError:
>         print("FAIL:", test.__name__)
> print(passed, "of", len(tests), "tests passed")
> ```
>
> Output:
>
> ```
> PASS: test_good_schedule_has_no_bay_conflict
> PASS: test_bay_conflict_is_caught
> 2 of 2 tests passed
> ```
>
> The `tests` list holds the functions themselves (no parentheses), so the loop can call each one with `test()`, and `test.__name__` is the function's name. Put your own tests in the list and run the module with `uv run test_scheduler.py`, or whatever you named it. If you already know `pytest`, you can use it instead: it finds and runs functions whose names start with `test_`.

## Z3 Tips

These snippets show the pattern for this problem. Your code will need more than this. In your program, the file loading code goes in its own module (requirement 7). The file names have no folder in them, so Python looks for the CSV files in the folder you run the program from.

```python
# TODO: Split this code into modules: file loading, the Z3 model and solving,
#       and user input and output (requirement 7)

import csv
from z3 import Solver, Int, Bool, And, Or, Implies, Sum, If, sat, unsat

# Load a CSV file into a list of dictionaries (requirement 2)
# Each row becomes a dictionary whose keys are the column names,
# for example {"job_id": "J101", "service": "brakes", ...}
def load_csv(filename):
    rows = []
    with open(filename, newline="") as file:    # "with" closes the file when done
        reader = csv.DictReader(file)
        for row in reader:
            rows.append(row)
    return rows

mechanics = load_csv("mechanics.csv")
bays = load_csv("bays.csv")
jobs = load_csv("jobs.csv")

# Every value is read as a string, so convert the numbers to int
# and split the semicolon lists into Python lists
for mechanic_info in mechanics:
    mechanic_info["max_jobs"] = int(mechanic_info["max_jobs"])
    mechanic_info["certifications"] = mechanic_info["certifications"].split(";")
for job in jobs:
    job["earliest_slot"] = int(job["earliest_slot"])
    job["latest_slot"] = int(job["latest_slot"])

# One set of decision variables per job (requirement 3)
slot = []
mechanic = []
bay = []
for job in jobs:
    job_id = job["job_id"]
    slot.append(Int("slot_" + job_id))
    mechanic.append(Int("mechanic_" + job_id))
    bay.append(Int("bay_" + job_id))

# One tracking flag per constraint group (requirement 6)
group_names = ["domain", "bay_conflict", "mechanic_conflict", "qualification",
               "workload", "time_window"]
flags = {}        # a dictionary, like an object in JS or a Dictionary in C#
flag_list = []
for name in group_names:
    flags[name] = Bool(name)
    flag_list.append(flags[name])

solver = Solver()
solver.set("timeout", 10000)    # milliseconds

# Every constraint is added through this function so it belongs to a group
def add(group, constraint):
    solver.add(Implies(flags[group], constraint))

# TODO: Add the constraints for the other rules (requirement 4):
#       domain, bay_conflict, mechanic_conflict, qualification and time_window

# Counting with Sum and If (rule 5)
# If(condition, 1, 0) works like the ternary operator: condition ? 1 : 0
for w in range(len(mechanics)):
    terms = []
    for j in range(len(jobs)):
        terms.append(If(mechanic[j] == w, 1, 0))
    count = Sum(terms)
    add("workload", count <= mechanics[w]["max_jobs"])

result = solver.check(flag_list)    # the flags are passed in as assumptions
if result == sat:
    model = solver.model()
    # Read a value from the model and convert it to a Python int
    first_slot = model.eval(slot[0], model_completion=True).as_long()
    # TODO: Read every job's slot, mechanic and bay out of the model,
    #       return the schedule as a list of dictionaries and print it
    #       as a table sorted by time slot (requirement 5)
elif result == unsat:
    print("Conflicting rules:", solver.unsat_core())
# TODO: Handle the case where result is unknown (the solver timed out)

# TODO: Run the program on each data set in the unsolvable_data folder (requirement 6)
# TODO: Write the test module with a plain Python schedule checker (requirement 8)
```

## Optional Challenges

**Challenge 1: Lift capacity and mechanic availability.** Make the problem more realistic by adding two more rules:

| # | Rule | Constraint group name |
| --- | --- | --- |
| 7 | Each job is in a bay whose lift can hold at least the vehicle's weight. | `capacity` |
| 8 | No mechanic is scheduled in a time slot listed as unavailable for them. | `availability` |

The data files you were given don't have this information, so you will need to refactor them. Add these columns and fill in values for every row:

| File | Column | Meaning |
| --- | --- | --- |
| `bays.csv` | `lift_capacity_lbs` | Most weight the bay's lift can hold, in pounds |
| `jobs.csv` | `vehicle_weight_lbs` | Weight of the vehicle, in pounds |
| `mechanics.csv` | `unavailable_slots` | Time slots this mechanic can't work (lunch, training), for example `4;5` |

Your data should meet these extra requirements:

- The 5 bays have different lift capacities, and at least 2 jobs are too heavy for every bay except the one with the strongest lift.
- Each mechanic has 1 or 2 unavailable time slots.

If Z3 says your data has no solution, that's not necessarily a bug in your code. Use the unsat core to find out which rules conflict, then adjust your data.

Update your loading code for the new columns, add the two new groups to your tracking flags, add a data set to `unsolvable_data` that breaks each new rule (for example, a vehicle heavier than the strongest lift can hold), and update your checker and tests to cover all eight rules.

**Challenge 2: Minimizing part-time jobs.** The shop would rather give its full-time mechanics a full day of work than rely on part-time mechanics. Find a schedule that has as few jobs done by part-time mechanics as possible, and print that number and the schedule that goes with it.

First, count the jobs done by part-time mechanics. This uses `Sum` and `If` like the workload counting in the Z3 tips, with one `If` for each job:

```python
part_time_terms = []
for j in range(len(jobs)):
    # A list of conditions: "job j is done by part-time mechanic w"
    done_by_part_time = []
    for w in range(len(mechanics)):
        if mechanics[w]["max_jobs"] == 2:    # part-time
            done_by_part_time.append(mechanic[j] == w)
    # Count 1 if any of those conditions is true
    part_time_terms.append(If(Or(done_by_part_time), 1, 0))
part_time_jobs = Sum(part_time_terms)
```

The full-time mechanics can do at most 6 × 3 = 18 jobs, so at least 24 − 18 = 6 jobs must go to part-time mechanics. That makes 6 the lowest possible value. Proving that no solution exists can take Z3 much longer than finding one, so both approaches below use 6 as a lower bound instead of asking Z3 to prove that 5 is impossible.

Choose one of these two approaches. If you have time, try both and compare them.

**Option A: A loop with `push()` and `pop()`.** Keep using your `Solver`. In a loop, add a constraint that `part_time_jobs` is at most *k*, check, then lower *k* and try again. Stop when the check is `unsat` or `unknown`, or when *k* reaches 6.

> **Example: a loop with `push()` and `pop()`**
>
> `push()` saves a checkpoint of the constraints the solver has so far. `pop()` goes back to the last checkpoint, removing any constraints that were added after it. This lets you try a constraint, check it, and then take it back out before trying a different one.
>
> This small example finds the smallest `x` where `x + y == 10` and `y` is at most 7. Each time through the loop it tries a tighter limit on `x`, until there's no solution.
>
> ```python
> from z3 import Solver, Int, sat
> 
> x = Int("x")
> y = Int("y")
> solver = Solver()
> solver.add(x + y == 10, x >= 0, y >= 0, y <= 7)
> 
> best_x = None
> limit = 10
> while limit >= 0:
>     solver.push()                # save a checkpoint of the constraints
>     solver.add(x <= limit)       # try a tighter limit
>     result = solver.check()
>     if result == sat:
>         best_x = solver.model()[x].as_long()
>     solver.pop()                 # go back to the checkpoint (removes x <= limit)
>     if result != sat:
>         break                    # no solution with this limit, so stop
>     limit = limit - 1
> 
> print("Smallest x:", best_x)     # Smallest x: 3
> ```
>
> Read the value out of the model before calling `pop()`, because the model belongs to that check. In this challenge, the limit is on `part_time_jobs` instead of on `x`.

- **Pros:** It uses the `Solver` you already have. Every check that succeeds gives you a complete schedule, so if a later check times out you still have the best one found so far. You can print *k* each time through the loop to watch it improve.
- **Cons:** You write more code, and Z3 runs many separate checks. You have to decide when to stop the loop.

**Option B: The `Optimize` class.** Z3 has an `Optimize` class that works like a `Solver`, with the same `add()`, `check()` and `model()` methods, plus a `minimize()` method. Add all of your constraints to an `Optimize` object instead of a `Solver`, then tell it what to minimize:

```python
from z3 import Optimize

optimizer = Optimize()
optimizer.set("timeout", 30000)    # milliseconds
# ... add all of your constraints with optimizer.add() ...

# Turn every constraint group on. Without this, Z3 can make the tracking
# flags False, which turns off your rules. (This is also much faster than
# passing the flags to check() as assumptions.)
for flag in flag_list:
    optimizer.add(flag)

optimizer.add(part_time_jobs >= 6)    # the lower bound
optimizer.minimize(part_time_jobs)

if optimizer.check() == sat:
    model = optimizer.model()
    print("Part-time jobs:", model.eval(part_time_jobs))    # Part-time jobs: 6
```

- **Pros:** It takes only a few lines of code, and Z3 does the searching for you.
- **Cons:** It's all or nothing: if the check times out, you may not get a schedule at all. It can be much slower than finding a single schedule. In testing for this lab, it took about 9 times longer without the lower bound, and on this kind of problem it sometimes returned wrong answers without one. It's also sensitive to how the count is written: with a separate `If` for every job and part-time mechanic pair, instead of one `If` per job as shown above, it timed out. Your model code must be able to add constraints to an `Optimize` object as well as a `Solver`.

## Submitting your lab work on Canvas

### Beta Version

- Post the beta version of your program to your team channel in Discord.

### Code Review

- Review one of your lab partners' code and post the review in your team channel on Discord.
- Submit a copy of the code review <u>you did</u> to the code review assignment on Canvas.

### Production Version

 Based on the code review and helpful advice from your lab partners, you may revise your code. On the code review from your lab partner, complete the “Prod.” column to show what you revised. Upload the following to the *Lab Production Version* assignment on Canvas:

1. The files: Python (.py) files (one or more) and the `unsolvable_data` folder. If you did Challenge 1, also include your refactored data files.
2. The code review <u>from your lab partner</u> with the “Prod.” column filled out by you.

### Grading Criteria

The main focus of grading will be on how you model the problem as constraints and on testing.



*These instructions were drafted by Claude Sonnet 5.5 and adapted by Claude Opus 5.5 for the class example.*
