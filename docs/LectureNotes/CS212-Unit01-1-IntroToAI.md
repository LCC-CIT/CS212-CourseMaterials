---
title: Unit 1 Overview
description: What's AI
keywords: Classical AI, Symbolic AI, GOFAI
generator: Typora
author: Brian Bird
---

**CS 212, AI Programming 1**

<h1>Overview of AI</h1>



<h2>Contents</h2>

- [What is AI?](#what-is-ai)
- [John McCarthy and the Dartmouth Workshop](#john-mccarthy-and-the-dartmouth-workshop)
    - [McCarthy's Definition of AI](#mccarthys-definition-of-ai)
- [Classical Symbolic AI (GOFAI)](#classical-symbolic-ai-gofai)
- [A Modern Definition](#a-modern-definition)
    - [Analysis of the modern definition](#analysis-of-the-modern-definition)
- [Categories of AI](#categories-of-ai)
- [What We'll Cover in this Course](#what-well-cover-in-this-course)

## What is AI?

## John McCarthy and the Dartmouth Workshop

John McCarthy was a mathematics professor at Dartmouth College who coined the term *Artificial Intelligence*.

- He and his colleagues convened the Dartmouth Summer Research Project on Artificial Intelligence in 1956. [^1]

- The workshop was based on the idea that: "Every aspect of learning or any other feature of  intelligence can in principle be so precisely described that a machine can be made to simulate it."
- This workshop is considered the founding event for AI research as a distinct field of study.

#### McCarthy's Definition of AI

- McCarthy defined AI as "the science and engineering of making intelligent machines, especially intelligent computer programs"[^2]

## Classical Symbolic AI (GOFAI)

One of the major approaches to AI in the mid-twentieth century was to use rules and logic to make decisions. This approach was later labeled "Good Old Fashioned AI"(GOFAI)[^4] by John Haugeland[^5] , a professor at the University of Chicago.

In the GOFAI age, an algorithm was considered "AI" if it successfully used explicit rules (selection statements, look-up tables, etc.) to manipulate high-level, human-readable *symbols* like `IF (animal has feathers) AND (animal can fly) THEN (animal is a bird)`.

## A Modern Definition

From the United States National Artificial Intelligence Initiative Act of 2020[^6]:

> The term "artificial intelligence" means a machine-based system that can, for a given set of human-defined objectives, make ***predictions***, ***recommendations*** or ***decisions*** influencing real or virtual environments. Artificial intelligence systems use machine and human-based inputs to:
>
> (A) ***perceive*** real and virtual environments;
>
> (B) ***abstract*** such perceptions into models through analysis in an automated manner; and
>
> (C) use model ***inference*** to formulate options for information or action.

#### Analysis of the modern definition

This definition raises the bar by implying that *machine learning* is an essential part of AI.

1. It describes things that AI systems do:

   - Predict

   - Recommend

   - Decide

   Q: Can you think of some examples of systems using AI that does one or more of these things?

2. It describes the way AI systems do it:

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

- Intro/review of Python.
- Simplified symbolic AI as a way to practice Python.
- Statistical machine learning with the Python Scikit Learn library.
- ANNs with TensorFlow, image recognition.
- Generative AI
  - Use AI to write code.
  - Using a chat completion API to add AI to an application.
  - Use MCP to enable AI to use tools (other applications).



*Note: Parts of this document were drafted with assistance from Gemini 2.5 Flash*


---



<a href="http://creativecommons.org/licenses/by-sa/4.0/" target="_blank"><img src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" alt="Creative Commons License"></a> AI Programming 1 Course Materials by <a href="https://profbird.dev" target="_blank">Brian Bird</a>, written in <time>2025</time>, revised in 2026 are licensed under a <a href="http://creativecommons.org/licenses/by-sa/4.0/" target="_blank">Creative Commons Attribution-ShareAlike 4.0 International License</a>. 

[^1]: <a href="https://en.wikipedia.org/wiki/Dartmouth_workshop" target="_blank">Dartmouth workshop</a>&mdash;Wikipedia
[^2]: <a href="http://jmc.stanford.edu/artificial-intelligence/what-is-ai/#:~:text=Q.,methods%20that%20are%20biologically%20observable." target="_blank">What is AI? / Basic Questions</a>&mdash;Professor John McCarthy, Father of AI Website
[^3]: <a href="https://law.justia.com/codes/us/2021/title-15/chapter-119/sec-9401/#:~:text=SUBSIDIARIES%20SHORT%20TITLE-,Pub.,Title" target="_blank">2021 U.S. Code Title 15 - Commerce and Trade Chapter 119 - National Artificial Intelligence Initiative Sec. 9401 - Definitions</a>&mdash;Justia web site
[^4]: <a href="https://en.wikipedia.org/wiki/GOFAI" target="_blank">GOFAI</a>&mdash;Wikipedia
[^5]: <a href="https://direct.mit.edu/books/book/4347/Artificial-IntelligenceThe-Very-Idea" target="_blank">*Artificial Intelligence: The Very Idea*</a>, John Haugeland, 1989, MIT Press.
[^6]: <a href="https://science.house.gov/bills?ID=34889C3E-C675-4EAF-B50F-880C05EB753B" target="_blank">National Artificial Intelligence Initiative Act of 2020</a>



