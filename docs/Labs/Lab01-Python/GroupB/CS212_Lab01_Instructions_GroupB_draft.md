---
title: Lab 1, Group B
description: Group B assignment to translate and write Python apps
keywords: python, programming, AI, challenge, selection statements
material: Lab Instructions
generator: Typora
author: Brian Bird
---

<h1>Lab 1, Python and AI Warm-Up</h1>

<h2>Group B</h2>

**CS 212, AI Programming 1**



### 1. Translate a Program into Python

#### Meeting Room Reservation System

Build a reservation system that recommends a meeting room based on the number of *Attendees* and whether a *Projector is Needed* (True/False).

| Attendees         | Projector Needed | Recommended Room                    |
| ----------------- | ---------------- | ----------------------------------- |
| **1−5 (Small)**   | Any              | Room Alpha (No Projector)           |
| **6−15 (Medium)** | True             | Room Beta (Has Projector)           |
| **6−15 (Medium)** | False            | Room Gamma (No Projector)           |
| **16+ (Large)**   | Any              | Reservation Denied (No large rooms) |


Translate the program from either <a href="roomReservations.js" download>JavaScript</a> or <a href="roomReservations.cs" download>C#</a> into Python



### 2. Write a Python Program

#### Server Status and Priority Alert

Create a simplified system for monitoring a server cluster. The system uses a *Health Code* (1=Critical, 2=Warning, 3=Optimal) and the *Time Since Last Check* (in hours) to determine the required response priority.

| Health Code  | Time Since Last Check (H) | Alert Priority |
| ------------ | ------------------------- | -------------- |
| 1 (Critical) | Any                       | **HIGH**       |
| 2 (Warning)  | >4 Hours                  | **HIGH**       |
| 2 (Warning)  | ≤4 Hours                  | **MEDIUM**     |
| 3 (Optimal)  | >10 Hours                 | **LOW**        |
| 3 (Optimal)  | ≤10 Hours                 | **CLEAR**      |



### Program requirements

*(Draft for next year. It fixes the details that this year's students had to guess, so the check scripts can be strict.)*

- Name your files `room_reservations.py` / `server_status.py`.
- Put each program's decision logic in one function: Part 1 `recommend_room(attendees, projector_needed)`, Part 2 `alert_priority(health_code, hours)`. Use these exact function and parameter names. The functions **return** their answer (they do not only print it); Part 1 returns the text in the *Recommended Room* column (for example `Room Beta`), Part 2 returns `HIGH`, `MEDIUM`, `LOW` or `CLEAR`.
- Also include a small `main()` that asks the user for the inputs with `input()` (attendees, then projector (True/False) for Part 1; the Part 2 inputs in the order of its function's parameters), calls your function and prints the result. Run `main()` only when the file is run directly (`if __name__ == "__main__":`).
- Zero or negative attendees, and health codes other than 1, 2 or 3, are invalid input; say so instead of guessing.
- Use the wording of the tables in this document for every result.

### Check your work before you submit

Run the check scripts for your group (`check_rooms.py` and `check_server.py`, in the Group B `drivers` folder, with a README) from the folder that holds your programs. Each case prints `PASS` or `FAIL`. Every line should say PASS before you post your beta version. Add your own tests as well: a test program is graded, so test the boundaries of each table.

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

