---
title: Lab 3, Part 1
description: Part 1 of the assignment is to do the scikit-learn "Working with Text Data Tutorial"
keywords: scikit-learn
material: Lab Instructions
generator: Typora
author: Brian Bird
---

**CS 212, AI Programming 1**

# Lab 3, Text Classification

## Part 1

This part of the lab is for everyone.

### Step A: Do the Tutorial

- Work through the scikit-learn tutorial: [Working with Text Data](https://lcc-cit.github.io/CS212-CourseMaterials/Tutorials/scikit-learn-1.7/WorkingWithTextData.html) . 
  Read it, run the code and check the results at each step so you understand what the code is doing. Adding code that prints variables is a great way to do this. (There are already quite a few lines of code that are just there to show you what the program is doing.)

- You have two choices for the way you do the tutorial:

  - Copy the code from the tutorial web page into an interactive Python interpereter (as suggested in the tutorial.)
    -- OR --

  - Run the code in this [Jupyter notebook on Google Colab](https://colab.research.google.com/drive/1FBrABO2L1DFKRn1v0zRknHS57eiktzgm?usp=sharing).

- You don't need to do the exercises at the end of the tutorial... yet. (Groups A and B will do them for part 2. Group C has a different exercise.)

### Step B: Put the Essential Parts of the Tutorial in a Python File

Write a .py file that <u>only includes the essential steps</u> to:

- Fetch the training data

- Build a feature vector matrix

- Train the classifier (without using a pipeline)

- Test the classifier
  
  - Use test data from  
    
    ```Python
    twenty_test = fetch_20newsgroups(subset='test',  categories=categories, shuffle=True, random_state=42)
    ```
  
  - Print the average (mean) accuracy of the classifier

<u>You don't need to build a pipeline or do a grid search</u>.

**Alternative:** To make this interesting, you can use a different set of newsgroup categories than the ones used in the tutorial.



## Part 2

There are three versions of part 2. 

- [Group A: Language Identification Using a Text Classifier](GroupA/CS212_Lab03_Part2_Instructions_GroupA.html)
- [Group B: Sentiment Analysis on Movie Reviews](GroupB/CS212_Lab03_Part2_Instructions_GroupB.html)
- [Group C: Predicting Star Ratings from Movie Reviews](GroupC/CS212_Lab03_Part2_Instructions_GroupC.html)


### Code Review

- Review one of your lab partners' code for part 2 and post the review in your team channel on Discord.
- Submit a copy of the code review <u>you did</u> to the code review assignment on Canvas.

## Submitting your lab work on Canvas

Zip and upload your Python code files to the Lab 3 Production Version  assignment on Canvas. 
You only need to submit your code. You <u>do not</u> need to upload your virtual environment (.venv) folder or any data.



### Grading Criteria

The main focus of grading will be on correct coding and problem solving skills.
