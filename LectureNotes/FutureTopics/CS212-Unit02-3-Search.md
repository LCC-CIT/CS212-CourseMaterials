---
title: Unit 1 Overview
description: What's AI
keywords: Classical AI, Symbolic AI, GOFAI
generator: Typora
author: Brian Bird
---

**CS 210, Intro to AI Programming**

<h1>Symbolic AI: Search-Based Techniques</h1>

| Topics                                   |                           |
| ---------------------------------------- | ------------------------- |
| 1. What is AI, Python                    | 6. ANN: Image recognition |
| 2.  <mark>Symbolic AI</mark>             | 7. Generative AI          |
| 3. Classical Machine Learning: Training  | 8. Custom chatbot         |
| 3. Classical Machine Learning: Inference | 9. LLM fine-tuning        |
| 5. Midterm                               | 10. Ethics                |
|                                          | 11. Final                 |

<h2>Contents</h2>

[toc]



## Review

- John McCarthy, a mathematics professor at Dartmouth College coined the term *Artificial Intelligence* in 1956.
- Categories of AI
  (There are other categories, but these are some of the major ones.)

  - Symbolic (GOFAI)
    - Rule-based, expert systems
    - Search-based


  - Machine Learning
    - Statistical
    - ANN (Artificial Neural Networks)


## Symbolic AI

- Last time, we briefly discussed expert systems as an example of rule-based systems. You wrote a "toy" version of an expert system.
- This time we will explore search-based systems and you will write a problem solving "AI" system using this approach.

## Search

Many problems can be thought of as search problems. We normally think of searching as a way to solve problems like finding a web site, finding a book in a library, or finding a product in an online store. But search can also be used to find the shortest route on a road map or the best sequence of moves to win a game.

Search techniques are now usually considered simply part of Computer Science rather than AI, but "back in the day", they were considered AI and are still a useful way to solve a problem. There are three broad categories of search algorithms we will look at:

### State-space search

Search for an optimal set of steps to reach a particular configuration given a set of constraints.

- **Airline example**: an airline needs to find the optimal assignment of flights for its fleet of aircraft. This process involves:

  - Planning all flight legs and ensuring they have adequate turnaround time at airports.  

  - Assigning a specific type of plane to a sequence of flights that starts and ends at a maintenance base.  

  The entire operation is governed by constraints, including federal aviation regulations on pilot duty hours, mandatory maintenance schedules, airport noise curfews, and crew schedules. The ultimate goal is to to minimize the time aircraft are sitting idle on the ground and maximize profit. 

- **Zombie and human river crossing puzzle**: Three humans and three zombies are on one side of a river. They all need to get to the other side. There is one rowboat.

  - The boat can only carry two of them for each crossing.
  - At least one of them has to be in the boat to row it.
  - Only the boat can be used to cross the river (no wading or swimming).
  - If the zombies on either side of the river outnumber the humans, they will kill them.

  Here is a solution to the [Zombies and humans river crossing problem](https://lcc-cit.github.io/CS123-CourseMaterials/LectureNotes/Topic-01-4-ZombieCrossingSolution.html) with a description of the state-space and the steps to get from the initial state-space configuration to the state-space configuration that is the goal.

  

## Search for an Optimal Route



Note: Parts of this document were initially drafted with assistance from Gemini 2.5 Flash


---



[![Creative Commons License](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/) Intro to AI Course Materials by [Brian Bird](https://profbird.dev), written in <time>2025</time>, are licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/). 

[^1]: [Dartmouth workshop](https://en.wikipedia.org/wiki/Dartmouth_workshop)&mdash;Wikipedia
