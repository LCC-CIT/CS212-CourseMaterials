<h1>The Z3 Constraint Solver</h1>

**CS 212 AI Programming 1**

<h2>Contents</h2>

[TOC]

## Meet Z3

**Z3** is a free, open-source constraint solver from Microsoft Research. Technically it's an **SMT solver** (*Satisfiability Modulo Theories*). You don't need to know what that means. In practice it means that Z3 understands rules about whole numbers, decimal numbers, true/false values, and more, all in the same problem.

Z3 is written in C++, but it comes with a Python package, so you can use it by writing ordinary Python code.

### Installing

In a terminal (in a Jupyter notebook cell, use `%pip install z3-solver` instead):

```bash
pip install z3-solver
```

> The package is named `z3-solver`, but in your code you import it as `z3`.

### Your First Z3 Program

Let's solve the movie seating puzzle from [Constraint Solvers](CS212-Unit02-1-ConstraintSolvers.md). Each friend's seat number is an unknown:

```python
from z3 import Ints, Solver, Distinct, Abs, sat

ana, ben, cat, dev = Ints('ana ben cat dev')  # 1. create the variables

s = Solver()                                  # 2. create a solver

for friend in (ana, ben, cat, dev):           # 3. add the constraints
    s.add(friend >= 1, friend <= 4)           # seats are numbered 1-4
s.add(Distinct(ana, ben, cat, dev))           # everyone gets their own seat
s.add(Abs(ana - ben) > 1)                     # Ana and Ben aren't next to each other
s.add(cat == 1)                               # Cat gets the aisle seat
s.add(Abs(dev - ana) == 1)                    # Dev sits next to Ana
s.add(ana < ben)                              # Ana is to the left of Ben

if s.check() == sat:                          # 4. ask for a solution
    m = s.model()                             # 5. get the solution
    print(m)
else:
    print("No solution")
# Output: [ben = 4, dev = 3, ana = 2, cat = 1]
```

Notice that the code is just the puzzle's rules, translated one by one. Nowhere did we tell Z3 *how* to find the seating.

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

To make a whole **list** of variables, use a loop, like in the lab partner example. Each variable needs a *different* name:

```python
# One variable per package: which truck carries it?
truck = []
for i in range(5):
    truck.append(Int(f'truck_{i}'))
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

### Combining Rules: Z3 Functions

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
| `Abs(a)` | the absolute value (distance from zero) | `Abs(x - y) == 1` means x and y are 1 apart |

Notes:

- `Implies(a, b)` only restricts things when `a` is true. If `a` is false, the rule is satisfied automatically, whatever `b` is.
- `If(...)` is how you do an "if statement" **inside** a rule. A regular Python `if` can't be used because Python can't tell whether `x > 0` is true until the solver has picked a value for `x`. `If(x > 0, 1, 0)` gives `1` when `x` is positive and `0` otherwise, which makes it ideal for **counting**.
- To add up many terms, start at `0` and use `+=` in a loop. This counts how many packages are in truck 0:

  ```python
  count = 0
  for i in range(5):
      count += If(truck[i] == 0, 1, 0)
  ```

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
m[ana]              # the value of ana as a Z3 object: 2
m[ana].as_long()    # the value of ana as a normal Python int: 2
m.eval(ben - ana)   # evaluate any expression using the solution: 2
```

Use `.as_long()` whenever you need a regular Python integer, for example to use it as a list index or in an f-string. Printing a whole model (`print(m)`) shows all the variables in the form `[ben = 4, dev = 3, ana = 2, cat = 1]`. The order isn't predictable, so don't rely on it.

If a variable doesn't matter to any rule, the model may leave it out, and `m[x]` gives `None`. Use `m.eval(x, model_completion=True)` to make Z3 fill in a value. The larger examples below use `m.eval(..., model_completion=True).as_long()` every time, so they always get a Python `int` back.

### A Complete Mini Example

Find three *different* numbers *a*, *b*, *c*, each between 1 and 3, such that *a < b*, and *if b is 3 then c must be 1*:

