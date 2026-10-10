---
title: Lab 2, Group C
description: Group C assignment to use the Z3 constraint solver to schedule deliveries, drivers and delivery vans (simplified version)
keywords: constraint solver, Z3, scheduling, constraint satisfaction, unsat core, CSV files, testing
material: Lab Instructions
generator: Typora
author: Brian Bird
---

<h1>Lab 2, Scheduling with a Constraint Solver</h1>

<h2>Group C</h2>

**CS 212, AI Programming 1**

<h2>Contents</h2>

[TOC]

## Scheduling Package Deliveries

Every day, a delivery company that handles large packages such as appliances and furniture has to decide when each delivery happens, which driver makes it and which van carries it. Doing this by hand is slow and it's easy to create conflicts, such as one van sent to two customers at once.

In this lab you will write a Python program that uses the Z3 constraint solver to build the schedule. You won't write a search algorithm. Instead, you will describe what a valid schedule looks like, as constraints, and Z3 will find one.

## The Problem

The company has 24 deliveries to make in one day, with 10 drivers and 5 delivery vans. Each delivery happens in one of 8 delivery windows.

| What | How many | Data file |
| --- | --- | --- |
| Deliveries | 24 | `deliveries.csv` |
| Drivers | 10 (6 full-time, 4 part-time) | `drivers.csv` |
| Delivery vans | 5 | `vans.csv` |
| Delivery windows | 8 (numbered 0 to 7) | none, the slots are fixed (see below) |

Each delivery window is one hour. Every delivery, including the drive, unloading and any setup, fits in one window, so the van and driver are free again at the start of the next window.

| Slot | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Time | 8:00 am | 9:00 am | 10:00 am | 11:00 am | 12:00 pm | 1:00 pm | 2:00 pm | 3:00 pm |

To keep the problem manageable, every delivery takes exactly one time slot, there are no linked deliveries that must happen in order, every van is big enough for every delivery, and every driver can work in any time slot.

### Scheduling Rules

A valid schedule must follow all of these rules. Each rule will become a group of constraints in your program.

| # | Rule | Constraint group name |
| --- | --- | --- |
| 1 | Every delivery gets a time slot (0 to 7), a driver and a van that exist in the data. | `domain` |
| 2 | No two deliveries can use the same van in the same time slot. | `van_conflict` |
| 3 | No driver can be assigned to two deliveries in the same time slot. | `driver_conflict` |
| 4 | Each delivery is made by a driver who has the skill the delivery needs, for example appliance installation or furniture assembly. | `qualification` |
| 5 | No driver is assigned more deliveries than their `max_deliveries` limit: 3 for full-time drivers and 2 for part-time drivers. | `workload` |
| 6 | Each delivery happens within the customer's requested time window (`earliest_slot` to `latest_slot`). For example, a customer who works afternoons wants slot 0, 1 or 2. | `time_window` |

## Data Files

