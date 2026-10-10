---
title: Lab 2, Group B
description: Group B assignment to use the Z3 constraint solver to schedule flights, aircraft and flight crews (simplified version)
keywords: constraint solver, Z3, scheduling, constraint satisfaction, unsat core, CSV files, testing
material: Lab Instructions
generator: Typora
author: Brian Bird
---

<h1>Lab 2, Scheduling with a Constraint Solver</h1>

<h2>Group B</h2>

**CS 212, AI Programming 1**

<h2>Contents</h2>

[TOC]

## Scheduling a Small Airline

Every day, a small regional airline has to decide when each flight departs, which aircraft flies it and which crew works it. Doing this by hand is slow and it's easy to create conflicts, such as one crew assigned to two flights at once.

In this lab you will write a Python program that uses the Z3 constraint solver to build the schedule. You won't write a search algorithm. Instead, you will describe what a valid schedule looks like, as constraints, and Z3 will find one.

## The Problem

The airline operates 24 flights a day with 10 flight crews and 5 aircraft. Each flight departs in one of 8 departure slots.

| What | How many | Data file |
| --- | --- | --- |
| Flights | 24 | `flights.csv` |
| Flight crews | 10 (6 regular, 4 reserve) | `crews.csv` |
| Aircraft | 5 | `aircraft.csv` |
| Departure slots | 8 (numbered 0 to 7) | none, the slots are fixed (see below) |

Each departure slot is a 2 hour block. Every flight is a short round trip that takes less than 2 hours, so the aircraft and crew are free again at the start of the next slot.

| Slot | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Time | 6:00 am | 8:00 am | 10:00 am | 12:00 pm | 2:00 pm | 4:00 pm | 6:00 pm | 8:00 pm |

To keep the problem manageable, every flight takes exactly one time slot, there are no connecting flights, every aircraft is big enough for every flight, and every crew can work in any time slot.

### Scheduling Rules

A valid schedule must follow all of these rules. Each rule will become a group of constraints in your program.

| # | Rule | Constraint group name |
| --- | --- | --- |
| 1 | Every flight gets a time slot (0 to 7), a crew and an aircraft that exist in the data. | `domain` |
| 2 | No two flights can use the same aircraft in the same time slot. | `aircraft_conflict` |
| 3 | No crew can be assigned to two flights in the same time slot. | `crew_conflict` |
| 4 | Each flight is worked by a crew that is qualified for the flight's destination. Some airports, such as mountain or short-runway airports, need special training. | `qualification` |
| 5 | No crew is assigned more flights than their `max_flights` limit: 3 for regular crews and 2 for reserve crews. | `workload` |
| 6 | Each flight departs within its allowed time window (`earliest_slot` to `latest_slot`). For example, a business commuter flight must depart in slot 0 or 1. | `time_window` |

## Data Files

