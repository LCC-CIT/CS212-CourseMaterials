<h1>Python Loops</h1>

**CS 210 Intro to AI Programming**

<h2>Contents</h2>

[toc]

## `for` Loops (Iteration Over a Sequence)

A **`for` loop** is used for iterating over a sequence (such as a list, tuple, dictionary, set, or string) or other iterable objects. It executes a block of code once for each item in the sequence. It's ideal when you know the number of iterations or when you need to process every element in a collection.

| Feature        | Description                                                  |
| -------------- | ------------------------------------------------------------ |
| **Purpose**    | To iterate over items in a collection or sequence.           |
| **Control**    | Controlled by the elements in the iterable.                  |
| **Structure**  | `for <variable> in <iterable>:`                              |
| **Common Use** | Processing lists, calculating sums, or repeating an action a specific number of times (using `range()`). |

**Example (Iterating over a List):**

```python
fruits = ["apple", "banana", "cherry"]

for fruit in fruits:
    print(f"I like {fruit}.")
# Output:
# I like apple.
# I like banana.
# I like cherry.
```

**Example (Iterating a fixed number of times using `range()`):**

```python
for i in range(3): # range(3) produces the sequence 0, 1, 2
    print(f"Count: {i}")
# Output:
# Count: 0
# Count: 1
# Count: 2
```



## `while` Loops (Execution Based on a Condition)

A **`while` loop** is used to execute a block of code **repeatedly as long as a specified condition is true**. It's ideal when you don't know the number of times you need to loop beforehand and the loop should continue until some condition changes (e.g., a user quits, a file runs out of data).

| Feature        | Description                                                  |
| -------------- | ------------------------------------------------------------ |
| **Purpose**    | To execute a block of code as long as a boolean condition remains true. |
| **Control**    | Controlled by a **boolean expression**.                      |
| **Structure**  | `while <condition>:`                                         |
| **Common Use** | Reading external data, user input validation, or countdown timers. |

**Example:**

```python
count = 3

while count > 0:
    print(f"Counting down: {count}")
    count = count - 1 # Crucial step to change the condition
# Output:
# Counting down: 3
# Counting down: 2
# Counting down: 1
```



## Loop Control Statements (Optional)

These statements are used to alter the normal flow of either a `for` or a `while` loop:

| Statement      | Purpose                                                      | Example                                   |
| -------------- | ------------------------------------------------------------ | ----------------------------------------- |
| **`break`**    | Immediately **exits** the loop entirely.                     | `if value == 10: break`                   |
| **`continue`** | Skips the **rest of the current iteration** and moves to the next one. | `if value % 2 == 0: continue`             |
| **`else`**     | Executes a block of code **only if the loop finishes normally** (without being terminated by `break`). | `for i in data: ... else: print("Done!")` |

**Example (`break`):**

```python
numbers = [1, 5, 10, 15]

for num in numbers:
    if num == 10:
        print("Found the number 10, stopping.")
        break
    print(f"Processing: {num}")
# Output:
# Processing: 1
# Processing: 5
# Found the number 10, stopping.
```

**Example (`continue`):**

```python
for x in range(1, 5):
    if x % 2 != 0: # Skip odd numbers
        continue
    print(f"Even number: {x}")
# Output:
# Even number: 2
# Even number: 4
```

## References

- [**Python Looping Techniques **](https://docs.python.org/3/tutorial/datastructures.html#looping-techniques)
  Part of the official Python Tutorial.
- **W3Schools Python Loops**
  - [Python while loops](https://www.w3schools.com/python/python_while_loops.asp)
  - [Python for Loops](https://www.w3schools.com/python/python_for_loops.asp)



Note: This document was drafted using Gemini 2.5 Flash


---

[![Creative Commons License](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/) Intro to AI Programming Course Materials by [Brian Bird](https://profbird.dev), written in <time>2025</time>, are licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/). 

---