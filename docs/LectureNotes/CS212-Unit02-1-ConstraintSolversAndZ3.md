<h1>Constraint Solvers and Z3</h1>

**CS 212 AI Programming 1**

<h2>Contents</h2>

[TOC]

## The Big Idea: Describe the Answer, Don't Compute It

Most of the programming you have done so far is **imperative**: you write step-by-step instructions that *compute* an answer.

A **constraint solver** works the opposite way. You don't tell it *how* to find the answer. You only describe **what a correct answer looks like**, and the solver figures out the rest. This style is called **declarative** programming.

You already know a tiny version of this from algebra class:

> Find two numbers, *x* and *y*, such that  
> x + y = 10  
> x − y = 2

You didn't follow a fixed recipe; you used the two *rules* to work out the answer (x = 6, y = 4). A constraint solver does the same thing, but for problems with hundreds or thousands of unknowns and rules, where solving by hand would be impossible.

### The Three Ingredients

Every constraint problem has the same three parts:

| Ingredient | Meaning | Example (above) |
| --- | --- | --- |
| **Variables** (also called *decision variables*) | The unknowns you want the solver to find | `x`, `y` |
| **Domains** | The kinds of values each variable may take (whole numbers, true/false, ...) | whole numbers |
| **Constraints** | Rules that any valid answer must obey | `x + y == 10`, `x - y == 2` |

The solver searches for values for the variables that make **every** constraint true at the same time. There are three possible outcomes:

- **Satisfiable (`sat`)**: at least one solution exists, and the solver gives you one.
- **Unsatisfiable (`unsat`)**: the rules contradict each other (for example, *a > 5* and *a < 3*), so no solution exists. Knowing that is useful too!
- **Unknown**: the problem was too hard and the solver gave up (rare for the problems in this course).

### Why Not Just Write a Loop?

You *could* solve small problems by trying every combination with nested loops. But the number of combinations explodes. Assigning each of 20 students to one of 7 groups has about 80 quadrillion possible arrangements, which is far too many to check one by one. Constraint solvers use clever reasoning to **rule out huge numbers of combinations at once**. When they learn that a partial answer breaks a rule, they discard every answer that starts that way without looking at any of them.

Constraint solving is part of **symbolic AI**. It works with explicit rules and logic, not with patterns learned from data like machine learning does. Unlike a neural network, a solver's answer is **guaranteed** to obey your rules, and it can **prove** when no answer exists.

## Real-World Problems That Are Really Constraint Problems

Many everyday logistics problems fit the variables-and-constraints pattern. Here are three.

### Flight and Gate Scheduling

| Ingredient | In this problem |
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

You often also want the *best* answer, such as the fewest trucks or the shortest total distance. Many solvers can **optimize**: find a solution that makes some number as small or as large as possible.

### More Examples

- **Class timetables**: no teacher or room is double-booked.
- **Sudoku and other puzzles**: each row, column, and box contains each digit exactly once.
- **Hospital nurse schedules**: everyone gets days off, and every shift is covered.
- **Computer chip design and software verification**: proving that a program can never reach a bad state. (This is what Z3 was originally built for.)
- **Our lab partner example**: assign students to groups of three so that no group has two students with the same lab version. See [`docs/Examples/ConstraintSolving`](../Examples/ConstraintSolving/README.md).

> **Key skill:** Learning to constraint-solve is mostly learning to look at a problem and ask, *"What are the unknowns, and what are the rules?"*

## Meet Z3

**Z3** is a free, open-source constraint solver from Microsoft Research. Technically it's an **SMT solver** (*Satisfiability Modulo Theories*). You don't need to know what that means. In practice it means that Z3 understands rules about whole numbers, decimal numbers, true/false values, and more, all in the same problem.

Z3 is written in C++, but it comes with a Python package, so you can use it by writing ordinary Python code.

### Installing

In a terminal (or in a Jupyter notebook cell, start the line with `%`):

```bash
pip install z3-solver
```

> The package is named `z3-solver`, but in your code you import it as `z3`.

### Your First Z3 Program

Let's solve the algebra problem from the beginning:

```python
from z3 import Int, Solver, sat

x = Int('x')          # 1. create the variables
y = Int('y')

s = Solver()          # 2. create a solver
s.add(x + y == 10)    # 3. add the constraints
s.add(x - y == 2)

if s.check() == sat:  # 4. ask for a solution
    m = s.model()     # 5. get the solution
    print(m[x], m[y])
else:
    print("No solution")
# Output: 6 4
```

Every Z3 program follows the same five steps: **create variables → create a solver → add constraints → check → read the model.** The rest of this tutorial explains each step.

