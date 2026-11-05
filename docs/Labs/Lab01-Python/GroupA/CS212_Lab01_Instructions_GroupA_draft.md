---
title: Lab 1, Group A
description: Group A assignment to translate and write Python apps
keywords: if
material: Lab Instructions
generator: Typora
author: Brian Bird
---

<h1>Lab 1, Python and AI Warm-Up</h1>

<h2>Group A</h2>

**CS 212, AI Programming 1**



### 1. Translate a Program into Python

#### Shipping Cost Calculator

This program calculates the shipping cost based on the package's *Weight (in kg)* and the *Destination Zone* (A, B, or C). The system must apply base costs and surcharges using the following tiered structure:

| Zone  | Weight ≤5 kg | 5< Weight ≤10 kg | Weight >10 kg |
| ----- | ------------ | ---------------- | ------------- |
| **A** | $10.00       | $15.00           | $20.00        |
| **B** | $15.00       | $20.00           | $25.00        |
| **C** | $20.00       | $25.00           | $30.00        |

Translate the program from either <a href="shippingCalculator.js" download>JavaScript</a> or <a href="shippingCalculator.cs" download>C#</a> into Python

### 2. Write a Python Program

#### Financial Product Recommendation System

Create a simplified expert system that recommends a suitable investment product based on two factors provided by the user: *Investment Horizon* (Short-Term: <5 years, or Long-Term: ≥5 years) and *Risk Tolerance* (Low or High).

| Horizon    | Risk Tolerance | Recommended Product         |
| ---------- | -------------- | --------------------------- |
| Short-Term | Low            | High-Yield Savings Account  |
| Short-Term | High           | Short-Term Corporate Bonds  |
| Long-Term  | Low            | Government Bonds/Index Fund |
| Long-Term  | High           | Diversified Stock Portfolio |

### Program requirements

*(Draft for next year. It fixes the details that this year's students had to guess, so the check scripts can be strict.)*

- Name your files `shipping_cost.py` / `recommend.py`.
- Put each program's decision logic in one function: Part 1 `shipping_cost(weight_kg, zone)`, Part 2 `recommend_product(horizon, risk)`. Use these exact function and parameter names. The functions **return** their answer (they do not only print it); Part 1 returns the cost as a number (for example `15.0`), Part 2 returns the product name exactly as written in the table.
- Also include a small `main()` that asks the user for the inputs with `input()` (weight, then zone for Part 1; the Part 2 inputs in the order of its function's parameters), calls your function and prints the result. Run `main()` only when the file is run directly (`if __name__ == "__main__":`).
- Zones may be typed in lower case. Anything that is not zone A, B or C is invalid input; say so instead of guessing a cost.
- Use the wording of the tables in this document for every result.

### Check your work before you submit

Run the check scripts for your group (`check_shipping.py` and `check_recommend.py`, in the Group A `drivers` folder, with a README) from the folder that holds your programs. Each case prints `PASS` or `FAIL`. Every line should say PASS before you post your beta version. Add your own tests as well: a test program is graded, so test the boundaries of each table.

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

