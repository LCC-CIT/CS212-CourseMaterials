---
title: Lab 2, Group A
description: Group A assignment to use the Z3 constraint solver to schedule class sections, instructors and classrooms
keywords: constraint solver, Z3, scheduling, constraint satisfaction, unsat core, CSV files, testing
material: Lab Instructions
generator: Typora
author: Brian Bird
---

<h1>Lab 2, Scheduling with a Constraint Solver</h1>

<h2>Group A</h2>

**CS 212, AI Programming 1**

## Scheduling a CS Department

Every term, a computer science department has to decide when each class section meets, who teaches it and which room it's in. Doing this by hand is slow and it's easy to create conflicts, such as two sections in the same room at the same time.

In this lab you will write a Python program that uses the Z3 constraint solver to build the schedule. You won't write a search algorithm. Instead, you will describe what a valid schedule looks like, as constraints, and Z3 will find one.

## The Problem

The department offers 30 class sections, has 10 instructors and 5 classrooms. Classes meet on Monday and Wednesday in one of 8 time slots.

| What | How many | Data file |
| --- | --- | --- |
| Class sections | 30 | `sections.csv` |
| Instructors | 10 | `instructors.csv` |
| Classrooms | 5 | `classrooms.csv` |
| Time slots | 8 (numbered 0 to 7) | none, the slots are fixed (see below) |
| Lecture and lab pairs | 4 | `section_pairs.csv` |

Each time slot is a 1 hour 20 minute class period on Monday and Wednesday.

| Slot | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Time | 8:00 am | 9:30 am | 11:00 am | 12:30 pm | 2:00 pm | 3:30 pm | 5:00 pm | 6:30 pm |

To keep the problem manageable, every section takes exactly one time slot.

### Scheduling Rules

A valid schedule must follow all of these rules. Each rule will become a group of constraints in your program.

| # | Rule | Constraint group name |
| --- | --- | --- |
| 1 | Every section gets a time slot (0 to 7), an instructor and a classroom that exist in the data. | `domain` |
| 2 | No two sections can use the same classroom in the same time slot. | `room_conflict` |
| 3 | No instructor can be assigned to two sections in the same time slot. | `instructor_conflict` |
| 4 | Each section is taught by an instructor who is qualified to teach that course. | `qualification` |
| 5 | Each section is in a classroom with at least as many seats as the section's enrollment. | `capacity` |
| 6 | No instructor is scheduled in a time slot listed as unavailable for them. | `availability` |
| 7 | No instructor is assigned more sections than their `max_sections` limit. | `workload` |
| 8 | Each section meets within its allowed time window (`earliest_slot` to `latest_slot`). For example, an evening section must be in slot 6 or 7. | `time_window` |
| 9 | For each lecture and lab pair, the lab meets at least one time slot after the lecture. | `ordering` |

## Data Files

You will create the data files yourself. Use these columns. In columns that hold a list, separate the items with semicolons, for example `CS133Y;CS161;CS162`.

**`instructors.csv`**

| Column | Meaning |
| --- | --- |
| `instructor_id` | A short ID, for example `I01` |
| `name` | Instructor's name |
| `max_sections` | Most sections this instructor can teach |
| `unavailable_slots` | Time slots this instructor can't teach, for example `0;7` |
| `qualified_courses` | Courses this instructor can teach |

**`classrooms.csv`**

| Column | Meaning |
| --- | --- |
| `room_id` | Room number, for example `BLD19-108` |
| `seats` | Number of seats |

**`sections.csv`**

| Column | Meaning |
| --- | --- |
| `section_id` | A short ID, for example `S01` |
| `course` | Course number, for example `CS161` |
| `enrollment` | Number of students enrolled |
| `earliest_slot` | Earliest allowed time slot |
| `latest_slot` | Latest allowed time slot |

**`section_pairs.csv`**

| Column | Meaning |
| --- | --- |
| `first_section` | The lecture section |
| `second_section` | The lab section that must meet later |

Your data must meet these requirements so that it is realistic and the problem is not too easy:

- Use exactly 30 sections, 10 instructors and 5 classrooms.
- There are 6 different courses. Every instructor is qualified for 3 or 4 of them, and every course has at least 4 qualified instructors.
- Each instructor has a `max_sections` of 3 or 4.
- Each instructor has 1 or 2 unavailable time slots.
- The 5 classrooms have different numbers of seats, and at least 2 sections are too big for every classroom except the largest one.
- At least 10 sections have a time window narrower than 0 to 7.
- `section_pairs.csv` lists 4 pairs of sections, and the pairs don't share any sections.

If Z3 says your data has no solution, that's not necessarily a bug in your code. Use the unsat core (requirement 7) to find out which rules conflict, then adjust your data.

## Requirements

1. **Data files.** Create the four CSV files described above.
2. **Loading data.** Load each CSV file into a list of dictionaries, for example with `csv.DictReader`. Convert numbers to `int` and split the semicolon lists into Python lists.
3. **Decision variables.** For each section, create three Z3 `Int` variables: its time slot, its instructor (an index into the instructors list) and its classroom (an index into the classrooms list).
4. **Constraints.** Add constraints for all nine scheduling rules. You will need these Z3 tools: `And`, `Or`, `Not`, `Implies`, and `Sum` combined with `If` for counting (rule 7). For rules 2 and 3 you can use either `Implies` on every pair of sections or `Distinct`.
5. **Solving.** Use a Z3 `Solver` to find a schedule. Read the values out of the model and return the schedule as a list of dictionaries. Print the schedule in a readable table sorted by time slot, showing the time, section, course, instructor and classroom.
6. **Improving the schedule.** Balance the workload so that no instructor gets many more sections than the others. Use a loop with `push()` and `pop()`: add a constraint that every instructor has at most *k* sections, check, then lower *k* and try again. Stop when the check is `unsat` or `unknown`, or when *k* reaches the lowest possible value, which is 30 ÷ 10 = 3. Set a timeout on the solver so that a single check can't run forever. Print the best *k* you found and the schedule that goes with it.
7. **Explaining an impossible schedule.** Create one Boolean tracking variable per constraint group (the names in the rules table) and add each constraint as `Implies(group_flag, constraint)`. Call `check()` with all the flags as assumptions. When the result is `unsat`, print the names of the groups in `unsat_core()`. Make a folder named `bad_data` with three variations of your data, each of which breaks a different rule. For example: a section with more students than the largest classroom holds, a lab whose time window ends before its lecture's window starts, or a course that no available instructor is qualified to teach. Your program must report the conflicting groups for each one.
8. **Separation of concerns.** Keep the Z3 model and solving code in its own module, separate from file loading and from user input and output.
9. **Testing.** Write a test module with a function that checks a schedule against all nine rules in plain Python, without using Z3. Use it to test that:
   - the schedule from your real data passes every rule,
   - each data set in `bad_data` is reported as `unsat` with the expected constraint group in the core,
   - the checker itself catches a schedule that you broke on purpose, for example by moving two sections into the same classroom at the same time.

## Z3 Tips

These snippets show the pattern for this problem. Your code will need more than this.

```python
from z3 import Solver, Int, Bool, And, Or, Implies, Sum, If, sat, unsat

# One set of decision variables per section (requirement 3)
slot = []
instructor = []
room = []
for section in sections:
    section_id = section["section_id"]
    slot.append(Int("slot_" + section_id))
    instructor.append(Int("instructor_" + section_id))
    room.append(Int("room_" + section_id))

# One tracking flag per constraint group (requirement 7)
group_names = ["domain", "room_conflict", "instructor_conflict", "qualification",
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
