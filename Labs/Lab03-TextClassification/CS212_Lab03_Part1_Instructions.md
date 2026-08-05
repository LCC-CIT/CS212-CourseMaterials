---
title: Lab 3, Part 1
description: Part 1 of the assignment is to do the scikit-learn "Working with Text Data Tutorial"
keywords: scikit-learn
material: Lab Instructions
generator: Typora
author: Brian Bird
---

**CS 210, Intro to AI Programming**

<h1>Lab 3, Text Classification</h1>

<h2>Part 1</h2>

This part of the lab is for everyone.

Do these parts of the "[Working with Text Data](https://lcc-cit.github.io/CS210-CourseMaterials/Tutorials/scikit-learn-1.7/WorkingWithTextData.html)" scikit-learn tutorial in the interactive Python interpreter (Command line):

- Tutorial setup
- Building Feature Vectors and Training
- Building a Pipeline
- Testing Classification Accuracy
- Fine Tuning Hyperparameters with a Grid Search

Wiite a .py file that <u>only includes the essential steps</u> to:

- Fetch the training data

- Build a feature vector matrix

- Train the classifier (without using a pipeline)

- Test the classifier
  
  - Use test data from  
    
    ```Python
    twenty_test = fetch_20newsgroups(subset='test',  categories=categories, shuffle=True, random_state=42)
    ```
  
  - Print the average (mean) accuracy of the classifier

You don't need to build a pipeline or do a grid search.

To make this interesting, you can use a different set of newsgroup categories from the ones used in the tutorial.

## Part 2

There will be three versions of part 2. The instructions will be in separate documents.

## Submitting your lab work on Moodle

Upload the one file to the Lab 3, Part 1 assignment link. 
You only need to submit your code. You <u>do not</u> need to upload your virtual environment (.venv) folder.

(No code review is needed)

### Grading Criteria

The main focus of grading will be on correct coding and problem solving skills.