## Step 1: Creating Variables

A Z3 variable is **not** a normal Python variable. It doesn't hold a value yet. It's a *placeholder* (a **symbol**) that stands for an unknown value the solver will find. Z3 has a function for each type of unknown:

| Function | Creates a variable that is... | Example |
| --- | --- | --- |
| `Int('name')` | a whole number (..., -1, 0, 1, 2, ...) | `age = Int('age')` |
| `Real('name')` | a real (decimal) number | `price = Real('price')` |
| `Bool('name')` | `True` or `False` | `is_late = Bool('is_late')` |
| `Ints('a b c')` | several `Int`s at once | `a, b, c = Ints('a b c')` |
| `Reals('a b')`, `Bools('a b')` | several `Real`s or `Bool`s | |

The string you pass (`'x'`) is the name Z3 uses when it prints results. It's good practice to make it match the Python variable name.

To make a whole **list** of variables, use a list comprehension, like in the lab partner example. Each variable needs a *different* name:

```python
# One variable per package: which truck carries it?
truck = [Int(f'truck_{i}') for i in range(5)]
print(truck)   # [truck_0, truck_1, truck_2, truck_3, truck_4]
```

> **Important:** A Python variable and a Z3 variable are different things.
> After `x = Int('x')`, the Python name `x` refers to a Z3 symbol, not a number. `print(x)` shows `x`, not a value. Only after the solver finishes can you look up a number for it.

## Step 2: Writing Constraints

A constraint is an expression that is either true or false, built with ordinary Python operators:

```python
x + y == 10        # equal  (note the DOUBLE equals sign)
x - y != 3         # not equal
x > 0
x * 2 <= y + 5
```

Because `x` is a Z3 symbol, writing `x + y == 10` does **not** produce `True` or `False` right away. It builds a *rule object* and hands it to the solver. (Python lets a library redefine operators like `+` and `==`; this is called **operator overloading**.)

> ⚠️ **Common mistake:** `x = 10` is Python *assignment* (it throws away your Z3 variable!). `x == 10` is the Z3 *constraint*.

### Combining Rules: Logical Functions

Python's `and`, `or`, `not` and `if` don't work on Z3 expressions. Z3 provides its own capitalized versions:

| Z3 function | Meaning | Example |
| --- | --- | --- |
| `And(a, b, ...)` | all of these are true | `And(x >= 1, x <= 10)` |
| `Or(a, b, ...)` | at least one is true | `Or(x == 1, x == 5)` |
| `Not(a)` | the opposite | `Not(x == 3)` |
| `Implies(a, b)` | *if* a is true, *then* b must be true | `Implies(x > 5, y == 0)` |
| `If(cond, then, else)` | a value that depends on a condition | `If(x > 0, 1, 0)` |
| `Distinct(a, b, c, ...)` | every one has a different value | `Distinct(x, y, z)` |
| `Sum([a, b, c, ...])` | the total of a list of expressions | `Sum([x, y, z])` |

Notes:

- `Implies(a, b)` only restricts things when `a` is true. If `a` is false, the rule is satisfied automatically, whatever `b` is.
- `If(...)` is how you do an "if statement" **inside** a rule. A regular Python `if` can't be used because Python can't tell whether `x > 0` is true until the solver has picked a value for `x`. `If(x > 0, 1, 0)` gives `1` when `x` is positive and `0` otherwise, which makes it ideal for **counting**.
- Use `Sum` with a list comprehension to add up many terms: `Sum([If(truck[i] == 0, 1, 0) for i in range(5)])` counts how many packages are in truck 0.

## Step 3: The Solver Object and Its Methods

`Solver()` creates a solver. It's like an empty "rule book" that you fill with constraints. These are the methods you need:

| Method | What it does |
| --- | --- |
| `s.add(c1, c2, ...)` | Adds one or more constraints to the rule book. A solution must satisfy **all** of them (they are combined with `And`). |
| `s.check()` | Searches for a solution. Returns `sat`, `unsat`, or `unknown`. |
| `s.model()` | After `check()` returns `sat`, returns the solution (a **model**). |
| `s.push()` | Saves the current set of constraints (a "checkpoint"). |
| `s.pop()` | Throws away constraints added since the last `push()`. |
| `s.reset()` | Clears all constraints and starts over. |

### `check()` and `sat`

`check()` doesn't return `True`/`False`. It returns one of three special Z3 values, which you import: `sat`, `unsat`, `unknown`.

```python
from z3 import Int, Solver, sat

a = Int('a')
s = Solver()
s.add(a > 5, a < 3)    # impossible!

result = s.check()
print(result)           # unsat
print(result == sat)    # False
```

