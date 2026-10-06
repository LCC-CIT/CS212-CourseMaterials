---
title: Lab 2, Group C
description: Group C assignment to use the Z3 constraint solver to schedule deliveries, drivers and delivery vans
keywords: constraint solver, Z3, scheduling, constraint satisfaction, unsat core, CSV files, testing
material: Lab Instructions
generator: Typora
author: Brian Bird
---

<h1>Lab 2, Scheduling with a Constraint Solver</h1>

<h2>Group C</h2>

**CS 212, AI Programming 1**

## Scheduling Package Deliveries

Every day, a delivery company that handles large packages such as appliances and furniture has to decide when each delivery happens, which driver makes it and which van carries it. Doing this by hand is slow and it's easy to create conflicts, such as one van sent to two customers at once.

In this lab you will write a Python program that uses the Z3 constraint solver to build the schedule. You won't write a search algorithm. Instead, you will describe what a valid schedule looks like, as constraints, and Z3 will find one.

## The Problem

The company has 30 deliveries to make in one day, with 10 drivers and 5 delivery vans. Each delivery happens in one of 8 delivery windows.

| What | How many | Data file |
| --- | --- | --- |
| Deliveries | 30 | `deliveries.csv` |
| Drivers | 10 | `drivers.csv` |
| Delivery vans | 5 | `vans.csv` |
| Delivery windows | 8 (numbered 0 to 7) | none, the slots are fixed (see below) |
| Linked delivery pairs | 4 | `linked_deliveries.csv` |

Each delivery window is one hour. Every delivery, including the drive, unloading and any setup, fits in one window, so the van and driver are free again at the start of the next window.

| Slot | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Time | 8:00 am | 9:00 am | 10:00 am | 11:00 am | 12:00 pm | 1:00 pm | 2:00 pm | 3:00 pm |

To keep the problem manageable, every delivery takes exactly one time slot.

### Scheduling Rules

A valid schedule must follow all of these rules. Each rule will become a group of constraints in your program.

| # | Rule | Constraint group name |
| --- | --- | --- |
| 1 | Every delivery gets a time slot (0 to 7), a driver and a van that exist in the data. | `domain` |
| 2 | No two deliveries can use the same van in the same time slot. | `van_conflict` |
| 3 | No driver can be assigned to two deliveries in the same time slot. | `driver_conflict` |
| 4 | Each delivery is made by a driver who has the skill the delivery needs, for example appliance installation or furniture assembly. | `qualification` |
| 5 | Each delivery is carried in a van with at least as much cargo space (in cubic feet) as the delivery's packages need. | `capacity` |
| 6 | No driver is scheduled in a time slot listed as unavailable for them. | `availability` |
| 7 | No driver is assigned more deliveries than their `max_deliveries` limit. | `workload` |
| 8 | Each delivery happens within the customer's requested time window (`earliest_slot` to `latest_slot`). For example, a customer who works afternoons wants slot 0, 1 or 2. | `time_window` |
| 9 | For each linked delivery pair, the second delivery happens at least one window after the first. For example, a new washer can only be delivered after the old one has been hauled away. | `ordering` |

## Data Files

You will create the data files yourself. Use these columns. In columns that hold a list, separate the items with semicolons, for example `appliance;install;furniture`.

**`drivers.csv`**

| Column | Meaning |
| --- | --- |
| `driver_id` | A short ID, for example `D01` |
| `name` | Driver's name |
| `max_deliveries` | Most deliveries this driver can make in a day |
| `unavailable_slots` | Delivery windows this driver can't work (breaks, shift limits), for example `4;7` |
| `skills` | Skills this driver has |

**`vans.csv`**

| Column | Meaning |
| --- | --- |
| `van_id` | A short ID, for example `V1` |
| `cargo_cubic_feet` | Cargo space in cubic feet |

**`deliveries.csv`**

| Column | Meaning |
| --- | --- |
| `delivery_id` | A short ID, for example `O101` |
| `skill_needed` | The skill this delivery needs, for example `install` |
| `cubic_feet` | Cargo space the packages need |
| `earliest_slot` | Earliest allowed delivery window |
| `latest_slot` | Latest allowed delivery window |

