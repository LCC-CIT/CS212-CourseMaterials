<h1>Constraint Solvers</h1>

**CS 212 AI Programming 1**

<h2>Contents</h2>

[TOC]

## The Big Idea: Describe the Answer, Don't Compute It

Most of the programming you have done so far is *imperative*: you write step-by-step instructions that *compute* an answer.

A *constraint solver* works the opposite way. You don't tell it *how* to find the answer. You only describe what a correct answer looks like, and the solver figures out the rest. This style is called *declarative* programming.

You already know a tiny version of this from algebra class:

> Find two numbers, *x* and *y*, such that  
> x + y = 10  
> x − y = 2

You didn't follow a fixed recipe; you worked out an answer (x = 6, y = 4) that satisfied the two *rules*. A constraint solver does the same thing, but for problems with hundreds or thousands of unknowns and rules, where solving by hand would be impossible.

### The Three Inputs

Every constraint problem has the same three parts:

| Input | Meaning | Example (above) |
| --- | --- | --- |
| **Variables** (also called *decision variables*) | The unknowns you want the solver to find | `x`, `y` |
| **Domains** | The kinds of values each variable may take (whole numbers, true/false, ...) | whole numbers |
| **Constraints** | Rules that any valid answer must obey | `x + y == 10`, `x - y == 2` |

The solver searches for values for the variables that make **every** constraint true at the same time. There are three possible outcomes:

- **Satisfiable (`sat`)**: at least one solution exists, and the solver gives you one.
- **Unsatisfiable (`unsat`)**: the rules contradict each other (for example, *a > 5* and *a < 3*), so no solution exists. Knowing that is useful too!
- **Unknown**: the problem was too hard and the solver gave up (rare for the problems in this course).

### Why Not Just Write a Loop?

You *could* solve small problems by trying every combination with nested loops. But the number of combinations explodes. It increases with the number of constraints and the domain size (boundaries of the possible solution). Constraint solvers use smart techniques to rule out huge numbers of combinations at once. When they learn that a partial answer breaks a rule, they discard every answer that starts that way without looking at any of them.

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

