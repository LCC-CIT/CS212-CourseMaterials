---
title: Lab 4, Group B
description: Instructions for doing classification with TensorFlow
keywords: classifier, TensorFlow, Keras
material: Lab Instructions
generator: Typora
author: Brian Bird
---

**CS 210, Intro to AI Programming**

<h1>Lab 4: TensorFlow with Keras</h1>

<h2>Group B</h2>

[TOC]

## Keras Image Classification with the KMNIST Dataset

### Objective:

Your goal is to apply the exact same steps as those in the "[Basic image classification](https://www.tensorflow.org/tutorials/keras/classification)" tutorial (which used the Fashion MNIST dataset) to a new, KMNIST dataset, which is a collection of 10 classical Japanese "Kuzushiji" characters.

This dataset contains 70,000 (60,000 training, 10,000 testing) 28x28 grayscale images of 10 different classical Japanese characters.

### Instructions

Use a Google Colab notebook. The only *real* change is in Step 2, where we load the data.

Step 1: Import Libraries (One new one!)

You'll need tensorflow, numpy, and matplotlib.pyplot as before. You also need to import tensorflow_datasets, which is the library that hosts KMNIST.

Python

```
import tensorflow as tf
import tensorflow_datasets as tfds  # <-- The new import
import numpy as np
import matplotlib.pyplot as plt
```

Step 2: Load the Data (The Only New Part)

KMNIST isn't built into Keras like Fashion MNIST is, so we use tensorflow_datasets (tfds) to get it. This code looks different, but it does the same job.

**This is the most complex part of the exercise, and I've provided the code to get you back to the familiar NumPy arrays from the tutorial.**

```python
# 1. Load the KMNIST data using tfds
#    This downloads the data as a 'tf.data.Dataset' object
(ds_train, ds_test), ds_info = tfds.load(
    'kmnist',
    split=['train', 'test'],
    shuffle_files=True,
    as_supervised=True,  # Returns (image, label) tuples
    with_info=True,      # Gives us info about the dataset
)

# 2. Convert the data to the NumPy arrays the tutorial used
#    This helper code will do the work for you.
def convert_to_numpy(dataset):
    images = []
    labels = []
    for img, lbl in dataset:
        images.append(img)
        labels.append(lbl)
    return np.array(images), np.array(labels)

print("Converting training data to NumPy...")
train_images, train_labels = convert_to_numpy(ds_train)
print("Converting test data to NumPy...")
test_images, test_labels = convert_to_numpy(ds_test)

# Define the class names (these are just a representation)
class_names = ['o', 'ki', 'su', 'tsu', 'na', 'ha', 'ma', 'ya', 're', 'wo']
```

Step 3: Explore the Data

Now you're back on familiar ground! This is 100% identical to the tutorial.

- Check `train_images.shape`. You should see `(60000, 28, 28, 1)`. (Note: It has a `1` at the end for the color channel; this is fine!)
- Check `len(train_labels)`.
- Check `test_images.shape`.

Step 4: Preprocess the Data

100% identical. The pixel values are 0-255.

```python
train_images = train_images / 255.0
test_images = test_images / 255.0
```

Step 5: Build the Model (CRITICAL STEP)

This is the key. Because the new data is also 28x28, the model architecture is... 100% identical.

