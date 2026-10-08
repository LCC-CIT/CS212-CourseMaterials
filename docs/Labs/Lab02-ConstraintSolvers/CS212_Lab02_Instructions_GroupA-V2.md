---
title: Lab 2, Group A
description: Group A assignment to use the Z3 constraint solver to schedule class sections, instructors and classrooms (simplified version)
keywords: constraint solver, Z3, scheduling, constraint satisfaction, unsat core, CSV files, testing
material: Lab Instructions
generator: Typora
author: Brian Bird
---

<h1>Lab 2, Scheduling with a Constraint Solver</h1>

<h2>Group A</h2>

**CS 212, AI Programming 1**

<h2>Contents</h2>

[TOC]

## Scheduling a CS Department

Every term, a computer science department has to decide when each class section meets, who teaches it and which room it's in. Doing this by hand is slow and it's easy to create conflicts, such as two sections in the same room at the same time.

In this lab you will write a Python program that uses the Z3 constraint solver to build the schedule. You won't write a search algorithm. Instead, you will describe what a valid schedule looks like, as constraints, and Z3 will find one.

## The Problem

The department offers 24 class sections, has 10 instructors and 5 classrooms. Classes meet on Monday and Wednesday in one of 8 time slots.

| What | How many | Data file |
| --- | --- | --- |
| Class sections | 24 | `sections.csv` |
| Instructors | 10 (6 full-time, 4 part-time) | `instructors.csv` |
| Classrooms | 5 | `classrooms.csv` |
| Time slots | 8 (numbered 0 to 7) | none, the slots are fixed (see below) |

Each time slot is a 1 hour 20 minute class period on Monday and Wednesday.

| Slot | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Time | 8:00 am | 9:30 am | 11:00 am | 12:30 pm | 2:00 pm | 3:30 pm | 5:00 pm | 6:30 pm |

To keep the problem manageable, every section takes exactly one time slot, every section stands alone (there are no lecture and lab pairs), every classroom is big enough for every section, and every instructor can teach in any time slot.

### Scheduling Rules

A valid schedule must follow all of these rules. Each rule will become a group of constraints in your program.

| # | Rule | Constraint group name |
| --- | --- | --- |
| 1 | Every section gets a time slot (0 to 7), an instructor and a classroom that exist in the data. | `domain` |
| 2 | No two sections can use the same classroom in the same time slot. | `room_conflict` |
| 3 | No instructor can be assigned to two sections in the same time slot. | `instructor_conflict` |
| 4 | Each section is taught by an instructor who is qualified to teach that course. | `qualification` |
| 5 | No instructor is assigned more sections than their `max_sections` limit: 3 for full-time instructors and 2 for part-time instructors. | `workload` |
| 6 | Each section meets within its allowed time window (`earliest_slot` to `latest_slot`). For example, an evening section must be in slot 6 or 7. | `time_window` |

## Data Files