**Always check the result before calling `s.model()`.** Asking for the model when there is no solution raises an error.

### Reading the Model

A **model** is the solver's answer: a value for each variable. You can look values up by variable:

```python
m = s.model()
m[x]              # the value of x as a Z3 object, e.g. 6
m[x].as_long()    # the value of x as a normal Python int
m.eval(x * y)     # evaluate any expression using the solution -> 24
```

Use `.as_long()` whenever you need a regular Python integer, for example to use it as a list index or in an f-string. Printing a whole model (`print(m)`) shows all the variables in the form `[y = 4, x = 6]`. The order isn't alphabetical, so don't rely on it.

If a variable doesn't matter to any rule, the model may leave it out, and `m[x]` gives `None`. Use `m.eval(x, model_completion=True)` to make Z3 fill in a value.

### A Complete Mini Example

Find three *different* numbers *a*, *b*, *c*, each between 1 and 3, such that *a < b*, and *if b is 2 then c must be 3*:

```python
from z3 import Ints, Solver, And, Distinct, Implies, sat

a, b, c = Ints('a b c')
s = Solver()

for v in (a, b, c):
    s.add(And(v >= 1, v <= 3))     # each is between 1 and 3
s.add(Distinct(a, b, c))           # all different
s.add(a < b)
s.add(Implies(b == 2, c == 3))

if s.check() == sat:
    m = s.model()
    print(m[a], m[b], m[c])        # 2 3 1 (Z3 might pick another valid answer)
```

