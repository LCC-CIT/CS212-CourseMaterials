---
title: AI-Assisted Coding
description: How to use AI tools to help write code
keywords: AI-assisted coding, code generation
generator: Typora
author: Brian Bird
---

**CS 212, AI Programming 1**

<h1>AI-Assisted Coding</h1>

<h2>Contents</h2>

[TOC]

## What is AI-Assisted Coding

AI-assisted coding has the potential to significantly boost developer productivity by using AI as a *pair programmer* working directly in the development environment (e.g., CLI or IDE) to write code based on natural language prompts from the developer. The underlying Large Language Models (LLMs) then leverage their training on vast codebases to predict and generate entire functions, repetitive boilerplate code, or suggest code completions, to handle routine, time-consuming tasks. 

This assistance allows developers to accelerate debugging, quickly translate code between languages, and focus their time and effort on <u>higher-value activities</u> such as:

- Requirements gathering.
- Architectural design.
- Program design.
- Non-standard logic implementation.
-  Higher level problem-solving.
-  Verification.



### Maybe Don't Call It Vibe Coding

Vibe coding is a term that was originally used by Andrej Karpathy in <a href="https://x.com/karpathy/status/1886192184808149383?lang=en" target="_blank">a post on X</a> to describe his experience writing code using AI. The term caught on and became popular but then quickly fell into disfavor because it implies a casual, non-rigorous approach that prioritizes quick code generation based on a "vibe" rather than well thought out design and careful testing.

Critics argue it encourages thoughtless production of "AI slop", leading to:

- *Technical debt*.
- Security vulnerabilities.
- Code that is difficult to maintain or scale. 



## How to Code with AI without Making a Mess

AI coding agents can now write whole modules, not just suggest the next line. That changes the developer's job. You spend less time typing code and more time on the things the AI can't decide for you: what the software should do, how it should be organized, and whether it actually works.

A good way to picture this is a building project. The developer is the **architect and the inspector**, and the AI is the **construction crew**. The architect draws the plans and the crew builds. The inspector checks the work at key stages (the foundation, the framing, the wiring before the walls are closed up), when problems are still easy to see and fix. At the end, the owner does a final walkthrough before moving in.

You won't read every line the AI writes, but you are still <u>responsible for everything that ships</u>. Here's how you meet that responsibility in each of four stages, and how you manage the whole project.

### 1. Requirements: Write a Specification You Can Test

The developer gathers requirements from the people who will use the software and writes them down. AI can help you find gaps and questions you missed, but deciding what the software should do is your job.

- **Write user stories with acceptance criteria.** A user story says who wants what, and why. The acceptance criteria say how you'll know the story is done. For example:

  > **Story:** As a student, I want to see which assignments are due this week, so that I can plan my time.
  >
  > **Acceptance criteria:**
  >
  > - *Given* I have assignments due this week, *when* I open the app, *then* I see them listed in order of due date.
  > - *Given* I have no assignments due this week, *when* I open the app, *then* I see "Nothing due this week."
  > - *Given* an assignment is past due, *when* I open the app, *then* it is marked as late.

- **Include the non-functional requirements.** These are qualities the whole system needs, such as security, privacy, speed, and accessibility. The AI won't guess them, so write them down.
- **Keep the specification in the project repository,** where both you and the AI can read it. It's a living document: update it whenever users give you feedback.

### 2. Architecture: Design It Yourself, Then Refine It with AI

The developer plans the high-level design: the major components, how they connect (their interfaces), and how data flows between them.

- **Use AI as a design partner.** Once you have a draft, ask the AI to critique it: "What are the weaknesses of this design?" or "What would be hard to change later?" You make the final decisions.
- **Write your guidance where the AI will read it.** Coding agents read an instruction file at the start of every session, such as `AGENTS.md`, `CLAUDE.md`, or `.github/copilot-instructions.md`. Put your coding standards, project layout, and design rules there (e.g., "Always use `snake_case` for variables," or "All database access goes through the `storage` module").
- **Record important decisions** and the reasons for them in a short note in the repository. This helps the AI (and your teammates) keep the design consistent as the project grows.

### 3. Module Coding: Guide the AI and Inspect at Key Points

Let the AI write the module-level code, but steer it and check its work.

- **Give it one well-defined task at a time.** Break the work into tasks small enough to finish in one session, and start a fresh session for each new task. Ask the AI for a plan before it writes any code (many tools have a *plan mode* for this).
- **Spot-check where the risks are.** You can't review everything, so focus on:
  - **Boundaries between modules:** Does the code use the interfaces you designed? Is it following the architecture, or quietly working around it?
  - **Security, and actions that can't be undone:** logins, user input, passwords and keys, deleting data, payments.
  - **New dependencies:** Did the AI add a package you don't need, or one that doesn't exist? Attackers publish fake packages under the names AI tools tend to make up (this is called *slopsquatting*).
  - **The tests:** AI sometimes makes a failing test pass by weakening it, skipping it, or adding special-case code just for that test. Reviewing the tests is often more useful than reviewing the code.