**`linked_deliveries.csv`**

| Column | Meaning |
| --- | --- |
| `first_delivery` | The delivery that must happen first |
| `second_delivery` | The delivery that must happen later |

Your data must meet these requirements so that it is realistic and the problem is not too easy:

- Use exactly 30 deliveries, 10 drivers and 5 vans.
- There are 6 different skills. Every driver is qualified for 3 or 4 of them, and every skill has at least 4 qualified drivers.
- Each driver has a `max_deliveries` of 3 or 4.
- Each driver has 1 or 2 unavailable time slots.
- The 5 vans have different amounts of cargo space, and at least 2 deliveries are too big for every van except the largest one.
- At least 10 deliveries have a time window narrower than 0 to 7.
- `linked_deliveries.csv` lists 4 pairs of deliveries, and the pairs don't share any deliveries.

If Z3 says your data has no solution, that's not necessarily a bug in your code. Use the unsat core (requirement 7) to find out which rules conflict, then adjust your data.

## Requirements

1. **Data files.** Create the four CSV files described above.
2. **Loading data.** Load each CSV file into a list of dictionaries, for example with `csv.DictReader`. Convert numbers to `int` and split the semicolon lists into Python lists.
3. **Decision variables.** For each delivery, create three Z3 `Int` variables: its time slot, its driver (an index into the drivers list) and its van (an index into the vans list).
4. **Constraints.** Add constraints for all nine scheduling rules. You will need these Z3 tools: `And`, `Or`, `Not`, `Implies`, and `Sum` combined with `If` for counting (rule 7). For rules 2 and 3 you can use either `Implies` on every pair of deliveries or `Distinct`.
5. **Solving.** Use a Z3 `Solver` to find a schedule. Read the values out of the model and return the schedule as a list of dictionaries. Print the schedule in a readable table sorted by time slot, showing the delivery window, delivery ID, skill needed, driver and van.
6. **Improving the schedule.** Balance the workload so that no driver gets many more deliveries than the others. Use a loop with `push()` and `pop()`: add a constraint that every driver has at most *k* deliveries, check, then lower *k* and try again. Stop when the check is `unsat` or `unknown`, or when *k* reaches the lowest possible value, which is 30 ÷ 10 = 3. Set a timeout on the solver so that a single check can't run forever. Print the best *k* you found and the schedule that goes with it.
7. **Explaining an impossible schedule.** Create one Boolean tracking variable per constraint group (the names in the rules table) and add each constraint as `Implies(group_flag, constraint)`. Call `check()` with all the flags as assumptions. When the result is `unsat`, print the names of the groups in `unsat_core()`. Make a folder named `bad_data` with three variations of your data, each of which breaks a different rule. For example: a delivery bigger than the largest van's cargo space, a linked delivery whose time window ends before the first delivery's window starts, or a skill that no available driver has. Your program must report the conflicting groups for each one.
8. **Separation of concerns.** Keep the Z3 model and solving code in its own module, separate from file loading and from user input and output.
9. **Testing.** Write a test module with a function that checks a schedule against all nine rules in plain Python, without using Z3. Use it to test that:
   - the schedule from your real data passes every rule,
   - each data set in `bad_data` is reported as `unsat` with the expected constraint group in the core,
   - the checker itself catches a schedule that you broke on purpose, for example by moving two deliveries into the same van at the same time.

## Z3 Tips

These snippets show the pattern for this problem. Your code will need more than this.

```python
from z3 import Solver, Int, Bool, And, Or, Implies, Sum, If, sat, unsat

# One set of decision variables per delivery (requirement 3)
slot = []
driver = []
van = []
for delivery in deliveries:
    delivery_id = delivery["delivery_id"]
    slot.append(Int("slot_" + delivery_id))
    driver.append(Int("driver_" + delivery_id))
    van.append(Int("van_" + delivery_id))

# One tracking flag per constraint group (requirement 7)
group_names = ["domain", "van_conflict", "driver_conflict", "qualification",
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
