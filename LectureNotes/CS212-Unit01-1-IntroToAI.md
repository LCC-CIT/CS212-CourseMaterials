---
title: Unit 1 Overview
description: What's AI
keywords: Classical AI, Symbolic AI, GOFAI
generator: Typora
author: Brian Bird
---

**CS 210, Intro to AI Programming**

<h1>Overview of AI</h1>



| Topics                                   |                           |
| ---------------------------------------- | ------------------------- |
| <mark>1. What is AI</mark>, Python       | 6. ANN: Image recognition |
| 2.  Symbolic AI                          | 7. Generative AI          |
| 3. Classical Machine Learning: Training  | 8. Custom chatbot         |
| 4. Classical Machine Learning: Inference | 9. LLM fine-tuning        |
| 5. Midterm                               | 10. Ethics                |
|                                          | 11. Final                 |



<h2>Contents</h2>

[TOC]

## What is AI?

## John McCarthy and the Dartmouth Workshop

John McCarthy was a mathematics professor at Dartmouth College who coined the term *Artificial Intelligence*.

- He and his colleagues convened the Dartmouth Summer Research Project on Artificial Intelligence in 1956. [^1]

- The workshop was based on the idea that: "Every aspect of learning or any other feature of  intelligence can in principle be so precisely described that a machine can be made to simulate it."
- This workshop is considered the founding event for AI research as a distinct field of study.

#### McCarthy's Definition of AI

- McCarthy defined AI as "the science and engineering of making intelligent machines, especially intelligent computer programs"[^2]

## Classical Symbolic AI (GOFAI)

One of the major approaches to AI in the mid-twentieth century was to use rules and logic to make decisions. This approach was later labeled "Good Old Fashioned AI"[^4] by John Haugeland[^5] , a professor at the University of Chicago.

In the GOFAI age, an algorithm was considered "AI" if it successfully used explicit rules (selection statements, logical predicates, etc.) to manipulate high-level, human-readable *symbols* like `IF (animal has feathers) AND (animal can fly) THEN (animal is a bird)`.

## A Modern Definition

From the United States National Artificial Intelligence Initiative Act of 2020:

> The term "artificial intelligence" means a machine-based system that can, for a given set of human-defined objectives, make predictions, recommendations or decisions influencing real or virtual environments. Artificial intelligence systems use machine and human-based inputs to—
>
> (A) perceive real and virtual environments;
>
> (B) abstract such perceptions into models through analysis in an automated manner; and
>
> (C) use model inference to formulate options for information or action.

#### Analysis of the modern definition

This definition raises the bar by implying that *machine learning* an essential part of AI.

It describes things that AI systems do:

- Predict
- Recommend
- Decide

It describes the way AI systems do it:

- Perception, i.e. getting input. This input could be in the form of a file containing: text, an image, sound or other data. It could also be input from sensors or input devices: camera, microphone, temperature sensor, etc.
- Abstract perception into models. This is what is usually called *training* a model.
- Inference. This means running a program that uses the model to do something.



## Categories of AI

For the purposes of this class, we will categorize the different approaches to AI as:

- Symbolic (GOFAI)
- Machine Learning
  - Statistical
  - ANN (Artificial Neural Networks)

## What We'll Cover in this Course

Our main focus in this course will be on machine learning. But first we will review Python and write some simplified symbolic AI code. 

Here is an outline of what we'll cover:

- Intro/review of Python
- Simplified symbolic AI as a way to practice Python
- Statistical machine learning with the Python Scikit Learn library
- ANNs with TensorFlow, image recognition
- Generative AI
  - Creating a custom chatbot (Gemini Gem)
  - Using the chat completion API (Google Gemini)
  - Fine-tuning an LLM



Note: Parts of this document were drafted with assistance from Gemini 2.5 Flash


---



[![Creative Commons License](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/) Intro to AI Programming Course Materials by [Brian Bird](https://profbird.dev), written in <time>2025</time>, are licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/). 

[^1]: [Dartmouth workshop](https://en.wikipedia.org/wiki/Dartmouth_workshop)&mdash;Wikipedia
[^2]: [What is AI? / Basic Questions](http://jmc.stanford.edu/artificial-intelligence/what-is-ai/#:~:text=Q.,methods%20that%20are%20biologically%20observable.)&mdash;Professor John McCarthy, Father of AI Website
[^3]: [2021 U.S. Code Title 15 - Commerce and Trade Chapter 119 - National Artificial Intelligence Initiative Sec. 9401 - Definitions](https://law.justia.com/codes/us/2021/title-15/chapter-119/sec-9401/#:~:text=SUBSIDIARIES%20SHORT%20TITLE-,Pub.,Title)&mdash;Justia web site
[^4]: [GOFAI](https://en.wikipedia.org/wiki/GOFAI)&mdash;Wikipedia
[^5]: [*Artificial Intelligence: The Very Idea*](https://direct.mit.edu/books/book/4347/Artificial-IntelligenceThe-Very-Idea), John Haugeland, 1989, MIT Press.



