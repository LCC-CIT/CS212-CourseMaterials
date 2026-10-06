---
title: Lab 2, Group B
description: Group B assignment to use the Z3 constraint solver to schedule flights, aircraft and flight crews
keywords: constraint solver, Z3, scheduling, constraint satisfaction, unsat core, CSV files, testing
material: Lab Instructions
generator: Typora
author: Brian Bird
---

<h1>Lab 2, Scheduling with a Constraint Solver</h1>

<h2>Group B</h2>

**CS 212, AI Programming 1**

## Scheduling a Small Airline

Every day, a small regional airline has to decide when each flight departs, which aircraft flies it and which crew works it. Doing this by hand is slow and it's easy to create conflicts, such as one crew assigned to two flights at once.

In this lab you will write a Python program that uses the Z3 constraint solver to build the schedule. You won't write a search algorithm. Instead, you will describe what a valid schedule looks like, as constraints, and Z3 will find one.

## The Problem

The airline operates 30 flights a day with 10 flight crews and 5 aircraft. Each flight departs in one of 8 departure slots.

| What | How many | Data file |
| --- | --- | --- |
| Flights | 30 | `flights.csv` |
| Flight crews | 10 | `crews.csv` |
| Aircraft | 5 | `aircraft.csv` |
| Departure slots | 8 (numbered 0 to 7) | none, the slots are fixed (see below) |
| Connecting flight pairs | 4 | `connections.csv` |

Each departure slot is a 2 hour block. Every flight is a short round trip that takes less than 2 hours, so the aircraft and crew are free again at the start of the next slot.

| Slot | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Time | 6:00 am | 8:00 am | 10:00 am | 12:00 pm | 2:00 pm | 4:00 pm | 6:00 pm | 8:00 pm |

To keep the problem manageable, every flight takes exactly one time slot.

### Scheduling Rules

A valid schedule must follow all of these rules. Each rule will become a group of constraints in your program.

| # | Rule | Constraint group name |
| --- | --- | --- |
| 1 | Every flight gets a time slot (0 to 7), a crew and an aircraft that exist in the data. | `domain` |
| 2 | No two flights can use the same aircraft in the same time slot. | `aircraft_conflict` |
| 3 | No crew can be assigned to two flights in the same time slot. | `crew_conflict` |
| 4 | Each flight is worked by a crew that is qualified for the flight's destination. Some airports, such as mountain or short-runway airports, need special training. | `qualification` |
| 5 | Each flight uses an aircraft with at least as many seats as the flight's booked passengers. | `capacity` |
| 6 | No crew is scheduled in a time slot listed as unavailable for them. | `availability` |
| 7 | No crew is assigned more flights than their `max_flights` limit. | `workload` |
| 8 | Each flight departs within its allowed time window (`earliest_slot` to `latest_slot`). For example, a business commuter flight must depart in slot 0 or 1. | `time_window` |
| 9 | For each connecting flight pair, the second flight departs at least one slot after the first, so passengers can make the connection. | `ordering` |

## Data Files

You will create the data files yourself. Use these columns. In columns that hold a list, separate the items with semicolons, for example `EUG;PDX;SUN`.

**`crews.csv`**

| Column | Meaning |
| --- | --- |
| `crew_id` | A short ID, for example `C01` |
| `captain` | Captain's name |
| `max_flights` | Most flights this crew can work in a day |
| `unavailable_slots` | Departure slots this crew can't work (required rest), for example `0;1` |
| `qualified_destinations` | Airport codes this crew is qualified to fly to |

**`aircraft.csv`**

| Column | Meaning |
| --- | --- |
| `tail_number` | Aircraft registration, for example `N412LC` |
| `seats` | Number of passenger seats |

**`flights.csv`**

| Column | Meaning |
| --- | --- |
| `flight_number` | Flight number, for example `LC101` |
| `destination` | Airport code, for example `PDX` |
| `passengers` | Number of passengers booked |
| `earliest_slot` | Earliest allowed departure slot |
| `latest_slot` | Latest allowed departure slot |

**`connections.csv`**

| Column | Meaning |
| --- | --- |
| `first_flight` | The flight passengers arrive on |
| `second_flight` | The connecting flight that must depart later |

Your data must meet these requirements so that it is realistic and the problem is not too easy:

- Use exactly 30 flights, 10 crews and 5 aircraft.
- There are 6 different destinations. Every crew is qualified for 3 or 4 of them, and every destination has at least 4 qualified crews.
- Each crew has a `max_flights` of 3 or 4.
- Each crew has 1 or 2 unavailable time slots.
- The 5 aircraft have different numbers of seats, and at least 2 flights are too big for every aircraft except the largest one.
- At least 10 flights have a time window narrower than 0 to 7.
- `connections.csv` lists 4 pairs of flights, and the pairs don't share any flights.

