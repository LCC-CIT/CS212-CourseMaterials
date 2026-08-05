---
title: Lab 4, Group A
description: Instructions for doing classification with TensorFlow
keywords: classifier, TensorFlow, Keras
material: Lab Instructions
generator: Typora
author: Brian Bird
---

**CS 210, Intro to AI Programming**

<h1>Lab 4: TensorFlow with Keras</h1>

<h2>Group A</h2>

[TOC]

## Keras Image Classification with the CIFAR-10 Dataset

### Objective:

Your goal is to apply the exact same steps you learned in the "[Basic image classification](https://www.tensorflow.org/tutorials/keras/classification)" tutorial (which used the Fashion MNIST dataset) to a new, slightly more complex dataset: CIFAR-10.

This will test your understanding of:

- Loading a standard Keras dataset.
- Exploring and understanding the *shape* and *type* of your data.
- Adapting the model's first layer to match your new data's input shape.
- Building, compiling, training, and evaluating a basic neural network.

The New Dataset: CIFAR-10

The CIFAR-10 dataset is a "Hello, World" of computer vision. It contains 60,000 32x32 color images (50,000 training, 10,000 testing) divided into 10 classes:

- Airplane
- Automobile
- Bird
- Cat
- Deer
- Dog
- Frog
- Horse
- Ship
- Truck

### Instructions

Use a Google Colab notebook and follow the structure from the tutorial. Here is a step-by-step guide on how to adapt it.

Step 1: Import Libraries

This is the same as the tutorial. You'll need tensorflow (as tf), numpy, and matplotlib.pyplot.

Python

```
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
```

Step 2: Load the Data

Instead of fashion_mnist, you will import and load cifar10.

```python
# Load the CIFAR-10 dataset
cifar10 = tf.keras.datasets.cifar10
(train_images, train_labels), (test_images, test_labels) = cifar10.load_data()

# Define the class names for plotting
class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer',
               'dog', 'frog', 'horse', 'ship', 'truck']
```

Step 3: Explore the Data (CRITICAL STEP)

This is where you need to pay close attention. In the tutorial, the train_images had a shape of (60000, 28, 28). What is the shape of your new train_images?

- Find the `shape` of `train_images`.
- Find the `shape` of `train_labels`. Notice it's slightly different from Fashion MNIST's labels.
- Use `plt.imshow()` to look at the first image (`train_images[0]`). It will look colorful and pixelated.

Step 4: Preprocess the Data

This step is identical. The pixel values in CIFAR-10 also range from 0 to 255. You need to normalize them to a range of 0.0 to 1.0.

```python
# Normalize pixel values to be between 0 and 1
train_images, test_images = train_images / 255.0, test_images / 255.0
```

Step 5: Build the Model (THE MAIN CHALLENGE)

Now, you will build the exact same model architecture as the tutorial:

- A `Flatten` layer first
- A `Dense` layer with 128 neurons and `relu` activation
- A `Dense` layer with 10 neurons (for the 10 classes)

**Your challenge:** The `Flatten` layer in the tutorial used `input_shape=(28, 28)`. This will *not* work for your new data. Using the shape you found in Step 3, what should the `input_shape` be for your CIFAR-10 data?

```
# Build the model, replacing ??? with the correct input shape
model = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape=(???)),  # <-- YOU MUST CHANGE THIS LINE
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(10)
])
```

*Hint: A color image has three dimensions: (height, width, color_channels).*

Step 6: Compile the Model

This step is identical. The problem is still a multi-class classification, and the labels are integers (0-9), so the tutorial's optimizer and loss function are perfect.

Python

```
model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])
```

Step 7: Train the Model

This is identical. Train the model for 10 epochs and observe the accuracy.

Python

```python
model.fit(train_images, train_labels, epochs=10)
```

*Note: Don't be surprised if the accuracy is much lower than for Fashion MNIST! CIFAR-10 is a harder dataset, and this simple model will struggle. Getting 45-55% accuracy is normal for this model.*

Step 8: Evaluate Accuracy

This is identical. See how your model performs on the test set.

```python
test_loss, test_acc = model.evaluate(test_images, test_labels, verbose=2)
print('\nTest accuracy:', test_acc)
```

Step 9: Make Predictions

This is identical. Create the probability model by adding a Softmax layer and then use it to make predictions.

```python
probability_model = tf.keras.Sequential([model, tf.keras.layers.Softmax()])
predictions = probability_model.predict(test_images)

# You can now try to plot the predictions, just like in the tutorial!
# Make sure to use your new `class_names` list.
```

------



### Bonus Challenge (Optional, XC)

The simple model from the tutorial performs poorly on CIFAR-10. Can you improve it?

Try modifying **Step 5 (Build the Model)**. After the `Dense(128, activation='relu')` layer, try adding **another** `Dense` layer (e.g., 64 neurons, also with `relu` activation) before the final `Dense(10)` layer.

Does this new, "deeper" model get better accuracy?



## Submitting your lab work on Moodle

### Beta Version

- Post the beta version of your Jupyter Notebook file or a link to your Colab notebook in your team channel on Discord.

### Code Review

- Review one of your lab partners' code and post the review in your team channel on Discord.
- Submit a copy of the code review <u>you did</u> on the LMS.

### Production Version

 Based on the code review and helpful advice from your lab partners, you may revise your code. On the code review from your lab partner, complete the “Prod.” column to show what you revised. Upload the following to the *Lab Production Version* assignment on the LMS:

1. The Jupyter Notebook file (.Ipynb) or a link to your Google Colab notebook.
3. The code review <u>from your lab partner</u> with the “Prod.” column filled out by you.



## Grading Criteria

The main focus of grading will be on use of the sckit-learn classes and problem solving skills.



------

[![Creative Commons License](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/) AI Programming lab instructions by [Brian Bird](https://profbird.dev), written in <time>2025</time>, are licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/). 

------------

