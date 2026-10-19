---
title: Python Crash Course
description: A guide to the Python lecture notes in CS 212, with links and a short summary of each one.
keywords: Python, crash course, collections, loops, venv, uv, PEP 8
generator: Typora
author: Brian Bird
---

<h1>Python Crash Course</h1>

**CS 212 AI Programming 1**

## Introduction

In this course we write all of our AI programs in Python. You don't need to be a Python expert to get started. If you already know another programming language, such as JavaScript, C#, or Java, most of what you know carries over, and you mainly need to learn Python's syntax and a few of its distinctive features.

The Python notes for this course are spread across several units. This page lists them all in one place, in the order we suggest reading them. Each note is short and focused, so you can read the whole set like a crash course, or come back to a single note when you need a refresher.

## The Python Notes

1. **[Intro to Python](https://lcc-cit.github.io/CS212-CourseMaterials/LectureNotes/CS212-Unit01-1-Python.html)**
   How to install Python on Windows and macOS, run a "Hello World" program, and use VS Code and its debugger. It also covers what makes Python different from C-family languages (indentation instead of curly braces, dynamic typing, no semicolons), Python's programming paradigms, an object-oriented example, and a "die battle" exercise to translate into Python.

2. **[Python Coding Style Cheat-Sheet](https://lcc-cit.github.io/CS212-CourseMaterials/LectureNotes/PythonCodingStyleCheatSheet.html)**
   A one-page summary of the PEP 8 style guide: indentation and line length, naming conventions (`snake_case`, `CapWords`, `ALL_CAPS`), comments, whitespace, docstrings, imports, and blank lines. Use it to make your code look *pythonic*.

3. **[Python Collection Types](https://lcc-cit.github.io/CS212-CourseMaterials/LectureNotes/CS212-Unit02-3-PythonCollectionTypes.html)**
   The four built-in collection types: lists, dictionaries, sets, and tuples. Each one has a table showing its syntax, ordering, mutability, and whether it allows duplicates, plus examples. It also explains how to use `dict.get()` to look up a key safely.

4. **[Python Loops](https://lcc-cit.github.io/CS212-CourseMaterials/LectureNotes/CS212-Unit02-4-PythonLoops.html)**
   How to use `for` loops to go through a sequence (including `range()`), how to use `while` loops to repeat code while a condition is true, and how `break`, `continue`, and a loop's `else` clause change the flow of a loop.

5. **[Python Projects](https://lcc-cit.github.io/CS212-CourseMaterials/LectureNotes/CS212-Unit02-5-PythonProjects.html)**
   Why each project needs its own virtual environment, and how to manage environments and packages in two ways: with Python's built-in `venv` and `pip` tools (including `requirements.txt`), and with `uv`, the project manager we use in this course. It also explains `pyproject.toml`, the `uv.lock` file, using environments in VS Code, and how to fix common problems.

6. **[Set Up Python Packages for ML](https://lcc-cit.github.io/CS212-CourseMaterials/LectureNotes/SetUpPythonAndLibrariesForAI.html)**
   An introduction to the machine learning libraries we'll use later in the course (NumPy, scikit-learn, TensorFlow with Keras, Pillow, and Matplotlib), with instructions for installing them in a virtual environment on Windows and macOS.

## More Python Resources

- <a href="https://docs.python.org/3/tutorial/" target="_blank">The Python Tutorial</a>&mdash;Official Python web site
- <a href="https://www.w3schools.com/python/" target="_blank">Python Tutorial</a>&mdash;W3Schools

---

*Note: This page was drafted with assistance from Claude Opus 5.5 10/19/2026*

---

<a href="http://creativecommons.org/licenses/by-sa/4.0/" target="_blank"><img src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" alt="Creative Commons License"></a> AI Programming Course Materials by <a href="https://profbird.dev" target="_blank">Brian Bird</a>, written in <time>2026</time> are licensed under a <a href="http://creativecommons.org/licenses/by-sa/4.0/" target="_blank">Creative Commons Attribution-ShareAlike 4.0 International License</a>.

---
