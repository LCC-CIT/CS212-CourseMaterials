---
title: Lab 1, Example
description: Example assignment to translate and write Python apps
keywords: if
material: Lab Instructions
generator: Typora
author: Brian Bird
---

<h1>Lab 1, Python and AI Warm-Up</h1>

<h2>Example</h2>

**CS 212, AI Programming 1**



### 1. Translate a Program into Python

**Simple Medical Diagnostic System**

This is a simplified diagnostic system for a fictional clinic. The system should take two binary inputs (`True`/`False`): whether the patient has a *Fever* and whether the patient has a *Persistent Cough*. Based on the combination of these symptoms, the system provides a preliminary diagnosis.

| Fever | Persistent Cough | Diagnosis                                                    |
| ----- | ---------------- | ------------------------------------------------------------ |
| True  | True             | Flu - Recommend rest and hydration.                          |
| True  | False            | Possible Infection - Recommend primary care physician visit. |
| False | True             | Cold/Allergies - Recommend over-the-counter medication.      |
| False | False            | General Check-up - Patient appears healthy.                  |

Translate the program from either [JavaScript](medicalDiagnosis.js) or [C#](medicalDiagnosis.cs) into [Python](medicalDiagnosis.py)

### 2. Write a Python Program

**Coffee Order Configuration & Pricing**

Write a program that calculates the price of a custom coffee order. The price is based on the *Size* and the *Milk Type*.

1. **Base Price (Determined by Size):**
   - Small: $3.00
   - Medium: $4.00
   - Large: $5.50
2. **Milk Surcharge (Applied Conditionally):**
   - Oat Milk: +$0.75
   - Almond Milk: +$0.50
   - Dairy Milk: +$0.00

The program should take the size and milk type as input and output the final price.

[Python solution](coffeeOrder.py)
