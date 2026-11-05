---
title: TensorFlow
description: Intro to TensorFlow
keywords: AI, ML, ANN
generator: Typora
author: Brian Bird
---

<h1>TensorFlow</h1>

**CS 212, AI Programming 1**

<h2>Contents</h2>

[TOC]

## What is TensorFlow?

Adapted from Wikipedia:

> TensorFlow is a  machine learning platform that can be used across a wide range of tasks, but is used mainly for <a href="https://en.wikipedia.org/wiki/Types_of_artificial_neural_networks#Training" target="_blank">training</a> and <a href="https://en.wikipedia.org/wiki/Statistical_inference" target="_blank">inference</a> of <a href="https://en.wikipedia.org/wiki/Neural_network_(machine_learning)" target="_blank">neural networks</a>. It is one of the most popular <a href="https://en.wikipedia.org/wiki/Deep_learning" target="_blank">deep learning</a> frameworks, alongside others such as <a href="https://en.wikipedia.org/wiki/PyTorch" target="_blank">PyTorch</a>. It is free and open-source software released under the <a href="https://en.wikipedia.org/wiki/Apache_License_2.0" target="_blank">Apache License 2.0</a>.
>
> It was developed by the <a href="https://en.wikipedia.org/wiki/Google_Brain" target="_blank">Google Brain</a> team for Google's internal use in research and production. The initial version was released in 2015. Google released an updated version, TensorFlow 2.0, in September 2019.
>
> TensorFlow can be used with a wide variety of programming languages, including <a href="https://en.wikipedia.org/wiki/Python_(programming_language)" target="_blank">Python</a>, <a href="https://en.wikipedia.org/wiki/JavaScript" target="_blank">JavaScript</a>, <a href="https://en.wikipedia.org/wiki/C%2B%2B" target="_blank">C++</a>, [C#](https://dotnet.microsoft.com/en-us/apps/ai/ml-dotnet#extensibility) and <a href="https://en.wikipedia.org/wiki/Java_(programming_language)" target="_blank">Java</a>, facilitating its use in a range of applications in many sectors.
>

## What It Can Do

- **Computer Vision and Image Processing:** Handling image classification, object detection in self-driving cars, facial recognition, and medical scan analysis using Convolutional Neural Networks (CNNs).
- **Natural Language Processing (NLP)**: Powering text translation, sentiment analysis, chatbots, and Large Language Models (LLMs) using Recurrent Neural Networks (RNNs) and Transformers.
- **Time-Series Forecasting**: Predicting stock market trends, weather patterns, and supply chain demands.
- **Generative AI**: Powering Generative Adversarial Networks (GANs) and diffusion models to create entirely new art, audio, or text.
- **Tabular Data Analysis**: Running traditional machine learning algorithms like regression, decision trees, and clustering for financial fraud detection or customer churn prediction.
- **Reinforcement Learning**: Training AI agents to play video games, control robotics, or navigate autonomous vehicles through specialized libraries like TF-Agents.

## The  TensorFlow Ecosystem

TensorFlow is considered a "platform" because it handles the entire life-cycle of a machine learning model, from data preparation to production:

| Component                     | What It Does                                                 |
| ----------------------------- | ------------------------------------------------------------ |
| **tf.data**                   | Handles massive datasets and builds efficient input pipelines. |
| **TensorBoard**               | A visualization toolkit to track and log metrics like loss and accuracy during training. |
| **LiteRT (formerly TF Lite)** | Compresses and deploys models directly onto mobile phones, IoT gadgets, and edge devices. |
| **TensorFlow.js**             | Allows developers to train and run machine learning models directly inside a web browser using JavaScript. |
| **TFX (TensorFlow Extended)** | An enterprise-grade pipeline for deploying and managing production-scale machine learning workflows. |



## Reference

### Articles and Tutorials

<a href="https://en.wikipedia.org/wiki/TensorFlow" target="_blank">TensorFlow</a>&mdash;Wikipedia

<a href="https://www.tensorflow.org/tutorials" target="_blank">TensorFlow Tutorials</a>&mdash;Official TensorFlow documentation

### Interactive Web Pages

<a href="http://playground.tensorflow.org/" target="_blank">Tensorflow Playground</a>&mdash;Tinker with a neural network in your browser.

- <a href="https://cloud.google.com/blog/products/ai-machine-learning/understanding-neural-networks-with-tensorflow-playground" target="_blank">Understanding neural networks with TensorFlow Playground</a>&mdash;Kaz Sato, Google Cloud, 2016.



---

<a href="http://creativecommons.org/licenses/by-sa/4.0/" target="_blank"><img src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" alt="Creative Commons License"></a> AI Programming 1 lecture notes by <a href="https://profbird.dev" target="_blank">Brian Bird</a>, written in 2025, revised in <time>2026</time> are licensed under a <a href="http://creativecommons.org/licenses/by-sa/4.0/" target="_blank">Creative Commons Attribution-ShareAlike 4.0 International License</a>. 

---