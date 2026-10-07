# Lab Partner and Version Assignment Solver

A constraint-satisfaction program using the **Z3 SMT Solver** to partition students into peer-review groups and assign lab versions.

---

## Problem Overview

In a programming course, students are assigned one of three versions of a lab assignment (**Version A, B, or C**). Students perform code reviews for their lab partners, but can only review work on a **different** version of the assignment.

- Students are organized into groups of **3** (or groups of **2** if the class size is not divisible by 3).
- Every student in the same group must be assigned a **different lab version**.
- The program dynamically supports **any number of students** read from a CSV file.

---

## What is Z3?

**Z3** is a high-performance **SMT (Satisfiability Modulo Theories) solver** developed by Microsoft Research. 

Unlike traditional imperative programming where you must write algorithms (loops, backtracking, heuristics) to find a valid arrangement yourself, constraint programming is **declarative**:
1. You define **decision variables** (placeholders for unknown answers).
2. You declare **rules and constraints** that must hold true.
3. You hand the rules to **Z3**, which mathematically searches for a combination of values that satisfies every rule simultaneously.

---

## Quickstart & Setup with `uv`

[`uv`](https://docs.astral.sh/uv/) is a fast Python package and project manager. It reads [`pyproject.toml`](pyproject.toml) and automatically installs the right Python version and packages for you.

### 1. Install `uv`

**Windows** (PowerShell):
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS**: if you already use [Homebrew](https://brew.sh), run `brew install uv`. Otherwise, use the installer below (no need to install Homebrew just for `uv`).

**macOS / Linux**:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Close and reopen your terminal afterward so it can find the `uv` command. Check it with `uv --version`.

### 2. Run the Program
Open a terminal in the `ConstraintSolving` folder you downloaded (for example, `cd Downloads/ConstraintSolving`), then run:

```bash
# Read students.csv and print the groups
uv run assign_lab_partners.py

# Use a different roster and save the results to a CSV file
uv run assign_lab_partners.py -i students.csv -o assignments.csv
```

The first `uv run` takes a minute: it downloads Python 3.14, creates a `.venv` folder, and installs `z3-solver`. After that, it starts right away.

### 3. Run the Notebook (Optional)
Run `uv sync` in this folder to create the `.venv` folder. Then open [`Z3.ipynb`](Z3.ipynb) in VS Code and choose the `.venv` Python environment as the kernel.

---

## Input CSV Format

The input CSV file (`students.csv`) should contain student names in the first column. Headers like `Name` or `Student` are automatically recognized and skipped:

```csv
Name
Aaliyah Jackson
Hiroshi Tanaka
Mateo Rodriguez
Chloe Dubois
...
```

---

## How the Code Works (Step-by-Step)

The Python program ([`assign_lab_partners.py`](assign_lab_partners.py)) and notebook ([`Z3.ipynb`](Z3.ipynb)) use the following workflow:

### Step 1: Group Size Math (`%` Remainder Operator)
To distribute any class size $N$ into groups of at most 3:
```python
MAX_GROUP_SIZE = 3
num_groups = math.ceil(num_students / MAX_GROUP_SIZE)

remainder = num_students % MAX_GROUP_SIZE
if remainder == 0:
    num_groups_of_2 = 0
elif remainder == 2:
    num_groups_of_2 = 1
else:  # remainder == 1 (e.g., 4 students remaining: split into two groups of 2)
    num_groups_of_2 = 2

num_groups_of_3 = num_groups - num_groups_of_2
```
- If $N = 21$ ($21 \pmod 3 = 0$): 7 groups of 3, 0 groups of 2.
- If $N = 20$ ($20 \pmod 3 = 2$): 6 groups of 3, 1 group of 2 ($18 + 2 = 20$).
- If $N = 19$ ($19 \pmod 3 = 1$): 5 groups of 3, 2 groups of 2 ($15 + 4 = 19$).

---

### Step 2: Decision Variables (`Int()`)
```python
group = [Int(f'group_{i}') for i in range(num_students)]
version = [Int(f'version_{i}') for i in range(num_students)]
```
The `Int()` function creates symbolic integer placeholders called **decision variables** (one per student):
- `group[i]`: Represents the group index ($0 \le \text{group}_i < \text{num\_groups}$) assigned to student $i$.
- `version[i]`: Represents the lab version ($0 = \text{A}$, $1 = \text{B}$, $2 = \text{C}$) assigned to student $i$.

---

### Step 3: Domain & Range Constraints (`s.add()`)
```python
for i in range(num_students):
    s.add(group[i] >= 0, group[i] < num_groups)
    s.add(version[i] >= 0, version[i] < 3)
```
`s.add()` registers constraints with the solver. These rules restrict each student's group number to the valid group range and version index to $\{0, 1, 2\}$.

---

### Step 4: Group Size Headcount (`If()` & Overloaded `+=`)
```python
for g in range(num_groups):
    group_size = 0
    for i in range(num_students):
        group_size += If(group[i] == g, 1, 0)

    if g < num_groups_of_3:
        s.add(group_size == 3)
    else:
        s.add(group_size == 2)
```
- **`If(condition, then_value, else_value)`**: Z3's symbolic ternary operator. Because decision variables are unknown during code execution, standard Python `if` cannot inspect them. `If(group[i] == g, 1, 0)` acts as an indicator: evaluates to `1` if student $i$ is in group $g$, and `0` otherwise.
- **Overloaded `+=`**: Z3 overloads the `+` operator. Rather than computing an immediate number, each `+=` appends another term to the formula, building up `group_size` across all students.
- **Headcount Rule**: The first `num_groups_of_3` groups must total 3 students; any remaining groups must total 2 students.

---

### Step 5: Version Diversity Constraints (`Implies()`)
```python
for i in range(num_students):
    for j in range(i + 1, num_students):
        s.add(Implies(group[i] == group[j], version[i] != version[j]))
```
- The nested loops compare every unique pair of students $(i, j)$ once.
- **`Implies(condition, result)`**: Acts as an "if-then" rule. If student $i$ and student $j$ are assigned to the same group (`group[i] == group[j]`), then their versions must not match (`version[i] != version[j]`).

---

### Step 6: Solving & Extracting the Solution
```python
if s.check() == sat:
    m = s.model()
```
- **`s.check()`**: Asks Z3 to find values that satisfy all constraints. It returns `sat` (satisfiable) if a valid arrangement exists.
- **`s.model()`**: Retrieves the concrete values assigned to each decision variable.
- The script maps numeric versions back to letters (`0 -> 'A'`, `1 -> 'B'`, `2 -> 'C'`) and prints or exports the assignments.

---

## File Manifest

| File | Purpose |
|---|---|
| [`assign_lab_partners.py`](assign_lab_partners.py) | Standalone command-line Python application. |
| [`Z3.ipynb`](Z3.ipynb) | Interactive Jupyter Notebook version with step-by-step commentary. |
| [`students.csv`](students.csv) | Sample input roster of 20 students. |
| [`assignments.csv`](assignments.csv) | Sample output generated by the program. |
| [`pyproject.toml`](pyproject.toml) | Environment metadata and dependency specifications. |
| [`README.md`](README.md) | Documentation and setup guide. |