```python
from z3 import Ints, Solver, And, Distinct, Implies, sat

a, b, c = Ints('a b c')
s = Solver()

for v in (a, b, c):
    s.add(And(v >= 1, v <= 3))     # each is between 1 and 3
s.add(Distinct(a, b, c))           # all different
s.add(a < b)
s.add(Implies(b == 3, c == 1))

if s.check() == sat:
    m = s.model()
    print(m[a], m[b], m[c])        # 1 2 3 (Z3 might pick another valid answer)
```

(Check it by hand: 1 < 2, all different, and *b* isn't 3, so the `Implies` rule doesn't apply. Note that `1 3 2` would break the last rule: *b* is 3, so *c* must be 1. The only other valid answer is `2 3 1`.)

## Putting It Together: Two Realistic Examples

The examples so far were short scripts. A real program is easier to read, test and change when it's split into **modules** (separate `.py` files) that each do one job. The Lab 2 solution uses three:

| Module | Its job | Does it use Z3? |
| --- | --- | --- |
| **Data** (`data_loader.py` in the lab) | Gets the data and returns it as lists and dictionaries | No |
| **Model and solving** (`scheduler.py` in the lab) | Creates the variables, adds the constraints, runs the solver and returns the answer | Yes |
| **Main** (`main.py` in the lab) | Calls the other two and prints the results | No |

The model module doesn't read files or print anything. It takes data in and **returns the answer as a dictionary**, so you can test it without printing, and you can change how the answer is displayed without touching the Z3 code.

Both examples below use this layout. In each one, the three code blocks are three separate files that sit in the same folder. Put them in one folder and run `main.py`.

### Example 1: Airport Gates

Four flights need gates. Each flight has an arrival and departure time (in hours). Two flights that overlap in time can't use the same gate.

**`gate_data.py`** (module 1 of 3: the data)

```python
def load_flights():
    """Return the flights as a list of dictionaries."""
    return [
        {"name": "F1", "arrive": 8, "depart": 10},
        {"name": "F2", "arrive": 9, "depart": 11},
        {"name": "F3", "arrive": 10, "depart": 12},
        {"name": "F4", "arrive": 9, "depart": 10},
    ]
```

A Python dictionary written with `{ "key": value }` works like a JavaScript object literal. When you know the keys ahead of time, write the dictionary this way instead of adding one key at a time.

**`gate_scheduler.py`** (module 2 of 3: the Z3 model)

```python
from z3 import Int, Solver, sat


def create_variables(flights):
    """Make one gate variable for each flight."""
    gate = []
    for flight in flights:
        gate.append(Int("gate_" + flight["name"]))
    return gate


def overlap(flight_a, flight_b):
    """Plain Python: the times are known, so a normal comparison works."""
    return flight_a["arrive"] < flight_b["depart"] and flight_b["arrive"] < flight_a["depart"]


def add_constraints(solver, flights, gate, num_gates):
    for i in range(len(flights)):
        # Each flight uses a valid gate number
        solver.add(gate[i] >= 1, gate[i] <= num_gates)

        # Flights that overlap in time need different gates
        for k in range(i):
            if overlap(flights[i], flights[k]):
                solver.add(gate[i] != gate[k])    # Z3: the gates are unknown


def assign_gates(flights, num_gates):
    """Return {"status": "sat" or "unsat" or "unknown", "gates": {flight name: gate number}}."""
    solver = Solver()
    gate = create_variables(flights)
    add_constraints(solver, flights, gate, num_gates)

    result = solver.check()

    answer = {"status": str(result), "gates": {}}
    if result == sat:
        model = solver.model()
        for i in range(len(flights)):
            gate_number = model.eval(gate[i], model_completion=True).as_long()
            answer["gates"][flights[i]["name"]] = gate_number
    return answer
```

**`main.py`** (module 3 of 3: the output)