The data files have already been created for you: [drivers.csv](GroupC-V2-Data/drivers.csv), [vans.csv](GroupC-V2-Data/vans.csv) and [deliveries.csv](GroupC-V2-Data/deliveries.csv). To download all three at once, use this link: [Download the Group C data files as a zip file](https://download-directory.github.io/?url=https://github.com/LCC-CIT/CS212-CourseMaterials/tree/main/docs/Labs/Lab02-ConstraintSolvers/GroupC-V2-Data). Unzip the file and move the three CSV files into your project folder. They have the columns described below. In columns that hold a list, the items are separated with semicolons, for example `appliance;furniture;assembly`.

**`drivers.csv`**

| Column | Meaning |
| --- | --- |
| `driver_id` | A short ID, for example `D01` |
| `name` | Driver's name |
| `max_deliveries` | Most deliveries this driver can make in a day: 3 for full-time, 2 for part-time |
| `skills` | Skills this driver has |

**`vans.csv`**

| Column | Meaning |
| --- | --- |
| `van_id` | A short ID, for example `V1` |

**`deliveries.csv`**

| Column | Meaning |
| --- | --- |
| `delivery_id` | A short ID, for example `O101` |
| `skill_needed` | The skill this delivery needs, for example `install` |
| `earliest_slot` | Earliest allowed delivery window |
| `latest_slot` | Latest allowed delivery window |

## Requirements

1. **Data files.** Download the [zip file of data files](https://download-directory.github.io/?url=https://github.com/LCC-CIT/CS212-CourseMaterials/tree/main/docs/Labs/Lab02-ConstraintSolvers/GroupC-V2-Data), unzip it and put the three CSV files described above in a folder named `Data` inside your project folder. When your program opens a file using a relative path such as `Data/drivers.csv`, Python starts looking in the folder where the program is *running* (the current working directory), not the folder that holds the `.py` file. So run your program, for example with `uv run main.py`, from your project folder, the one that contains `Data`.
2. **Loading data.** Load each CSV file into a list of dictionaries, for example with `csv.DictReader`. Convert numbers to `int` and split the semicolon lists into Python lists.
3. **Decision variables.** For each delivery, create three Z3 `Int` variables: its time slot, its driver (an index into the drivers list) and its van (an index into the vans list).
4. **Constraints.** Add constraints for all six scheduling rules. You will need these Z3 tools: `And`, `Or`, `Implies`, and `Sum` combined with `If` for counting (rule 5). For rules 2 and 3 you can use either `Implies` on every pair of deliveries or `Distinct`.
5. **Solving.** Use a Z3 `Solver` to find a schedule. Read the values out of the model and return the schedule as a list of dictionaries. Print the schedule in a readable table sorted by time slot, showing the delivery window, delivery ID, skill needed, driver and van.
6. **Explaining an impossible schedule.** Create one Boolean tracking variable per constraint group (the names in the rules table) and add each constraint as `Implies(group_flag, constraint)`. Call `check()` with all the flags as assumptions. When the result is `unsat`, print the names of the groups in `unsat_core()`. Make a folder named `unsolvable_data` inside your `Data` folder, with three modified copies of the data files, each of which breaks a different rule. For example: a skill that no driver has, a delivery whose `earliest_slot` is later than its `latest_slot`, or a skill needed by 3 deliveries that only one part-time driver (`max_deliveries` of 2) has. Your program must report the conflicting groups for each one. Keep each conflict small. Proving that no solution exists can take Z3 a very long time, and in testing for this lab, a larger version of the last example (14 deliveries needing one skill for 13 openings) timed out instead of returning `unsat`.
7. **Separation of concerns.** Keep the Z3 model and solving code in its own module, separate from file loading and from user input and output.
8. **Testing.** Write a test module with a function that checks a schedule against all six rules in plain Python, without using Z3. Use it to test that:
   - the schedule from your real data passes every rule,
   - each data set in `unsolvable_data` is reported as `unsat` with the expected constraint group in the core,
   - the checker itself catches a schedule that you broke on purpose, for example by putting two deliveries in the same van at the same time.

> **Example: a simple test driver**
>
> You don't need a testing framework for requirement 8. Write each test as a function that uses `assert`, which stops the function with an `AssertionError` if its condition is `False`. Then write a short "test driver" loop that calls each test function and reports whether it passed.
>
> This small example tests a checker for one rule, using two hand-made schedules:
>
> ```python
> # A checker for one rule, written in plain Python (no Z3)
> def has_van_conflict(schedule):
>     """Return True if two deliveries use the same van in the same time slot."""
>     for j in range(len(schedule)):
>         for k in range(j):
>             if (schedule[j]["slot"] == schedule[k]["slot"]
>                     and schedule[j]["van_id"] == schedule[k]["van_id"]):
>                 return True
>     return False
> 
> # Each test is a function. assert stops the test with an error if its condition is False.
> def test_good_schedule_has_no_van_conflict():
>     schedule = [
>         {"delivery_id": "O101", "slot": 0, "van_id": "V1"},
>         {"delivery_id": "O102", "slot": 0, "van_id": "V2"},
>     ]
>     assert not has_van_conflict(schedule)
> 
> def test_van_conflict_is_caught():
>     schedule = [
>         {"delivery_id": "O101", "slot": 0, "van_id": "V1"},
>         {"delivery_id": "O102", "slot": 0, "van_id": "V1"},    # same van and slot
>     ]
>     assert has_van_conflict(schedule)
> 
> # The test driver: run each test function and report whether it passed
> tests = [test_good_schedule_has_no_van_conflict, test_van_conflict_is_caught]
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
> PASS: test_good_schedule_has_no_van_conflict
> PASS: test_van_conflict_is_caught
> 2 of 2 tests passed
> ```
>
> The `tests` list holds the functions themselves (no parentheses), so the loop can call each one with `test()`, and `test.__name__` is the function's name. Put your own tests in the list and run the module with `uv run test_scheduler.py`, or whatever you named it. If you already know `pytest`, you can use it instead: it finds and runs functions whose names start with `test_`.

## Z3 Tips

These snippets show the pattern for this problem. Your code will need more than this. In your program, the file loading code goes in its own module (requirement 7). The file paths start with `Data/`, so Python looks for the CSV files in the `Data` folder inside the folder you run the program from.

```python
# TODO: Split this code into modules: file loading, the Z3 model and solving,
#       and user input and output (requirement 7)

import csv
from z3 import Solver, Int, Bool, And, Or, Implies, Sum, If, sat, unsat

# Load a CSV file into a list of dictionaries (requirement 2)
# Each row becomes a dictionary whose keys are the column names,
# for example {"delivery_id": "O101", "skill_needed": "appliance", ...}
def load_csv(filename):
    rows = []
    with open(filename, newline="") as file:    # "with" closes the file when done
        reader = csv.DictReader(file)
        for row in reader:
            rows.append(row)
    return rows

drivers = load_csv("Data/drivers.csv")
vans = load_csv("Data/vans.csv")
deliveries = load_csv("Data/deliveries.csv")

# Every value is read as a string, so convert the numbers to int
# and split the semicolon lists into Python lists
for driver_info in drivers:
    driver_info["max_deliveries"] = int(driver_info["max_deliveries"])
    driver_info["skills"] = driver_info["skills"].split(";")
for delivery in deliveries:
    delivery["earliest_slot"] = int(delivery["earliest_slot"])
    delivery["latest_slot"] = int(delivery["latest_slot"])

# One set of decision variables per delivery (requirement 3)
slot = []
driver = []
van = []
for delivery in deliveries:
    delivery_id = delivery["delivery_id"]
    slot.append(Int("slot_" + delivery_id))
    driver.append(Int("driver_" + delivery_id))
    van.append(Int("van_" + delivery_id))

# One tracking flag per constraint group (requirement 6)
group_names = ["domain", "van_conflict", "driver_conflict", "qualification",
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
#       domain, van_conflict, driver_conflict, qualification and time_window

# Counting with Sum and If (rule 5)
# If(condition, 1, 0) works like the ternary operator: condition ? 1 : 0
for w in range(len(drivers)):
    terms = []
    for j in range(len(deliveries)):
        terms.append(If(driver[j] == w, 1, 0))
    count = Sum(terms)
    add("workload", count <= drivers[w]["max_deliveries"])

result = solver.check(flag_list)    # the flags are passed in as assumptions
if result == sat:
    model = solver.model()
    # Read a value from the model and convert it to a Python int
    first_slot = model.eval(slot[0], model_completion=True).as_long()
    # TODO: Read every delivery's slot, driver and van out of the model,
    #       return the schedule as a list of dictionaries and print it
    #       as a table sorted by time slot (requirement 5)
elif result == unsat:
    print("Conflicting rules:", solver.unsat_core())
# TODO: Handle the case where result is unknown (the solver timed out)

# TODO: Run the program on each data set in the unsolvable_data folder (requirement 6)
# TODO: Write the test module with a plain Python schedule checker (requirement 8)
```

## Optional Challenges

**Challenge 1: Van capacity and driver availability.** Make the problem more realistic by adding two more rules:

| # | Rule | Constraint group name |
| --- | --- | --- |
| 7 | Each delivery is carried in a van with at least as much cargo space (in cubic feet) as the delivery's packages need. | `capacity` |
| 8 | No driver is scheduled in a time slot listed as unavailable for them. | `availability` |

The data files you were given don't have this information, so you will need to refactor them. Add these columns and fill in values for every row:

| File | Column | Meaning |
| --- | --- | --- |
| `vans.csv` | `cargo_cubic_feet` | Cargo space in cubic feet |
| `deliveries.csv` | `cubic_feet` | Cargo space the packages need |
| `drivers.csv` | `unavailable_slots` | Delivery windows this driver can't work (breaks, shift limits), for example `4;7` |

Your data should meet these extra requirements:

- The 5 vans have different amounts of cargo space, and at least 2 deliveries are too big for every van except the largest one.
- Each driver has 1 or 2 unavailable time slots.

If Z3 says your data has no solution, that's not necessarily a bug in your code. Use the unsat core to find out which rules conflict, then adjust your data.

Update your loading code for the new columns, add the two new groups to your tracking flags, add a data set to `unsolvable_data` that breaks each new rule (for example, a delivery bigger than the largest van's cargo space), and update your checker and tests to cover all eight rules.

**Challenge 2: Minimizing part-time deliveries.** The company would rather give its full-time drivers a full day of deliveries than rely on part-time drivers. Find a schedule that has as few deliveries made by part-time drivers as possible, and print that number and the schedule that goes with it.

First, count the deliveries made by part-time drivers. This uses `Sum` and `If` like the workload counting in the Z3 tips, with one `If` for each delivery:

```python
part_time_terms = []
for j in range(len(deliveries)):
    # A list of conditions: "delivery j is made by part-time driver w"
    made_by_part_time = []
    for w in range(len(drivers)):
        if drivers[w]["max_deliveries"] == 2:    # part-time
            made_by_part_time.append(driver[j] == w)
    # Count 1 if any of those conditions is true
    part_time_terms.append(If(Or(made_by_part_time), 1, 0))
part_time_deliveries = Sum(part_time_terms)
```

The full-time drivers can make at most 6 × 3 = 18 deliveries, so at least 24 − 18 = 6 deliveries must go to part-time drivers. That makes 6 the lowest possible value. Proving that no solution exists can take Z3 much longer than finding one, so both approaches below use 6 as a lower bound instead of asking Z3 to prove that 5 is impossible.

Choose one of these two approaches. If you have time, try both and compare them.

**Option A: A loop with `push()` and `pop()`.** Keep using your `Solver`. In a loop, add a constraint that `part_time_deliveries` is at most *k*, check, then lower *k* and try again. Stop when the check is `unsat` or `unknown`, or when *k* reaches 6.

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
> Read the value out of the model before calling `pop()`, because the model belongs to that check. In this challenge, the limit is on `part_time_deliveries` instead of on `x`.

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

optimizer.add(part_time_deliveries >= 6)    # the lower bound
optimizer.minimize(part_time_deliveries)

if optimizer.check() == sat:
    model = optimizer.model()
    print("Part-time deliveries:", model.eval(part_time_deliveries))    # Part-time deliveries: 6
```

- **Pros:** It takes only a few lines of code, and Z3 does the searching for you.
- **Cons:** It's all or nothing: if the check times out, you may not get a schedule at all. It can be much slower than finding a single schedule. In testing for this lab, it took about 10 times longer without the lower bound, and on this kind of problem it sometimes returned wrong answers without one. It's also sensitive to how the count is written: with a separate `If` for every delivery and part-time driver pair, instead of one `If` per delivery as shown above, it timed out. Your model code must be able to add constraints to an `Optimize` object as well as a `Solver`.

## Submitting your lab work on Canvas

### Beta Version

- Post the beta version of your program to your team channel in Discord.

### Code Review

- Review one of your lab partners' code and post the review in your team channel on Discord.
- Submit a copy of the code review <u>you did</u> to the code review assignment on Canvas.

### Production Version

 Based on the code review and helpful advice from your lab partners, you may revise your code. On the code review from your lab partner, complete the “Prod.” column to show what you revised. Upload the following to the *Lab Production Version* assignment on Canvas:

1. The files: Python (.py) files (one or more) and the `unsolvable_data` folder from inside your `Data` folder. If you did Challenge 1, also include your refactored data files.
2. The code review <u>from your lab partner</u> with the “Prod.” column filled out by you.

### Grading Criteria

The main focus of grading will be on how you model the problem as constraints and on testing.



*These instructions were drafted by Claude Sonnet 5.5 and simplified by Claude Opus 5.5.*
