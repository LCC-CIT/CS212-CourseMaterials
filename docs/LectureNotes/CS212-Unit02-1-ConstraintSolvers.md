<h1>Constraint Solvers</h1>

**CS 212 AI Programming 1**

<h2>Contents</h2>

[TOC]

## Code the Problem, Not the Solution

Most of the programming you have done so far is *imperative*: you write step-by-step instructions that *compute* an answer.

A *constraint solver* works the opposite way. You don't tell it *how* to find the answer. You only describe the problem in terms of what a correct answer looks like, and the solver figures out the rest. This style is called *declarative* programming.

You have probably solved a small version of this kind of problem in a puzzle book:

> Four friends, Ana, Ben, Cat, and Dev, are going to a movie and will sit in four seats in a row, numbered 1 to 4 from left to right.
>
> - Each friend gets their own seat.
> - Ana and Ben had an argument, so they can't sit next to each other.
> - Cat wants the aisle seat, which is seat 1.
> - Dev wants to sit next to Ana.
> - Ana sits somewhere to the left of Ben.
>
> Who sits where?

There is no formula or step-by-step method for this, the way there is for a system of equations in algebra class. Instead, you probably tried an arrangement, checked it against the rules, and crossed out the ones that didn't work: *Cat is in seat 1, so Ana and Ben must be in seats 2 and 4 to avoid being next to each other. Ana is left of Ben, so Ana is in 2 and Ben in 4. That leaves seat 3 for Dev, who is next to Ana. It works!* You described what a correct answer looks like, then searched for one. A constraint solver does the same thing, but for problems with hundreds or thousands of unknowns and rules, where solving by hand would be impossible.

### The Three Inputs

Every constraint problem has the same three parts:

| Input | Meaning | Example (above) |
| --- | --- | --- |
| **Variables** (also called *decision variables*) | The unknowns you want the solver to find | The seat number for each friend: `ana`, `ben`, `cat`, `dev` |
| **Domains** | The kinds of values each variable may take (whole numbers, true/false, ...) | Whole numbers from 1 to 4 |
| **Constraints** | Rules that any valid answer must obey | All four seats are different, `abs(ana - ben) > 1`, `cat == 1`, `abs(dev - ana) == 1`, `ana < ben` |

The solver searches for values for the variables that make **every** constraint true at the same time. There are three possible outcomes:

- **Satisfiable (`sat`)**: at least one solution exists, and the solver gives you one. (For the movie puzzle: `ana = 2`, `ben = 4`, `cat = 1`, `dev = 3`.)
- **Unsatisfiable (`unsat`)**: the rules contradict each other, so no solution exists. For example, if we added the rule "Cat sits next to Ben," there would be no valid seating. Knowing that is useful too!
- **Unknown**: the problem was too hard and the solver gave up (rare for the problems in this course).

### Why Not Just Write a Loop?

You *could* solve small problems by trying every combination with nested loops. For the four friends that's only 4 × 3 × 2 × 1 = 24 seating arrangements, so a loop would finish instantly. But the number of combinations explodes as the problem grows. Seating 20 guests at a wedding has about 2.4 quintillion (2,400,000,000,000,000,000) possible arrangements, far too many to check one at a time. Constraint solvers use smart techniques to rule out huge numbers of combinations at once. When they learn that a partial answer breaks a rule (for example, "Ana in seat 1 and Ben in seat 2"), they discard every answer that starts that way without looking at any of them.

### Constraint Solvers Use Symbolic AI

Constraint solving is part of *symbolic AI*. It works with explicit rules and logic, not with patterns learned from data like machine learning does. Unlike a neural network, a solver's answer is guaranteed to obey your rules, and it can prove when no answer exists. We call this a [*deterministic*](https://en.wikipedia.org/wiki/Deterministic_algorithm) system.

## Real-World Constraint Problems

Many everyday logistics problems fit the variables-and-constraints pattern. Here are three.

### Flight and Gate Scheduling

| Input | In this problem |
| --- | --- |
| Variables | For each flight: which gate it uses (and which crew, which plane...) |
| Domains | Gate 1, 2, 3, ... |
| Constraints | Two flights at the same time can't share a gate. A plane needs 45 minutes between landing and taking off again. A pilot can't work more than 10 hours. |

Airlines run solvers like this every day, and when a storm cancels flights they re-run them to rebuild the schedule.

### Package Delivery

| Ingredient | In this problem |
| --- | --- |
| Variables | For each package: which truck carries it |
| Domains | Truck 0, 1, 2, ... |
| Constraints | A truck can't carry more than its weight limit. Fragile packages can't ride with heavy ones. Packages must arrive before their deadlines. |

You often also want the *best* answer, such as the fewest trucks or the shortest total distance. Many solvers can *optimize*: find a solution that makes some number as small or as large as possible.

### More Examples

- **Class timetables**: no teacher or room is double-booked.
- **Sudoku and other puzzles**: each row, column, and box contains each digit exactly once.
- **Hospital nurse schedules**: everyone gets days off, and every shift is covered.
- **Computer chip design and software verification**: proving that a program can never reach a bad state. (This is what Z3 was originally built for.)
- **Our lab partner example**: assign students to groups of three so that no group has two students with the same lab version. See [`docs/Examples/ConstraintSolving`](../Examples/ConstraintSolving/README.md).

> **Key skill:** Learning to constraint-solve is mostly learning to look at a problem and ask, *"What are the unknowns, and what are the rules?"*



*The first version of this page was drafted by Claude Sonnet 5.5 and revised by Brian Bird*

---

<a href="http://creativecommons.org/licenses/by-sa/4.0/" target="_blank"><img src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" alt="Creative Commons License"></a> AI Programming 1 Course Materials by <a href="https://profbird.dev" target="_blank">Brian Bird</a>, written in <time>2026</time>, are licensed under a <a href="http://creativecommons.org/licenses/by-sa/4.0/" target="_blank">Creative Commons Attribution-ShareAlike 4.0 International License</a>. 

---