```python
from gate_data import load_flights
from gate_scheduler import assign_gates

flights = load_flights()
for num_gates in (2, 3):
    answer = assign_gates(flights, num_gates)
    print(num_gates, "gates:", answer["status"], answer["gates"])

# 2 gates: unsat {}
# 3 gates: sat {'F1': 1, 'F2': 2, 'F3': 1, 'F4': 3}    (Z3 may pick other valid gates)
```

With 2 gates the answer is **`unsat`**: F1, F2, and F4 are all at the airport during the 9 o'clock hour, so three gates are needed. With 3 gates, the solver returns `sat`, and `assign_gates()` reads each flight's gate out of the model.

Some things to notice:

- Two kinds of `if`/comparison are used. The `overlap()` test uses ordinary Python because the times are plain numbers that we already know. The gate rule `gate[i] != gate[k]` uses Z3 because the gates are unknowns.
- `i` and `k` are positions in the `flights` list, and `gate[i]` is the Z3 variable for `flights[i]`. The two lists line up.
- `model.eval(..., model_completion=True)` asks the model for a value and makes Z3 fill one in if no rule mentions that variable. `.as_long()` converts it to a regular Python `int`. Using both every time means you never get `None` back.
- `create_variables()` and `add_constraints()` don't know about the `flights` data. They only look at the list they're given, so the same code works for any set of flights.

### Example 2: Loading Delivery Trucks

Five packages must be split between two trucks. Each truck can carry at most 10 kg.

**`truck_data.py`** (module 1 of 3: the data)

```python
CAPACITY = 10    # kg per truck
NUM_TRUCKS = 2


def load_packages():
    """Return the packages as a list of dictionaries (weight is in kg)."""
    return [
        {"name": "P1", "weight": 4},
        {"name": "P2", "weight": 3},
        {"name": "P3", "weight": 5},
        {"name": "P4", "weight": 2},
        {"name": "P5", "weight": 6},
    ]
```

**`truck_scheduler.py`** (module 2 of 3: the Z3 model)

```python
from z3 import Int, Solver, If, Sum, sat


def create_variables(packages):
    """Make one variable for each package: the number of the truck that carries it."""
    truck = []
    for package in packages:
        truck.append(Int("truck_" + package["name"]))
    return truck


def add_constraints(solver, packages, truck, num_trucks, capacity):
    # Each package goes on a truck that exists
    for p in range(len(packages)):
        solver.add(truck[p] >= 0, truck[p] < num_trucks)

    # The packages on each truck weigh no more than its capacity
    for t in range(num_trucks):
        terms = []
        for p in range(len(packages)):
            terms.append(If(truck[p] == t, packages[p]["weight"], 0))
        solver.add(Sum(terms) <= capacity)


def load_trucks(packages, num_trucks, capacity):
    """Return {"status": ..., "trucks": {package name: truck number}}."""
    solver = Solver()
    truck = create_variables(packages)
    add_constraints(solver, packages, truck, num_trucks, capacity)

    result = solver.check()

    answer = {"status": str(result), "trucks": {}}
    if result == sat:
        model = solver.model()
        for p in range(len(packages)):
            truck_number = model.eval(truck[p], model_completion=True).as_long()
            answer["trucks"][packages[p]["name"]] = truck_number
    return answer
```

**`main.py`** (module 3 of 3: the output)

```python
from truck_data import load_packages, NUM_TRUCKS, CAPACITY
from truck_scheduler import load_trucks

answer = load_trucks(load_packages(), NUM_TRUCKS, CAPACITY)
print(answer["status"])
for name in answer["trucks"]:
    print(name, "-> truck", answer["trucks"][name])
```

`If(truck[p] == t, packages[p]["weight"], 0)` contributes the package's weight *only if* it is on truck `t`, so the `Sum` adds up to the total weight on truck `t`. This "indicator" pattern is how you count and total things in Z3. One valid answer: P1 and P5 on one truck, the other three on the other truck (loads of 10 kg each). Z3 may pick a different valid one.

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