(Check it by hand: 2 < 3, all different, and *b* isn't 2, so the `Implies` rule doesn't apply. Note that `1 2 3` would break the last rule: *b* is 2, but *c* must be 3. Z3 didn't need to try it.)

## Putting It Together: Two Realistic Examples

### Example 1: Airport Gates

Four flights need gates. Each flight has a start and end time (in hours). Two flights that overlap in time can't use the same gate.

```python
from z3 import Int, Solver, sat

flights = {            # name: (arrive, depart)
    "F1": (8, 10),
    "F2": (9, 11),
    "F3": (10, 12),
    "F4": (9, 10),
}
names = list(flights)
NUM_GATES = 2

gate = {f: Int(f'gate_{f}') for f in names}   # one variable per flight
s = Solver()

# Each flight uses a valid gate number.
for f in names:
    s.add(gate[f] >= 1, gate[f] <= NUM_GATES)

# Flights that overlap in time need different gates.
for i in range(len(names)):
    for j in range(i + 1, len(names)):
        f, g = names[i], names[j]
        start1, end1 = flights[f]
        start2, end2 = flights[g]
        if start1 < end2 and start2 < end1:      # plain Python: the times are known
            s.add(gate[f] != gate[g])            # Z3: the gates are unknown

print(s.check())    # unsat
```

With 2 gates the answer is **`unsat`**: F1, F2, and F4 are all at the airport during the 9 o'clock hour, so three gates are needed. Change `NUM_GATES` to `3`, and the solver returns `sat`. Then you can read each flight's gate with `s.model()[gate[f]].as_long()`.

Notice the two different kinds of `if`/comparison here. The overlap test uses ordinary Python (`if start1 < end2 ...`) because the times are plain numbers that we already know. The gate rule uses Z3 (`gate[f] != gate[g]`) because the gates are unknowns.

### Example 2: Loading Delivery Trucks

Five packages must be split between two trucks. Each truck can carry at most 10 kg.

```python
from z3 import Int, Solver, Sum, If, sat

weights = {"P1": 4, "P2": 3, "P3": 5, "P4": 2, "P5": 6}   # kg
CAPACITY = 10
NUM_TRUCKS = 2

truck = {p: Int(f'truck_{p}') for p in weights}   # which truck carries each package
s = Solver()

for p in weights:
    s.add(truck[p] >= 0, truck[p] < NUM_TRUCKS)

for t in range(NUM_TRUCKS):
    load = Sum([If(truck[p] == t, w, 0) for p, w in weights.items()])
    s.add(load <= CAPACITY)

if s.check() == sat:
    m = s.model()
    for p in weights:
        print(p, "-> truck", m[truck[p]].as_long())
```

`If(truck[p] == t, w, 0)` contributes the package's weight *only if* it is on truck `t`, so `Sum` gives the total load of truck `t`. This "indicator" pattern is how you count and total things in Z3. One valid answer: P1 and P5 on truck 1, the other three on truck 0 (loads 10 and 10). Z3 may pick a different valid one.

## Going Further

### Asking for Another Solution

`check()` gives you *one* solution. To get another, add a constraint that rules out the one you just found, then check again:

```python
a = Int('a')
s = Solver()
s.add(a >= 1, a <= 3)

while s.check() == sat:
    value = s.model()[a]
    print(value)          # 1, 2, 3 (in some order)
    s.add(a != value)     # forbid this answer
```

When all answers are used up, `check()` returns `unsat` and the loop ends.

### Trying "What If" Scenarios with `push` and `pop`

```python
n = Int('n')
s = Solver()
s.add(n > 0, n < 10)

s.push()               # checkpoint
s.add(n > 20)          # try an extra rule
print(s.check())       # unsat
s.pop()                # undo the extra rule

print(s.check())       # sat
```

### Finding the Best Answer with `Optimize`

When you want the *largest* or *smallest* possible value of something, use `Optimize()` instead of `Solver()`. It has the same `add`, `check`, and `model` methods, plus `maximize` and `minimize`:

```python
from z3 import Ints, Optimize, sat

x, y = Ints('x y')
o = Optimize()
o.add(x >= 0, y >= 0)
o.add(x + y <= 10)         # at most 10 items in total
o.add(x + 2 * y <= 15)     # limited budget

o.maximize(3 * x + 2 * y)  # profit: $3 per x, $2 per y

if o.check() == sat:
    print(o.model())       # x = 10, y = 0  (profit 30)
```

You could use `o.minimize(...)` in the delivery example to find the smallest number of trucks, or the shortest total distance.

## Tips and Common Pitfalls

1. **`==` vs `=`.** Use `==` inside constraints.
2. **Use `And`/`Or`/`Not`/`If`, not `and`/`or`/`not`/`if`,** whenever the expression contains Z3 variables.
3. **Always bound your variables.** An `Int` can be any whole number, so tell the solver the range you intend (`x >= 0, x < 10`), or it may give you values like `-4827`.
4. **Check before you read.** Call `s.model()` only after `s.check() == sat`.
5. **`unsat` means your rules conflict.** To debug, comment out constraints one at a time (or use `push`/`pop`) until it becomes `sat`. The last rule you removed was part of the conflict.
6. **Convert answers to Python.** Use `.as_long()` to turn a Z3 integer into a regular `int`.
7. **Z3 gives *a* solution, not *the* solution.** There may be many valid answers, and the one you get can differ between runs or versions.

## Cheat Sheet

```python
from z3 import *

# --- variables ---
x = Int('x')            # whole number
r = Real('r')           # decimal number
b = Bool('b')           # True / False
p, q, r2 = Ints('p q r2') # several at once

# --- constraints (expressions using +, -, *, ==, !=, <, <=, >, >=) ---
And(p, q)   Or(p, q)   Not(p)   Implies(p, q)
If(cond, value_if_true, value_if_false)
Distinct(a, b, c)
Sum([a, b, c])

# --- solver ---
s = Solver()
s.add(constraint, ...)
s.check()               # sat / unsat / unknown
s.model()               # the solution (only after sat)
s.push();  s.pop()      # temporary constraints
s.reset()               # start over

# --- reading a model ---
m = s.model()
m[x].as_long()          # Python int
m.eval(expression)      # evaluate an expression using the solution

# --- optimization ---
o = Optimize()          # like Solver, plus:
o.maximize(expr);  o.minimize(expr)
```

## Practice Problems

1. **Age puzzle.** Alice is twice as old as Bob. In 5 years, their ages will add up to 40. How old are they now? (Variables: `alice`, `bob`.)
2. **Impossible?** Add the constraints `x > 10`, `x < 20`, and `x * 2 == 25` for an `Int` named `x`. What does `check()` return? Why?
3. **Meeting times.** Three meetings must be assigned to time slots 1-4 (one slot per meeting, no two meetings in the same slot). Meeting A must be before meeting B, and meeting C can't be in slot 1. Use `Distinct`.
4. **Gates.** In the airport example, add a fifth flight `"F5": (11, 13)` and find the smallest `NUM_GATES` that makes the problem satisfiable.
5. **Trucks.** In the delivery example, change the weights so the packages can't fit in two trucks. How many trucks do you need? Then use `Optimize` to find the minimum automatically. (*Hint:* add an `Int` variable `trucks_used` that is at least `truck[p] + 1` for every package, and minimize it.)

## Further Reading

- [Z3 Python guide ("Z3Py")](https://ericpony.github.io/z3py-tutorial/guide-examples.htm): a longer tutorial with more advanced examples.
- [Z3 on GitHub](https://github.com/Z3Prover/z3)
- Course example: [Lab partner assignment with Z3](../Examples/ConstraintSolving/README.md)



*This page was written by Claude Sonnet 5.5. It is a draft and needs to be revised by a human.*