- **Get a second opinion from a different model.** Different models tend to miss different things, so have another AI review the code. A fresh session that didn't write the code also helps. AI reviewers often flag things that aren't real problems, so you decide which findings matter.
- **Let tools check what tools are good at.** Linters, type checkers, and security scanners can run automatically every time you push code. That frees your attention for the bigger question: does this do what the specification says?
- **Use version control.** Commit often and keep each feature on its own branch. Small changes are easier to review, and easy to undo if something goes wrong.

### 4. Verification and Acceptance Testing

This is the final check that the software does what the specification says, and it's where your own judgment matters most.

- **Write the test cases from the acceptance criteria, before the code.** You decide what to test and what the right results are; the AI can write the code for the tests. If the AI writes both the program and its tests on its own, both may share the same misunderstanding of the requirements, and the tests will pass anyway.
- **Test the critical parts yourself, by hand.** Try the main things users will do, the security-sensitive features, and anything that could lose or damage data. Then try to break it with unusual inputs, empty fields, and steps done out of order.
- **Check against the specification.** Go through each user story's acceptance criteria. A story is done only when all of them pass.

### Managing the Project: Agile Development with AI

Most software teams use an agile process such as Scrum, where software is built in short cycles called *sprints* (usually one to four weeks). When you work with AI, you are the one who sets up and runs this process as part of your development plan:

- **Product backlog:** a prioritized list of user stories with acceptance criteria. This is your specification from stage 1.
- **Sprint planning:** choose the stories for the next sprint and break them into tasks for the AI.
- **Sprint review:** show the working software to users, collect their feedback, and update the backlog.
- **UX testing:** at several points in the project, watch real users try the software. They will find problems that neither you nor the AI thought of.

AI changes the pace of this cycle. When code is fast to write, the slow part becomes getting feedback and making decisions. That has two effects:

- **Prototypes are cheap,** so you can put something in front of users early and often, even a rough version you plan to throw away.
- **It's easy to build faster than users can try things.** Don't let features pile up that no real user has tested.

### Why You Still Need to Learn to Code

If the AI writes most of the code, why learn to program? Because every stage above depends on it. You can't judge an architecture, spot-check a module, understand a failing test, or take over when the AI gets stuck going in circles unless you can read and understand code. Knowing how to program is what makes you the architect and the inspector, rather than a bystander.

Working this way is the opposite of "vibe coding." The AI does most of the building, and you are the engineer who decides what gets built, checks that it's built right, and answers for the result.



## Reference

<a href="https://extremeprogrammingalliance.com/about-extreme-programming-xp/extreme-programming-xp-practices/extreme-programming-xp-coding-technical-practices/" target="_blank">Pair Programming</a>&mdash;Extreme Programming Alliance (XPA)

### Vibe Coding

<a href="https://en.wikipedia.org/wiki/Vibe_coding" target="_blank">Vibe Coding</a>&mdash;Wikipedia

<a href="https://x.com/karpathy/status/1886192184808149383?lang=en" target="_blank">Andrej Karpathy's  "vibe coding" post</a>&mdash;X

<a href="https://thenewstack.io/vibe-coding-the-shadow-it-problem-no-one-saw-coming/" target="_blank">Vibe Coding: The Shadow IT Problem No One Saw Coming</a>&mdash;<a href="https://thenewstack.io/author/steve-fenton/" target="_blank">Steve Fenton</a>, The New Stack, 2025.

### Agile Development and Specifications

<a href="https://scrumguides.org/scrum-guide.html" target="_blank">The Scrum Guide</a>&mdash;Ken Schwaber and Jeff Sutherland.

<a href="https://www.agilealliance.org/glossary/acceptance/" target="_blank">What is Acceptance Testing?</a>&mdash;Agile Alliance.

<a href="https://adr.github.io/" target="_blank">Architectural Decision Records (ADRs)</a>&mdash;ADR GitHub organization.

### AI Coding Agents

<a href="https://agents.md/" target="_blank">AGENTS.md</a>&mdash;An open format for giving instructions to coding agents.

<a href="https://en.wikipedia.org/wiki/Slopsquatting" target="_blank">Slopsquatting</a>&mdash;Wikipedia

### GitHub Copilot

<a href="https://github.com/features/copilot/tutorials" target="_blank">GitHub Copilot Tutorials</a>&mdash;GitHub.

<a href="https://code.visualstudio.com/docs/copilot/reference/copilot-vscode-features" target="_blank">GitHub Copilot for VS Code Cheat Sheet</a>&mdash;GitHub.

<a href="https://github.com/education" target="_blank">GitHub for Education</a>&mdash;Free Enterprise level account that includes GitHub Copilot.



*Parts of this document were drafted using Gemini Flash 2.5 (2025) and revised using Claude Opus 5.5 (2026).*

---

<a href="http://creativecommons.org/licenses/by-sa/4.0/" target="_blank"><img src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" alt="Creative Commons License"></a> AI Programming 1 Course Materials by <a href="https://profbird.dev" target="_blank">Brian Bird</a>, written in 2025, revised in <time>2026</time>, are licensed under a <a href="http://creativecommons.org/licenses/by-sa/4.0/" target="_blank">Creative Commons Attribution-ShareAlike 4.0 International License</a>. 

---