With more than one variable, forbid the whole *combination*, not each value separately: `s.add(Or(x != m[x], y != m[y]))` means "at least one variable must be different next time."

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

### Finding Out Which Rules Conflict: Tracking Flags

When `check()` returns `unsat`, it doesn't say *which* rules are in conflict. To find out, give each group of rules a **tracking flag**, which is a `Bool` variable, and add each rule as `Implies(flag, rule)`. That means "if this flag is on, this rule applies." Then pass the flags to `check()` as **assumptions** (a list of flags to turn on). If there's no solution, `unsat_core()` returns the flags that Z3 had to turn on to prove it.

```python
from z3 import Int, Bool, Solver, And, Implies, unsat

x = Int('x')
in_range = Bool('in_range')     # one flag per group of rules
is_even = Bool('is_even')
is_big = Bool('is_big')

s = Solver()
s.add(Implies(in_range, And(x >= 0, x <= 10)))
s.add(Implies(is_even, x % 2 == 0))
s.add(Implies(is_big, x > 20))

result = s.check([in_range, is_even, is_big])    # the flags are the assumptions
if result == unsat:
    print(s.unsat_core())    # [in_range, is_big]  (the order can vary)
```

The core names `in_range` and `is_big`: no number is both between 0 and 10 and greater than 20. `is_even` isn't in the core because it isn't part of the conflict.

The Lab 2 solution does this with a small `add(group, constraint)` function. Every rule goes through it, so every rule belongs to a group, and it can print the names of the conflicting groups.

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

You can also find a minimum with a `Solver`, `push()` and `pop()`. Try a limit, and if it works, lower the limit by 1 and try again. Read the model *before* you call `pop()`, because the model belongs to that check:

```python
from z3 import Ints, Solver, sat

x, y = Ints('x y')
s = Solver()
s.add(x + y == 10, x >= 0, y >= 0, y <= 7)

best_x = None
limit = 10
while limit >= 0:
    s.push()                 # save a checkpoint
    s.add(x <= limit)        # try a tighter limit
    result = s.check()
    if result == sat:
        best_x = s.model()[x].as_long()
    s.pop()                  # remove the limit
    if result != sat:
        break                # no solution with this limit, so stop
    limit = limit - 1        # try one fewer

print(best_x)    # 3
```

Z3 can take a long time to prove that *no* solution exists. If you know the smallest value that's possible (for example, you can work out that at least 6 jobs must go to part-time mechanics), stop the loop at that lower bound instead of asking Z3 to prove it.

## Tips and Common Pitfalls

1. **`==` vs `=`.** Use `==` inside constraints.
2. **Use `And`/`Or`/`Not`/`If`, not `and`/`or`/`not`/`if`,** whenever the expression contains Z3 variables.
3. **Always bound your variables.** An `Int` can be any whole number, so tell the solver the range you intend (`x >= 0, x < 10`), or it may give you values like `-4827`.
4. **Check before you read.** Call `s.model()` only after `s.check() == sat`.
5. **`unsat` means your rules conflict.** To debug, put the rules in groups with tracking flags and read `unsat_core()`, or comment out constraints one at a time (or use `push`/`pop`) until it becomes `sat`. The last rule you removed was part of the conflict.
6. **Convert answers to Python.** Use `.as_long()` to turn a Z3 integer into a regular `int`, and `model_completion=True` so you always get a value.
7. **Z3 gives *a* solution, not *the* solution.** There may be many valid answers, and which one you get can change if you reorder your constraints or use a different version of Z3. If your program needs a specific answer, add a rule (or use `Optimize`) that says so.
8. **Keep Z3 out of your printing code.** Put the model in its own module that returns a dictionary, and print from `main.py`. The model is easier to test and read.
9. **Keep conflicts small when you test `unsat`.** Proving that no solution exists can take Z3 a very long time, and it may return `unknown` after a timeout. Set one with `s.set("timeout", 10000)` (milliseconds).

## Cheat Sheet

