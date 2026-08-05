---
title: Unit 1 Overview
description: What's AI
keywords: Classical AI, Symbolic AI, GOFAI
generator: Typora
author: Brian Bird
---

**CS 210, Intro to AI Programming**

<h1>Rule-Based AI Techniques: Overview</h1>


| Topics                                           |                           |
| ------------------------------------------------ | ------------------------- |
| 1. What is AI, Python                            | 6. ANN: Image recognition |
| 2. Symbolic AI:  <mark>rule-based systems</mark> | 7. Generative AI          |
| 3. Classical Machine Learning: Training          | 8. Custom chatbot         |
| 4. Classical Machine Learning: Inference         | 9. LLM fine-tuning        |
| 5. Midterm                                       | 10. Ethics                |
|                                                  | 11. Final                 |

<h2>Contents</h2>

[TOC]



## Review

- John McCarthy, a mathematics professor at Dartmouth College coined the term *Artificial Intelligence* in 1956.
- Categories of AI
  (There are other categories, but these are some of the major ones.)

  - Symbolic (GOFAI)
    - Rule-based (expert) systems
    - Search-based
  
  
    - Machine Learning
      - Statistical
      - ANN (Artificial Neural Networks)
  


## Introduction

- Last time, we briefly discussed expert systems as an example of *rule-based systems*. You wrote a "toy" version of an *expert system* that used hard-coded if-then statements to implement the rules.
- This time you will make an expert system that has rules stored in a file so that it is more flexible and can be updated without re-writing code.

## More on Rule-Based (Expert) Systems

### What are Rule-Based AI Systems?

*Rule-based AI (RBAI)* systems are a classical type of symbolic AI that operates by applying predefined logical rules in order to solve a problem or reach a decision.

- Purpose: To mimic human-like decision-making and reasoning in specific, limited domains.
- How it works: Logic is encoded in *declarative rules* (often in IF-THEN format) that are stored in a knowledge base (file, database) separate from the system's code. This allows rules to be easily revised or expanded without rewriting the program code.
- Advantages:
  - Transparency and Trust: Decisions are fully explainable, consistent, and traceable to specific, human-readable rules, which is essential for regulated industries.
  - Low Data Dependency: Can be built and deployed quickly using only expert knowledge, without the need for large, labeled training datasets.
- Disadvantages
  - Poor Scalability and Rigidity: Systems become unmanageable as complexity grows. They cannot learn, adapt, or handle unexpected inputs outside of their predefined rules.
  - Knowledge Acquisition Bottleneck: The process of manually coming up with rules, formalizing, and encoding them is slow and expensive.
- Examples: Fraud detection systems&mdash;expecially financial fraud, medical diagnostic tools, and automated business processes like bank loan approvals.

### Historical Development

Rule-based systems emerged from the mid-20th century's focus on symbolic AI, representing the dominant AI paradigm before the rise of modern machine learning.

- 1956: A significant starting point was the *Logic Theorist* program, created by Allen Newell and Herbert A. Simon which proved that computers could solve complex problems using formal, symbolic logic.
- 1970s–1980s (The AI Boom): The era of the *Expert System* saw the approach gain major commercial and academic traction. Examples:
  - MYCIN (1970s): Developed by Edward Feigenbaum at Stanford, it was one of the first systems designed for medical diagnosis&mdash;using hundreds of rules.
  - XCON (1980): A commercial expert system used by Digital Equipment Corporation (DEC) for configuring complex computer hardware.
- Legacy: While later challenged by scaling issues (known as the "knowledge acquisition bottleneck"), they laid the groundwork for future developments in AI systems[^1].

## How They Work

An RBAI system is fundamentally structured around three main, interacting components that execute a decision cycle.

1. Knowledge Base (or Rule Base):  
     The data store (file, database, etc.) containing all the programmed IF-THEN rules.

2. Working Memory:  
     Temporary storage holding the current facts or input for the specific problem being solved.

3. Inference Engine:  
     The system's 'brain' that manages the process of applying the rules to the data.
     
       - Operation: It continuously matches the IF-conditions in the Knowledge Base against the facts in the Working Memory.
     
       - The Cycle: When a rule's condition is met, its action is "fired" (executed), which either outputs a final answer or adds a new fact to the Working Memory, potentially triggering the next rule in a chain.
     



Note: Some parts of this document were initially drafted with assistance from Gemini 2.5 Flash


---

[![Creative Commons License](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/) Intro to AI Course Materials by [Brian Bird](https://profbird.dev), written in <time>2025</time>, are licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/). 

[^1]: **A) Architectural Separation:** Rule-based systems established fundamental AI architecture by separating the  *Knowledge Base* from the *inference engine*, allowing rules to be easily modified without changing the program code.  **B) Formal Knowledge Representation:** They pioneered the structured representation of human logic making expert thought machine-readable for the first time. **C) Automated Reasoning:** The introduction of the *Inference Engine* provided computational *models* for deductive reasoning (like Forward and Backward Chaining), demonstrating how a computer could link discrete facts and rules to reach logical, non-obvious conclusions.
