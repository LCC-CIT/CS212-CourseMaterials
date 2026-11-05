---
title: Lab 1, Group C
description: Group C assignment to translate and write Python apps
keywords: python, programming, AI, challenge, selection statements
material: Lab Instructions
generator: Typora
author: Brian Bird
---

<h1>Lab 1, Python and AI Warm-Up</h1>

<h2>Group C</h2>

**CS 212, AI Programming 1**



### 1. Translate a Program into Python

#### PC Component Compatibility Checker

Create a system that checks the compatibility of two core PC components: the **CPU Socket Type** and the **RAM Type**. The system should output whether the components are **Compatible** or **Incompatible**.

| CPU Socket Type | Required RAM Type | Result if Correct RAM | Result if Incorrect RAM |
| --------------- | ----------------- | --------------------- | ----------------------- |
| **LGA1700**     | DDR5              | Compatible            | Incompatible            |
| **AM4**         | DDR4              | Compatible            | Incompatible            |
| **Other**       | Any               | Incompatible          | Incompatible            |


Translate the program from either <a href="pcComponentCompatibility.js" download>JavaScript</a> or <a href="pcComponentCompatibility.cs" download>C#</a> into Python



### 2. Write a Python Program

#### Athlete Performance Rating

Design an expert system that assigns a performance *Rating* to an athlete based on their *Speed Score* (0-100) and *Strength Score* (0-100). The system must assign the highest applicable tier.

- **Elite:** Speed Score ≥90 **AND** Strength Score ≥80.
- **Advanced:** Speed Score ≥70 **OR** Strength Score ≥70.
- **Intermediate:** Speed Score ≥50.
- **Beginner:** All other scores.



### Program requirements

*(Draft for next year. It fixes the details that this year's students had to guess, so the check scripts can be strict.)*

- Name your files `pc_compatibility.py` / `athlete_rating.py`.
- Put each program's decision logic in one function: Part 1 `check_compatibility(socket_type, ram_type)`, Part 2 `rate_athlete(speed, strength)`. Use these exact function and parameter names. The functions **return** their answer (they do not only print it); Part 1 returns `Compatible` or `Incompatible`, Part 2 returns `Elite`, `Advanced`, `Intermediate` or `Beginner`.
- Also include a small `main()` that asks the user for the inputs with `input()` (socket, then RAM for Part 1; the Part 2 inputs in the order of its function's parameters), calls your function and prints the result. Run `main()` only when the file is run directly (`if __name__ == "__main__":`).
- Socket and RAM names may be typed in any letter case. An unknown socket or RAM type is `Incompatible`, not an error.
- Use the wording of the tables in this document for every result.

### Check your work before you submit

Run the check scripts for your group (`check_compat.py` and `check_athlete.py`, in the Group C `drivers` folder, with a README) from the folder that holds your programs. Each case prints `PASS` or `FAIL`. Every line should say PASS before you post your beta version. Add your own tests as well: a test program is graded, so test the boundaries of each table.

## Submitting your lab work on Canvas

### Beta Version

- Post the beta version of both programs to your team channel in Discord.

### Code Review

- Review one of your lab partners' code and post the review in your team channel on Discord.
- Submit a copy of the code review <u>you did</u> to the code review assignment on Canvas.

### Production Version

 Based on the code review and helpful advice from your lab partners, you may revise your code. On the code review from your lab partner, complete the “Prod.” column to show what you revised. Upload the following to the *Lab Production Version* assignment on Canvas:

1. The two Python (.py) files
2. The code review <u>from your lab partner</u> with the “Prod.” column filled out by you.

This will be a total of 3 files.

### Grading Criteria

The main focus of grading will be on correct coding and problem solving skills.