The data files have already been created for you: [instructors.csv](GroupA-V2-Data/instructors.csv), [classrooms.csv](GroupA-V2-Data/classrooms.csv) and [sections.csv](GroupA-V2-Data/sections.csv). To download all three at once, use this link: [Download the Group A data files as a zip file](https://download-directory.github.io/?url=https://github.com/LCC-CIT/CS212-CourseMaterials/tree/main/docs/Labs/Lab02-ConstraintSolvers/GroupA-V2-Data). Unzip the file and move the three CSV files into your project folder. They have the columns described below. In columns that hold a list, the items are separated with semicolons, for example `CS133Y;CS161;CS162`.

**`instructors.csv`**

| Column | Meaning |
| --- | --- |
| `instructor_id` | A short ID, for example `I01` |
| `name` | Instructor's name |
| `max_sections` | Most sections this instructor can teach: 3 for full-time, 2 for part-time |
| `qualified_courses` | Courses this instructor can teach |

**`classrooms.csv`**

| Column | Meaning |
| --- | --- |
| `room_id` | Room number, for example `BLD19-108` |

**`sections.csv`**

| Column | Meaning |
| --- | --- |
| `section_id` | A short ID, for example `S01` |
| `course` | Course number, for example `CS161` |
| `earliest_slot` | Earliest allowed time slot |
| `latest_slot` | Latest allowed time slot |

## Requirements

1. **Data files.** Download the [zip file of data files](https://download-directory.github.io/?url=https://github.com/LCC-CIT/CS212-CourseMaterials/tree/main/docs/Labs/Lab02-ConstraintSolvers/GroupA-V2-Data), unzip it and put the three CSV files described above in your project folder.
2. **Loading data.** Load each CSV file into a list of dictionaries, for example with `csv.DictReader`. Convert numbers to `int` and split the semicolon lists into Python lists.
3. **Decision variables.** For each section, create three Z3 `Int` variables: its time slot, its instructor (an index into the instructors list) and its classroom (an index into the classrooms list).
4. **Constraints.** Add constraints for all six scheduling rules. You will need these Z3 tools: `And`, `Or`, `Implies`, and `Sum` combined with `If` for counting (rule 5). For rules 2 and 3 you can use either `Implies` on every pair of sections or `Distinct`.
5. **Solving.** Use a Z3 `Solver` to find a schedule. Read the values out of the model and return the schedule as a list of dictionaries. Print the schedule in a readable table sorted by time slot, showing the time, section, course, instructor and classroom.
6. **Explaining an impossible schedule.** Create one Boolean tracking variable per constraint group (the names in the rules table) and add each constraint as `Implies(group_flag, constraint)`. Call `check()` with all the flags as assumptions. When the result is `unsat`, print the names of the groups in `unsat_core()`. Make a folder named `unsolvable_data` with three modified copies of the data files, each of which breaks a different rule. For example: a course that no instructor is qualified to teach, a section whose `earliest_slot` is later than its `latest_slot`, or a course with 3 sections that only one part-time instructor (`max_sections` of 2) is qualified to teach. Your program must report the conflicting groups for each one. Keep each conflict small. Proving that no solution exists can take Z3 a very long time, and in testing for this lab, a larger version of the last example (14 sections of a course for 13 openings) timed out instead of returning `unsat`.
7. **Separation of concerns.** Keep the Z3 model and solving code in its own module, separate from file loading and from user input and output.
8. **Testing.** Write a test module with a function that checks a schedule against all six rules in plain Python, without using Z3. Use it to test that:
   - the schedule from your real data passes every rule,
   - each data set in `unsolvable_data` is reported as `unsat` with the expected constraint group in the core,
   - the checker itself catches a schedule that you broke on purpose, for example by moving two sections into the same classroom at the same time.

> **Example: a simple test driver**
>
> You don't need a testing framework for requirement 8. Write each test as a function that uses `assert`, which stops the function with an `AssertionError` if its condition is `False`. Then write a short "test driver" loop that calls each test function and reports whether it passed.
>
> This small example tests a checker for one rule, using two hand-made schedules:
>
> ```python
> # A checker for one rule, written in plain Python (no Z3)
> def has_room_conflict(schedule):
>     """Return True if two sections are in the same room in the same time slot."""
>     for j in range(len(schedule)):
>         for k in range(j):
>             if (schedule[j]["slot"] == schedule[k]["slot"]
>                     and schedule[j]["room_id"] == schedule[k]["room_id"]):
>                 return True
>     return False
> 
> # Each test is a function. assert stops the test with an error if its condition is False.
> def test_good_schedule_has_no_room_conflict():
>     schedule = [
>         {"section_id": "S01", "slot": 0, "room_id": "BLD19-108"},
>         {"section_id": "S02", "slot": 0, "room_id": "BLD19-110"},
>     ]
>     assert not has_room_conflict(schedule)
> 
> def test_room_conflict_is_caught():
>     schedule = [
>         {"section_id": "S01", "slot": 0, "room_id": "BLD19-108"},
>         {"section_id": "S02", "slot": 0, "room_id": "BLD19-108"},    # same room and slot
>     ]
>     assert has_room_conflict(schedule)
> 
> # The test driver: run each test function and report whether it passed
> tests = [test_good_schedule_has_no_room_conflict, test_room_conflict_is_caught]
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
> PASS: test_good_schedule_has_no_room_conflict
> PASS: test_room_conflict_is_caught
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
# for example {"section_id": "S01", "course": "CS133Y", ...}
def load_csv(filename):
    rows = []
    with open(filename, newline="") as file:    # "with" closes the file when done
        reader = csv.DictReader(file)
        for row in reader:
            rows.append(row)
    return rows

instructors = load_csv("instructors.csv")
classrooms = load_csv("classrooms.csv")
sections = load_csv("sections.csv")

# Every value is read as a string, so convert the numbers to int
# and split the semicolon lists into Python lists
for teacher in instructors:
    teacher["max_sections"] = int(teacher["max_sections"])
    teacher["qualified_courses"] = teacher["qualified_courses"].split(";")
for section in sections:
    section["earliest_slot"] = int(section["earliest_slot"])
    section["latest_slot"] = int(section["latest_slot"])

# One set of decision variables per section (requirement 3)
slot = []
instructor = []
room = []
for section in sections:
    section_id = section["section_id"]
    slot.append(Int("slot_" + section_id))
    instructor.append(Int("instructor_" + section_id))
    room.append(Int("room_" + section_id))

# One tracking flag per constraint group (requirement 6)
group_names = ["domain", "room_conflict", "instructor_conflict", "qualification",
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
#       domain, room_conflict, instructor_conflict, qualification and time_window

# Counting with Sum and If (rule 5)
# If(condition, 1, 0) works like the ternary operator: condition ? 1 : 0
for w in range(len(instructors)):
    terms = []
    for j in range(len(sections)):
        terms.append(If(instructor[j] == w, 1, 0))
    count = Sum(terms)
    add("workload", count <= instructors[w]["max_sections"])

result = solver.check(flag_list)    # the flags are passed in as assumptions
if result == sat:
    model = solver.model()
    # Read a value from the model and convert it to a Python int
    first_slot = model.eval(slot[0], model_completion=True).as_long()
    # TODO: Read every section's slot, instructor and room out of the model,
    #       return the schedule as a list of dictionaries and print it
    #       as a table sorted by time slot (requirement 5)
elif result == unsat:
    print("Conflicting rules:", solver.unsat_core())
# TODO: Handle the case where result is unknown (the solver timed out)

# TODO: Run the program on each data set in the unsolvable_data folder (requirement 6)
# TODO: Write the test module with a plain Python schedule checker (requirement 8)
```

## Optional Challenges

**Challenge 1: Classroom capacity and instructor availability.** Make the problem more realistic by adding two more rules:

| # | Rule | Constraint group name |
| --- | --- | --- |
| 7 | Each section is in a classroom with at least as many seats as the section's enrollment. | `capacity` |
| 8 | No instructor is scheduled in a time slot listed as unavailable for them. | `availability` |

The data files you were given don't have this information, so you will need to refactor them. Add these columns and fill in values for every row:

| File | Column | Meaning |
| --- | --- | --- |
| `classrooms.csv` | `seats` | Number of seats |
| `sections.csv` | `enrollment` | Number of students enrolled |
| `instructors.csv` | `unavailable_slots` | Time slots this instructor can't teach, for example `0;7` |

Your data should meet these extra requirements:

- The 5 classrooms have different numbers of seats, and at least 2 sections are too big for every classroom except the largest one.
- Each instructor has 1 or 2 unavailable time slots.

If Z3 says your data has no solution, that's not necessarily a bug in your code. Use the unsat core to find out which rules conflict, then adjust your data.

Update your loading code for the new columns, add the two new groups to your tracking flags, add a data set to `unsolvable_data` that breaks each new rule (for example, a section with more students than the largest classroom holds), and update your checker and tests to cover all eight rules.

**Challenge 2: Minimizing part-time sections.** The department would rather give its full-time instructors a full load than rely on part-time instructors. Find a schedule that has as few sections taught by part-time instructors as possible, and print that number and the schedule that goes with it.

First, count the sections taught by part-time instructors. This uses `Sum` and `If` like the workload counting in the Z3 tips, with one `If` for each section:

```python
part_time_terms = []
for j in range(len(sections)):
    # A list of conditions: "section j is taught by part-time instructor w"
    taught_by_part_time = []
    for w in range(len(instructors)):
        if instructors[w]["max_sections"] == 2:    # part-time
            taught_by_part_time.append(instructor[j] == w)
    # Count 1 if any of those conditions is true
    part_time_terms.append(If(Or(taught_by_part_time), 1, 0))
part_time_sections = Sum(part_time_terms)
```

The full-time instructors can teach at most 6 × 3 = 18 sections, so at least 24 − 18 = 6 sections must go to part-time instructors. That makes 6 the lowest possible value. Proving that no solution exists can take Z3 much longer than finding one, so both approaches below use 6 as a lower bound instead of asking Z3 to prove that 5 is impossible.

Choose one of these two approaches. If you have time, try both and compare them.

**Option A: A loop with `push()` and `pop()`.** Keep using your `Solver`. In a loop, add a constraint that `part_time_sections` is at most *k*, check, then lower *k* and try again. Stop when the check is `unsat` or `unknown`, or when *k* reaches 6.

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
> Read the value out of the model before calling `pop()`, because the model belongs to that check. In this challenge, the limit is on `part_time_sections` instead of on `x`.

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

optimizer.add(part_time_sections >= 6)    # the lower bound
optimizer.minimize(part_time_sections)

if optimizer.check() == sat:
    model = optimizer.model()
    print("Part-time sections:", model.eval(part_time_sections))    # Part-time sections: 6
```

- **Pros:** It takes only a few lines of code, and Z3 does the searching for you.
- **Cons:** It's all or nothing: if the check times out, you may not get a schedule at all. It can be much slower than finding a single schedule. In testing for this lab, it took about 7 times longer without the lower bound, and on this kind of problem it sometimes returned wrong answers without one. It's also sensitive to how the count is written: with a separate `If` for every section and part-time instructor pair, instead of one `If` per section as shown above, it timed out. Your model code must be able to add constraints to an `Optimize` object as well as a `Solver`.

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



*These instructions were drafted by Claude Sonnet 5.5, simplified by Claude Opus 5.5 and reviewed and revised by Brian Bird.*
