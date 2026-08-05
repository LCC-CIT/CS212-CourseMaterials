---
title: Artificial Neural Networks
description: Overview of ANNs (Artificial Neural Networks)
keywords: AI, ML, ANN
generator: Typora
author: Brian Bird
---

<h1>Convolutional Neural Netoworks (CNNs)</h1>

**CS 210, Intro to AI Programming**

| Topics                                          |                                                              |
| ----------------------------------------------- | ------------------------------------------------------------ |
| 1. What is AI, Python                           | 6. <mark>Artificial Neural Networks: Image recognition</mark> |
| 2.  Symbolic AI: rule-based                     | 7. Generative AI                                             |
| 3.  Classical Machine Learning<br />Bayes' Rule | 8. Custom chatbot                                            |
| 4. ML: scikit-learn<br />Working with Data Sets | 9. LLM fine-tuning                                           |
| 5. ML: Scikit Learn Part 2                      | 10. Ethics                                                   |

<h2>Table of Contents</h2>

[TOC]

## Convolutional Neural Networks (CNN)

When we tried to assign weights to an ANN that classified happy and sad faces, we discovered that the ANN had difficulty with:

- Different sizes of faces
- Faces that were positioned higher or lower in the input grid
- Features (mouth size and position) that varied from face to face

CNNs resolves these problems and more using a *convolution operation*. This operation involves sliding a filter  over the input data and performing element-wise multiplication followed by a sum. This process helps in extracting features from the input.

Here is a simplified description of the process (provided by MS Copilot):

> Think of an image as a large field of different colored flowers. Now, suppose you want to identify patterns or features in this field, like areas of certain colors or color combinations.
>
> The convolution operation is like using a small magnifying glass to look at one small area of the field at a time. This magnifying glass is what we call a "filter" or "kernel" in a Convolutional Neural Network (CNN).
>
> As you move the magnifying glass across the field (or the image), you're focusing on one small area at a time. For each area, you're asking, "What's interesting here?" The answer could be "a lot of red flowers," "mostly blue flowers," "a mix of red and blue flowers," and so on. These are the "features" that the filter is learning to recognize.
>
> The interesting thing is, you use the same magnifying glass (the same filter) to look at the entire field. This means you're looking for the same kind of features everywhere in the image. This is what gives CNNs their power: they can recognize the same features no matter where they appear in the image.
>
> In summary, the convolution operation in a CNN is like using a magnifying glass to systematically scan across an image, looking for interesting features one small area at a time.

### History of CNN Development

Convolutional Neural Networks (CNNs) were first developed and used in the 1980s. The foundational work was done by Kunihiko Fukushima and Yann LeCun. 

Yann LeCun, in 1989, proposed a neural network architecture known as LeNet-5. This was the first successful implementation of a network that utilized the backpropagation algorithm for training, which is a standard method for training CNNs today. LeNet-5 was used for digit recognition tasks.

The significant breakthrough in the field of CNNs came in 2012 with the development of AlexNet by Alex Krizhevsky. AlexNet significantly outperformed previous image recognition algorithms and won the 2012 ImageNet contest with 85% accuracy. 



## Reference

### Articles and Tutorials



### Interactive Web Pages

[CNN Explainer](https://poloclub.github.io/cnn-explainer/)



[^1]: Marvin Minsky, in collaboration with Dean Edmonds, developed the first artificial neural network in 1951, known as the Stochastic Neural Analog Reinforcement Calculator (SNARC). It was not implemented in software and did not use a computer. Its 40 artificial neurons were built with mechanical and electronic components. It was about the size of a grand piano and included a plugboard for interconnecting the neurons. It was designed for a single task: to learn a path through a maze using Hebbian Learning.

---

[![Creative Commons License](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/) Intro to AI Programming lecture notes by [Brian Bird](https://profbird.dev), written in 2024, revised in <time>2025</time>, are licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/). 

Note: GPT-4 and GPT-4o were used to draft parts of these notes, July 2024.