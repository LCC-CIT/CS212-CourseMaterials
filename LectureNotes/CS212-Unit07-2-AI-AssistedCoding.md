---
title: Week 7 Overview
description: What's happening in CS 210 during week 7
keywords: Announcements, Due Dates, Help
generator: Typora
author: Brian Bird
---

**CS 210, Intro to AI Programming**

<h1>AI-Assisted Coding</h1>

| Topics                                   |                                                              |
| ---------------------------------------- | ------------------------------------------------------------ |
| 1. What is AI, Python                    | 6. ANN: Image recognition                                    |
| 2.  Symbolic AI                          | 7. <mark>Generative AI</mark>                                |
| 3. Classical machine learning: training  | 8. Calling the chat completion API                           |
| 4. Classical machine learning: inference | 9. Agentic AI with MCP                                       |
| 5. More ML + History of AI               | 10. Social and ethical issues  <br />Term project completion |
|                                          | 11. Final project presentation                               |

<h2>Contents</h2>

[TOC]

## What is AI-Assisted Coding

AI-assisted coding has the potential to significantly boost developer productivity by using AI as a *pair programmer* working directly in the development environment (e.g., CLI or IDE) to write code based on natural language prompts from the developer. The underlying Large Language Models (LLMs) then leverage their training on vast codebases to predict and generate entire functions, repetitive boilerplate code, or suggest code completions, to handle routine, time-consuming tasks. 

This assistance allows developers to accelerate debugging, quickly translate code between languages, and focus their time and effort on <u>higher-value activities</u> such as:

- Architectural design.
- Program design.
- Non-standard logic implementation.
-  Higher level problem-solving.



### Don't Call it Vibe Coding

Vibe coding is a term that was casually used by Andrej Karpathy in [a post on X](https://x.com/karpathy/status/1886192184808149383?lang=en) to describe his experience writing code using AI. The term caught on and became popular but then quickly fell into disfavor because it implies a casual, non-rigorous approach that prioritizes quick code generation based on a "vibe" rather than well thought out design and careful testing.

Critics argue it encourages thoughtless production of code without full comprehension, leading to:

- *Technical debt*.
- Security vulnerabilities.
- Code that is difficult to maintain or scale. 

This has been called the "enshitification" of software development.



## How to Code with AI without Making a Mess

The best practices for AI-assisted programming all center on the principle that the <u>human remains the architect, critical reviewer, and final authority.</u>

Here are some basic principles and best practices for good AI-assisted coding, broken down into three core areas:

### Architect & Planner Mindset (Before Coding)

A good developer must plan the system; the AI is merely the builder of a single room.

- **Define the Architecture First:** Do not let the AI define the high-level system structure. The human developer must plan the major components, APIs, and data flow. Only then should you use the AI to implement specific, well-defined functions or modules.

  > *Practice:* Break a large task (like "implement user profile") into small, isolated steps (e.g., "create the user model," "write the API route handler," "generate the unit tests").

- **Prioritize Context and Constraints:** AI models are far more effective when you give them project context.

  - **Share Standards:** Provide the AI with your project's coding conventions, style guides, and common design patterns (e.g., "Always use `snake_case` for variables," "Use our custom `Result` wrapper for all database calls").
  - **Define Requirements:** Be specific about data types, input/output examples, expected behavior, and constraints (e.g., "The function must be optimized for performance on large lists," or "Handle the edge case where the user is not authenticated").

- **Start with Tests:** Utilize the AI to practice Test-Driven Development (TDD). Ask the AI to <u>generate the failing unit tests first</u> based on your requirements. This forces you to clearly define the expected behavior and gives you immediate automated validation once the code is implemented.



### Critical Reviewer Mindset (During Coding)

You must treat AI-generated code as if it were written by a junior developer—it needs rigorous, critical review.

- **Own Every Line:** **Never blindly accept** a suggestion. You are responsible for every line of code committed. If you don't understand how a piece of generated code works, ask the AI to explain it before you integrate it.
- **Check for Security and Edge Cases:** AI often prioritizes functionality over security or robustness.
  - **Security:** Actively look for common vulnerabilities like poor input sanitization, insecure API calls, or missing authentication checks.
  - **Edge Cases:** Review how the code handles null values, empty lists, unexpected data types, or system failures (e.g., database connection error).
- **Encapsulate and Refactor:** Immediately wrap AI-generated code into defined functions, classes, or modules. This improves readability and makes the code easier to isolate, test, and maintain later.
- **Use the AI for Refinement:** Instead of just accepting the first draft, ask the AI to critique its own code (e.g., "Suggest a more Pythonic way to write this loop," or "How can this function be optimized for reduced memory usage?").



### Process & Documentation Mindset (After Coding)

Effective AI usage requires maintaining a clean, well-documented, and controlled environment.

- **Use Version Control Aggressively:** Commit frequently and isolate AI-generated features into their own branches. If the AI introduces a bug or technical debt, a small, isolated commit is easy to review and revert.
- **Document AI Usage:** Make a note of which sections of code were AI-generated. This helps future team members (and your future self) understand why certain architectural decisions were made or where potential "black box" code might exist.
- **Manage Context Windows:** Keep your conversations with the AI focused. For a new, complex task, start a fresh chat session and give the AI a short, fresh briefing. Long, convoluted chat histories lead to confused, low-quality output.
- **Delegate Repetitive Tasks:** Use AI for its greatest strength: generating boilerplate, getters, setters, standard documentation (like JSDoc or Python docstrings), and commit messages. This saves human time for complex problem-solving.

By applying these principles, you move away from "vibe coding" and engage in AI *Pair Programming*, where the AI is a high-speed assistant, and you are the focused, responsible engineer.



## Rererence

[Pair Programming](https://extremeprogrammingalliance.com/about-extreme-programming-xp/extreme-programming-xp-practices/extreme-programming-xp-coding-technical-practices/)&mdash;Extreme Programming Alliance (XPA)

### Vibe Coding

[Vibe Coding](https://en.wikipedia.org/wiki/Vibe_coding)&mdash;Wikipedia

[Andrej Karpathy's  "vibe coding" post](https://x.com/karpathy/status/1886192184808149383?lang=en)&mdash;X

[Vibe Coding: The Shadow IT Problem No One Saw Coming](https://thenewstack.io/vibe-coding-the-shadow-it-problem-no-one-saw-coming/)&mdash;[Steve Fenton](https://thenewstack.io/author/steve-fenton/), The New Stack, 2025.

### GitHub Copilot

[GitHub Copilot Tutorials](https://github.com/features/copilot/tutorials)&mdash;GitHub.

[GitHub Copilot for VS Code Cheat Sheet](https://code.visualstudio.com/docs/copilot/reference/copilot-vscode-features)&mdash;GitHub.

[GitHub for Education](https://github.com/education)&mdash;Free Enterprise level account that includes GitHub Copilot.



Note: Parts of this document were drafted using Gemini Flash 2.5 (2025).

---

[![Creative Commons License](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/) Intro to AI Programming Course Materials by [Brian Bird](https://profbird.dev), written in <time>2025</time>, are licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/). 

---