```python
from z3 import *

# --- variables ---
x = Int('x')            # whole number
r = Real('r')           # decimal number
b = Bool('b')           # True / False
a, c, d = Ints('a c d') # several at once

# --- constraints (expressions using +, -, *, ==, !=, <, <=, >, >=) ---
And(x > 0, x < 5)   Or(b, x == 3)   Not(b)   Implies(b, x == 0)
If(x > 0, 1, 0)         # If(condition, value_if_true, value_if_false)
Distinct(a, c, d)
Sum([a, c, d])
Abs(a - c)

# --- solver ---
s = Solver()
s.add(constraint, ...)
s.check()               # sat / unsat / unknown
s.model()               # the solution (only after sat)
s.push();  s.pop()      # temporary constraints
s.reset()               # start over
s.set("timeout", 10000) # give up after 10 seconds (check() returns unknown)
s.check([flag1, flag2]) # check with tracking flags as assumptions
s.unsat_core()          # after unsat: the flags that conflict

# --- reading a model ---
m = s.model()
m[x].as_long()          # Python int
m.eval(expression)      # evaluate an expression using the solution
m.eval(x, model_completion=True).as_long()    # always gives a Python int

# --- optimization ---
o = Optimize()          # like Solver, plus:
o.maximize(expr);  o.minimize(expr)
```

## Practice Problems

1. **Coin puzzle.** You have exactly 6 coins (pennies, nickels, dimes, and quarters) worth a total of 47 cents. How many of each coin do you have? (Variables: `pennies`, `nickels`, `dimes`, `quarters`. Don't forget that you can't have a negative number of coins!) Then change the puzzle to 7 coins and use the technique from [Asking for Another Solution](#asking-for-another-solution) to find every answer.
2. **Impossible?** Add the constraints `x > 10`, `x < 20`, and `x * 2 == 25` for an `Int` named `x`. What does `check()` return? Why?
3. **Meeting times.** Three meetings must be assigned to time slots 1-4 (one slot per meeting, no two meetings in the same slot). Meeting A must be before meeting B, and meeting C can't be in slot 1. Use `Distinct`.
4. **Gates.** In the airport example, add a fifth flight `{"name": "F5", "arrive": 11, "depart": 13}` to `load_flights()` and find the smallest `NUM_GATES` that makes the problem satisfiable.
5. **Trucks.** In the delivery example, change the weights so the packages can't fit in two trucks. How many trucks do you need? Then use `Optimize` to find the minimum automatically. (*Hint:* add an `Int` variable `trucks_used` that is at least `truck[p] + 1` for every package, and minimize it. Remember that `Optimize` is used the same way as `Solver`, so your `add_constraints()` function can take either one.)
6. **Which rules conflict?** In the airport example, give the overlap rules and the valid-gate rules their own tracking flags. Run it with 2 gates and print the `unsat_core()`.

## Further Reading

- [Z3 Python guide ("Z3Py")](https://ericpony.github.io/z3py-tutorial/guide-examples.htm): a longer tutorial with more advanced examples.
- [Z3 on GitHub](https://github.com/Z3Prover/z3)
- Course example: [Lab partner assignment with Z3](../Examples/ConstraintSolving/README.md)
- Course example: [Lab 2 scheduling solution](../Examples/Lab02-Scheduling/Solution/README.md), split into `data_loader.py`, `scheduler.py` and `main.py`



*This page was drafted by Claude Sonnet 5.5 and was revised by Brian Bird with assistance from Claude Opus 5.5, 10/7/26. Examples split into modules and updated to match the Lab 2 solution with Claude Sonnet 5.5, 10/10/26*

---

<a href="http://creativecommons.org/licenses/by-sa/4.0/" target="_blank"><img src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" alt="Creative Commons License"></a> AI Programming 1 Course Materials by <a href="https://profbird.dev" target="_blank">Brian Bird</a>, written in <time>2026</time>, are licensed under a <a href="http://creativecommons.org/licenses/by-sa/4.0/" target="_blank">Creative Commons Attribution-ShareAlike 4.0 International License</a>. 

---