(Note: The `Flatten` layer is smart. It doesn't care if the input is `(28, 28)` or `(28, 28, 1)`. It will flatten both correctly.)

```python
model = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28, 1)), # Or (28, 28)
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(10)
])
```

Step 6: Compile the Model

100% identical. 10 classes, integer labels.

```python
model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])
```

Step 7: Train the Model

100% identical.

```python
model.fit(train_images, train_labels, epochs=10)
```

You should see high accuracy, just like with Fashion MNIST.

Step 8 & 9: Evaluate and Make Predictions

The code is identical. You can use all the same plotting functions. The only difference is that instead of a "Shirt", the model will be predicting "tsu" or "na".

This exercise proves that the model architecture is tied to the *shape* of the data, not its *content*.

### Bonus Challenge (Optional, XC)

You bet. Adding a new layer is the "Hello, World" of seeing how models change.

Here is the full exercise again, now with a new bonus challenge at the end.

------



### Exercise: Keras Image Classification with the KMNIST Dataset



**Objective:** Your goal is to use the KMNIST dataset, which is a collection of 10 classical Japanese "Kuzushiji" characters. This dataset is a perfect "drop-in replacement" for the original Fashion MNIST and Digits datasets.

It will test your ability to load a *new* dataset (using the `tensorflow_datasets` library) while confirming that the *entire rest of the process* (preprocessing, model building, training) is identical because the data's shape and size are the same.

**The New Dataset: KMNIST** This dataset contains 70,000 (60,000 training, 10,000 testing) **28x28 grayscale images** of 10 different classical Japanese characters.

**Your Task: Follow the Tutorial's Steps**

Use a Google Colab notebook. The only *real* change is in Step 2, where we load the data.

**Step 1: Import Libraries (One new one!)** You'll need `tensorflow`, `numpy`, and `matplotlib.pyplot` as before. You also need to import `tensorflow_datasets`, which is the library that hosts KMNIST.

Python

```
import tensorflow as tf
import tensorflow_datasets as tfds  # <-- The new import
import numpy as np
import matplotlib.pyplot as plt
```

**Step 2: Load the Data (The Only New Part)** KMNIST isn't built into Keras like Fashion MNIST is, so we use `tensorflow_datasets` (tfds) to get it. This code looks different, but it does the same job.

**This is the most complex part of the exercise, and I've provided the code to get you back to the familiar NumPy arrays from the tutorial.**

Python

```
# 1. Load the KMNIST data using tfds
#    This downloads the data as a 'tf.data.Dataset' object
(ds_train, ds_test), ds_info = tfds.load(
    'kmnist',
    split=['train', 'test'],
    shuffle_files=True,
    as_supervised=True,  # Returns (image, label) tuples
    with_info=True,      # Gives us info about the dataset
)

# 2. Convert the data to the NumPy arrays the tutorial used
#    This helper code will do the work for you.
def convert_to_numpy(dataset):
    images = []
    labels = []
    # tfds data is an iterator, so we loop through it
    for img, lbl in dataset:
        images.append(img)
        labels.append(lbl)
    return np.array(images), np.array(labels)

print("Converting training data to NumPy...")
train_images, train_labels = convert_to_numpy(ds_train)
print("Converting test data to NumPy...")
test_images, test_labels = convert_to_numpy(ds_test)

# Define the class names (these are just a representation)
class_names = ['o', 'ki', 'su', 'tsu', 'na', 'ha', 'ma', 'ya', 're', 'wo']
```

**Step 3: Explore the Data** Now you're back on familiar ground! This is 100% identical to the tutorial.

- Check `train_images.shape`. You should see `(60000, 28, 28, 1)`. (Note: It has a `1` at the end for the color channel; this is fine!)
- Check `len(train_labels)`.
- Check `test_images.shape`.

**Step 4: Preprocess the Data** 100% identical. The pixel values are 0-255.

Python

```
train_images = train_images / 255.0
test_images = test_images / 255.0
```

**Step 5: Build the Model** This is the key. Because the new data is *also* 28x28, the model architecture is... **100% identical**.

(Note: The `Flatten` layer is smart. It doesn't care if the input is `(28, 28)` or `(28, 28, 1)`. It will flatten both correctly.)

```python
model = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28, 1)), # Or (28, 28)
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(10)
])
```

**Step 6: Compile the Model** 100% identical. 10 classes, integer labels.

```python
model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])
```

**Step 7: Train the Model** 100% identical.

Python

```
model.fit(train_images, train_labels, epochs=10)
```

You should see high accuracy, just like with Fashion MNIST.

**Step 8 & 9: Evaluate and Make Predictions** The code is identical. You can use all the same plotting functions. The only difference is that instead of a "Shirt" , the model will be predicting "tsu" or "na".

------



### Bonus Challenge (Optional)

When you run your model, you'll probably see the `accuracy` on the training data (e.g., 99%) is much higher than the `accuracy` you get from `model.evaluate` on the test data (e.g., 92%). This gap is called **overfitting**.

Your challenge is to introduce a new layer that fights overfitting: **Dropout**.

Go back to **Step 5 (Build the Model)** and add a `Dropout` layer. This layer "turns off" a random percentage of neurons during training, forcing the model to learn more robust patterns.

**Your new model should look like this:**

```python
model = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28, 1)),
    tf.keras.layers.Dense(128, activation='relu'),
    
    # Add this new Dropout layer
    tf.keras.layers.Dropout(0.2),  # "Drops out" 20% of neurons
    
    tf.keras.layers.Dense(10)
])
```

Now, re-compile (Step 6) and re-train (Step 7) the model.

**Compare your results:**

1. Does the final test accuracy (`model.evaluate`) get **better** or **worse**?
2. Look at the training log. Is the gap between the training `accuracy` and the eventual test `accuracy` **smaller** than before? (It should be!)



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

