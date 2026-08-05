---
title: Unit 1 Overview
description: What's AI
keywords: Classical AI, Symbolic AI, GOFAI
generator: Typora
author: Brian Bird
---

**CS 210, Intro to AI Programming**

<h1>Designing Rules for a Knowledge Base</h1>

| Topics                                    |                           |
| ----------------------------------------- | ------------------------- |
| 1. What is AI, Python                     | 6. ANN: Image recognition |
| 2.  Symbolic AI:  <mark>rule-based</mark> | 7. Generative AI          |
| 3. Classical Machine Learning: Training   | 8. Custom chatbot         |
| 4. Classical Machine Learning: Inference  | 9. LLM fine-tuning        |
| 5. Midterm                                | 10. Ethics                |
|                                           | 11. Final                 |

<h2>Contents</h2>

[TOC]

A knowledge base consists of a set of rules. In most expert systems these rules are designed so that one rule can potentially trigger one or more other rules. This is called *forward chaining*.

## Designing a Set of Rules for Forward Chaining

Here is an example of a set of rules for a hypothetical medical diagnosis expert system. Most of these rules are set up for forward chaining. See the explanation below the table.

| **IF**                            | **THEN**                 | **GOAL** |
| --------------------------------- | ------------------------ | -------- |
| fever and cough                   | suspect_flu              |          |
| headache and nausea               | suspect_migraine         |          |
| cough and wheezing                | suspect_bronchitis       |          |
| suspect_flu and body_aches        | diagnosis_influenza      |          |
| suspect_flu and sore_throat       | diagnosis_common_cold    |          |
| suspect_bronchitis and chest_pain | diagnosis_bronchitis     | GOAL     |
| diagnosis_influenza               | recommend_rest           | GOAL     |
| diagnosis_migraine                | recommend_dark_room      | GOAL     |
| no_appetite and stomach_pain      | diagnosis_food_poisoning | GOAL     |

### The IF Column

In this example, each item in the "IF" column is set of conditions that could trigger the rule. Some of these conditions are *initial facts* (the symptoms), others will be *new facts* inferred from previously applied rules (like suspected diagnosis).

### The THEN and GOAL Column

These are the *new facts* that will be used as conditions to fire and apply subsequest rules, unless the rule is marked as being a "GOAL"

### Depth of Chaining

- No chaining: A rule leads directly to a THEN which is a GOAL.  
  For example:

  - The rule triggered by `"no_appetite" and "stomach_pain"` results directly in  	`"diagnosis_food_poisoning"` which is a GOAL.

- Two rule depth: The first rule results in a THEN (new fact) which can (possibly with an additonal condition) trigger a second rule which is a GOAL.  
  For example:

  1. The rule triggered by `"cough" and "wheezing"` results in `suspected_bronchitis` 

  2. The rule triggerd by `"suspected_bronchitis"` and `"chest_pain"` results in `"diagnosis_bronchitis"` which is a GOAL.

- Three rule depth: The first rule results in a THEN (new fact) which can (possibly with an additonal condition) trigger a second rule which in turn (possibly with an additional condition) trigger a third rule which is a GOAL.  
  For example:

  1. The rule triggered by `"fever" and "cough"` results in `suspect_flu`

  2. The rule triggered by `"suspect_flu" and "body_aches"` results in `diagnosis_influenza`

  3. The rule tringgered by `diagnosis_influenza` results in `recommend_rest` which is a GOAL.

     

### Implementation in a CSV Rule File

The contents of a CSV (Comma Separated Value) file would look like this:

```tex
fever,cough,suspect_flu,  
headache,nausea,suspect_migraine,
cough,wheezing,suspect_bronchitis
suspect_flu,body_aches,diagnosis_influenza,  
suspect_flu,sore_throat,diagnosis_common_cold, 
suspect_bronchitis,chest_pain, diagnosis_bronchitis,GOAL
diagnosis_influenza,,recommend_rest,GOAL 
diagnosis_migraine,,recommend_dark_room,GOAL 
no_appetite,stomach_pain,diagnosis_food_poisoning,GOAL
```

Note that each row needs to have the same number of commas. If some rows don't have as many entries, there still need to be commas as "placeholders" to preserve consistency in the number of columns for each line.




---

[![Creative Commons License](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/) Intro to AI Programming Course Materials by [Brian Bird](https://profbird.dev), written in <time>2025</time>, are licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/). 

---