The data files have already been created for you: [crews.csv](GroupB-V2-Data/crews.csv), [aircraft.csv](GroupB-V2-Data/aircraft.csv) and [flights.csv](GroupB-V2-Data/flights.csv). To download all three at once, use this link: [Download the Group B data files as a zip file](https://download-directory.github.io/?url=https://github.com/LCC-CIT/CS212-CourseMaterials/tree/main/docs/Labs/Lab02-ConstraintSolvers/GroupB-V2-Data). Unzip the file and put the three CSV files in a folder named `Data` inside your project folder. They have the columns described below. In columns that hold a list, the items are separated with semicolons, for example `PDX;BOI;SUN`.

**`crews.csv`**

| Column | Meaning |
| --- | --- |
| `crew_id` | A short ID, for example `C01` |
| `captain` | Captain's name |
| `max_flights` | Most flights this crew can work in a day: 3 for regular crews, 2 for reserve crews |
| `qualified_destinations` | Airport codes this crew is qualified to fly to |

**`aircraft.csv`**

| Column | Meaning |
| --- | --- |
| `tail_number` | Aircraft registration, for example `N412LC` |

**`flights.csv`**

| Column | Meaning |
| --- | --- |
| `flight_number` | Flight number, for example `LC101` |
| `destination` | Airport code, for example `PDX` |
| `earliest_slot` | Earliest allowed departure slot |
| `latest_slot` | Latest allowed departure slot |

## Requirements

1. **Data files.** Download the [zip file of data files](https://download-directory.github.io/?url=https://github.com/LCC-CIT/CS212-CourseMaterials/tree/main/docs/Labs/Lab02-ConstraintSolvers/GroupB-V2-Data), unzip it and put the three CSV files described above in a folder named `Data` inside your project folder. When your program opens a file using a relative path such as `Data/crews.csv`, Python starts looking in the folder where the program is *running* (the current working directory), not the folder that holds the `.py` file. So run your program, for example with `uv run main.py`, from your project folder, the one that contains `Data`.
2. **Loading data.** Load each CSV file into a list of dictionaries, for example with `csv.DictReader`. Convert numbers to `int` and split the semicolon lists into Python lists.
3. **Decision variables.** For each flight, create three Z3 `Int` variables: its time slot, its crew (an index into the crews list) and its aircraft (an index into the aircraft list).
4. **Constraints.** Add constraints for all six scheduling rules. You will need these Z3 tools: `And`, `Or`, `Implies`, and `Sum` combined with `If` for counting (rule 5). For rules 2 and 3 you can use either `Implies` on every pair of flights or `Distinct`.
5. **Solving.** Use a Z3 `Solver` to find a schedule. Read the values out of the model and return the schedule as a list of dictionaries. Print the schedule in a readable table sorted by time slot, showing the departure time, flight number, destination, crew and aircraft.
6. **Explaining an impossible schedule.** Sometimes no schedule can follow all the rules at once. When that happens, your program should report which rules conflict.

   - Add code to do these things:

     - Create one tracking flag for each constraint group (the names in the rules table). A flag is a Z3 `Bool`, a variable that is either true or false. It works like a switch that turns its group of constraints on.

     - Add each constraint as `Implies(group_flag, constraint)`. `Implies(a, b)` means "if `a` is true, then `b` must be true," so a constraint only applies when its flag is on.

     - Call `check()` with all the flags as *assumptions*. An assumption is a flag that Z3 treats as true for that one check, so every group of constraints is turned on.

     - When the result is `unsat` (short for "unsatisfiable," which means Z3 has proved that no solution exists), print the names of the groups in `unsat_core()`. The *unsat core* is a set of flags whose constraint groups can't all be met at the same time.

   - Make a folder named `unsolvable_data` inside your `Data` folder, with three modified copies of the data files, each of which breaks a different rule. For example: a destination that no crew is qualified for, a flight whose `earliest_slot` is later than its `latest_slot`, or a destination with 3 flights that only one reserve crew (`max_flights` of 2) is qualified for.

   - Your program must report the conflicting groups for each unsolvable data file.

   - Hint: keep each conflict small. Proving that no solution exists can take Z3 a very long time. In testing earlier versions of this lab, a larger version of the last example (14 flights to one destination for 13 openings) ran past the time limit and returned `unknown` instead of `unsat`.

7. **Separation of concerns.** Keep the Z3 model and solving code in its own module, separate from file loading and from user input and output.
8. **Testing.** Write a test module with a function that checks a schedule against all six rules in plain Python, without using Z3. Use it to test that:
   - the schedule from your real data passes every rule,
   - each data set in `unsolvable_data` is reported as `unsat` with the expected constraint group in the core,
   - the checker itself catches a schedule that you broke on purpose, for example by putting two flights on the same aircraft at the same time.

> **Example: a simple test driver**
>
> You don't need a testing framework for requirement 8. Write each test as a function that uses `assert`, which stops the function with an `AssertionError` if its condition is `False`. Then write a short "test driver" loop that calls each test function and reports whether it passed.
>
> This small example tests a checker for one rule, using two hand-made schedules:
>
> ```python
> # A checker for one rule, written in plain Python (no Z3)
> def has_aircraft_conflict(schedule):
>     """Return True if two flights use the same aircraft in the same time slot."""
>     for j in range(len(schedule)):
>         for k in range(j):
>             if (schedule[j]["slot"] == schedule[k]["slot"]
>                     and schedule[j]["tail_number"] == schedule[k]["tail_number"]):
>                 return True
>     return False
> 
> # Each test is a function. assert stops the test with an error if its condition is False.
> def test_good_schedule_has_no_aircraft_conflict():
>     schedule = [
>         {"flight_number": "LC101", "slot": 0, "tail_number": "N412LC"},
>         {"flight_number": "LC102", "slot": 0, "tail_number": "N415LC"},
>     ]
>     assert not has_aircraft_conflict(schedule)
> 
> def test_aircraft_conflict_is_caught():
>     schedule = [
>         {"flight_number": "LC101", "slot": 0, "tail_number": "N412LC"},
>         {"flight_number": "LC102", "slot": 0, "tail_number": "N412LC"},    # same aircraft and slot
>     ]
>     assert has_aircraft_conflict(schedule)
> 
> # The test driver: run each test function and report whether it passed
> tests = [test_good_schedule_has_no_aircraft_conflict, test_aircraft_conflict_is_caught]
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
> PASS: test_good_schedule_has_no_aircraft_conflict
> PASS: test_aircraft_conflict_is_caught
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
# for example {"flight_number": "LC101", "destination": "PDX", ...}
def load_csv(filename):
    rows = []
    with open(filename, newline="") as file:    # "with" closes the file when done
        reader = csv.DictReader(file)
        for row in reader:
            rows.append(row)
    return rows

crews = load_csv("Data/crews.csv")
aircraft = load_csv("Data/aircraft.csv")
flights = load_csv("Data/flights.csv")

# Every value is read as a string, so convert the numbers to int
# and split the semicolon lists into Python lists
for crew_info in crews:
    crew_info["max_flights"] = int(crew_info["max_flights"])
    crew_info["qualified_destinations"] = crew_info["qualified_destinations"].split(";")
for flight in flights:
    flight["earliest_slot"] = int(flight["earliest_slot"])
    flight["latest_slot"] = int(flight["latest_slot"])

# One set of decision variables per flight (requirement 3)
slot = []
crew = []
plane = []
for flight in flights:
    flight_id = flight["flight_number"]
    slot.append(Int("slot_" + flight_id))
    crew.append(Int("crew_" + flight_id))
    plane.append(Int("plane_" + flight_id))

# One tracking flag per constraint group (requirement 6)
group_names = ["domain", "aircraft_conflict", "crew_conflict", "qualification",
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
#       domain, aircraft_conflict, crew_conflict, qualification and time_window

# Counting with Sum and If (rule 5)
# If(condition, 1, 0) works like the ternary operator: condition ? 1 : 0
for w in range(len(crews)):
    terms = []
    for j in range(len(flights)):
        terms.append(If(crew[j] == w, 1, 0))
    count = Sum(terms)
    add("workload", count <= crews[w]["max_flights"])

result = solver.check(flag_list)    # the flags are passed in as assumptions
if result == sat:
    model = solver.model()
    # Read a value from the model and convert it to a Python int
    first_slot = model.eval(slot[0], model_completion=True).as_long()
    # TODO: Read every flight's slot, crew and aircraft out of the model,
    #       return the schedule as a list of dictionaries and print it
    #       as a table sorted by time slot (requirement 5)
elif result == unsat:
    print("Conflicting rules:", solver.unsat_core())
# TODO: Handle the case where result is unknown (the solver timed out)

# TODO: Run the program on each data set in the unsolvable_data folder (requirement 6)
# TODO: Write the test module with a plain Python schedule checker (requirement 8)
```

## Optional Challenges

**Challenge 1: Aircraft capacity and crew availability.** Make the problem more realistic by adding two more rules:

| # | Rule | Constraint group name |
| --- | --- | --- |
| 7 | Each flight uses an aircraft with at least as many seats as the flight's booked passengers. | `capacity` |
| 8 | No crew is scheduled in a time slot listed as unavailable for them. | `availability` |

The data files you were given don't have this information, so you will need to refactor them. Add these columns and fill in values for every row:

| File | Column | Meaning |
| --- | --- | --- |
| `aircraft.csv` | `seats` | Number of passenger seats |
| `flights.csv` | `passengers` | Number of passengers booked |
| `crews.csv` | `unavailable_slots` | Departure slots this crew can't work (required rest), for example `0;1` |

Your data should meet these extra requirements:

- The 5 aircraft have different numbers of seats, and at least 2 flights are too big for every aircraft except the largest one.
- Each crew has 1 or 2 unavailable time slots.

If Z3 says your data has no solution, that's not necessarily a bug in your code. Use the unsat core to find out which rules conflict, then adjust your data.

Update your loading code for the new columns, add the two new groups to your tracking flags, add a data set to `unsolvable_data` that breaks each new rule (for example, a flight with more passengers than the largest aircraft holds), and update your checker and tests to cover all eight rules.

**Challenge 2: Minimizing reserve crew flights.** Reserve crews are on call for emergencies, so the airline would rather have its regular crews work as many flights as possible. Find a schedule that has as few flights worked by reserve crews as possible, and print that number and the schedule that goes with it.

First, count the flights worked by reserve crews. This uses `Sum` and `If` like the workload counting in the Z3 tips, with one `If` for each flight:

```python
reserve_terms = []
for j in range(len(flights)):
    # A list of conditions: "flight j is worked by reserve crew w"
    worked_by_reserve = []
    for w in range(len(crews)):
        if crews[w]["max_flights"] == 2:    # reserve crew
            worked_by_reserve.append(crew[j] == w)
    # Count 1 if any of those conditions is true
    reserve_terms.append(If(Or(worked_by_reserve), 1, 0))
reserve_flights = Sum(reserve_terms)
```

The regular crews can work at most 6 × 3 = 18 flights, so at least 24 − 18 = 6 flights must go to reserve crews. That makes 6 the lowest possible value. Proving that no solution exists can take Z3 much longer than finding one, so both approaches below use 6 as a lower bound instead of asking Z3 to prove that 5 is impossible.

Choose one of these two approaches. If you have time, try both and compare them.

**Option A: A loop with `push()` and `pop()`.** Keep using your `Solver`. In a loop, add a constraint that `reserve_flights` is at most *k*, check, then lower *k* and try again. Stop when the check is `unsat` or `unknown`, or when *k* goes below the lower bound (6).

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
> Read the value out of the model before calling `pop()`, because the model belongs to that check. In this challenge, the limit is on `reserve_flights` instead of on `x`.

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

optimizer.add(reserve_flights >= 6)    # the lower bound
optimizer.minimize(reserve_flights)

if optimizer.check() == sat:
    model = optimizer.model()
    print("Reserve crew flights:", model.eval(reserve_flights))    # Reserve crew flights: 6
```

- **Pros:** It takes only a few lines of code, and Z3 does the searching for you.
- **Cons:** It's all or nothing: if the check times out, you may not get a schedule at all. It can be much slower than finding a single schedule. In testing for this lab, it took about 6 times longer without the lower bound, and on this kind of problem it sometimes returned wrong answers without one. It's also sensitive to how the count is written: with a separate `If` for every flight and reserve crew pair, instead of one `If` per flight as shown above, it timed out. That's why the code that adds your constraints should go through one function that only calls `add()`, so it can add constraints to an `Optimize` object as well as a `Solver`.

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