If Z3 says your data has no solution, that's not necessarily a bug in your code. Use the unsat core (requirement 7) to find out which rules conflict, then adjust your data.

## Requirements

1. **Data files.** Create the four CSV files described above.
2. **Loading data.** Load each CSV file into a list of dictionaries, for example with `csv.DictReader`. Convert numbers to `int` and split the semicolon lists into Python lists.
3. **Decision variables.** For each flight, create three Z3 `Int` variables: its time slot, its crew (an index into the crews list) and its aircraft (an index into the aircraft list).
4. **Constraints.** Add constraints for all nine scheduling rules. You will need these Z3 tools: `And`, `Or`, `Not`, `Implies`, and `Sum` combined with `If` for counting (rule 7). For rules 2 and 3 you can use either `Implies` on every pair of flights or `Distinct`.
5. **Solving.** Use a Z3 `Solver` to find a schedule. Read the values out of the model and return the schedule as a list of dictionaries. Print the schedule in a readable table sorted by time slot, showing the departure time, flight number, destination, crew and aircraft.
6. **Improving the schedule.** Balance the workload so that no crew gets many more flights than the others. Use a loop with `push()` and `pop()`: add a constraint that every crew has at most *k* flights, check, then lower *k* and try again. Stop when the check is `unsat` or `unknown`, or when *k* reaches the lowest possible value, which is 30 ÷ 10 = 3. Set a timeout on the solver so that a single check can't run forever. Print the best *k* you found and the schedule that goes with it.
7. **Explaining an impossible schedule.** Create one Boolean tracking variable per constraint group (the names in the rules table) and add each constraint as `Implies(group_flag, constraint)`. Call `check()` with all the flags as assumptions. When the result is `unsat`, print the names of the groups in `unsat_core()`. Make a folder named `bad_data` with three variations of your data, each of which breaks a different rule. For example: a flight with more passengers than the largest aircraft holds, a connecting flight whose time window ends before the first flight's window starts, or a destination that no available crew is qualified for. Your program must report the conflicting groups for each one.
8. **Separation of concerns.** Keep the Z3 model and solving code in its own module, separate from file loading and from user input and output.
9. **Testing.** Write a test module with a function that checks a schedule against all nine rules in plain Python, without using Z3. Use it to test that:
   - the schedule from your real data passes every rule,
   - each data set in `bad_data` is reported as `unsat` with the expected constraint group in the core,
   - the checker itself catches a schedule that you broke on purpose, for example by moving two flights into the same aircraft at the same time.

## Z3 Tips

These snippets show the pattern for this problem. Your code will need more than this.

```python
from z3 import Solver, Int, Bool, And, Or, Implies, Sum, If, sat, unsat

# One set of decision variables per flight (requirement 3)
slot = []
crew = []
plane = []
for flight in flights:
    flight_id = flight["flight_number"]
    slot.append(Int("slot_" + flight_id))
    crew.append(Int("crew_" + flight_id))
    plane.append(Int("plane_" + flight_id))

# One tracking flag per constraint group (requirement 7)
group_names = ["domain", "aircraft_conflict", "crew_conflict", "qualification",
               "capacity", "availability", "workload", "time_window", "ordering"]
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

# Counting with Sum and If (rule 7)
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
elif result == unsat:
    print("Conflicting rules:", solver.unsat_core())
```

Proving that no solution exists can take Z3 much longer than finding one. That's why requirement 6 stops at the lower bound of 3 instead of asking Z3 to prove that 2 is impossible.

**Optional challenge:** Z3 also has an `Optimize` class with a `minimize()` method. Try it on the workload problem and compare it with your `push()`/`pop()` loop. If you do, give the objective variable a lower bound, for example `max_load >= 3`. In testing for this lab, without a lower bound Z3's optimizer sometimes returned wrong or very slow answers on this kind of problem.

## Submitting your lab work on Canvas

### Beta Version

- Post the beta version of your program to your team channel in Discord.

### Code Review

- Review one of your lab partners' code and post the review in your team channel on Discord.
- Submit a copy of the code review <u>you did</u> to the code review assignment on Canvas.

### Production Version

 Based on the code review and helpful advice from your lab partners, you may revise your code. On the code review from your lab partner, complete the “Prod.” column to show what you revised. Upload the following to the *Lab Production Version* assignment on Canvas:

1. The files: Python (.py) files (one or more) and the .csv data files, including the `bad_data` folder.
2. The code review <u>from your lab partner</u> with the “Prod.” column filled out by you.

### Grading Criteria

The main focus of grading will be on how you model the problem as constraints and on testing.



*These instructions were drafted by Claude Sonnet 5.5 and have been reviewed and minimally revised by a human.*
