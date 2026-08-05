---
title: Lab 4, Group C
description: Instructions for doing classification with TensorFlow
keywords: classifier, TensorFlow, Keras
material: Lab Instructions
generator: Typora
author: Brian Bird
---

**CS 210, Intro to AI Programming**

<h1>Lab 4: TensorFlow with Keras</h1>

<h2>Group C</h2>

[TOC]

## Keras Image Classification with the EMNIST (Letters) Dataset

### Objective:

Your goal is to apply the same steps as those in the "[Basic image classification](https://www.tensorflow.org/tutorials/keras/classification)" tutorial (which used the Fashion MNIST dataset) to a new,  EMNIST (Letters) dataset to build a handwritten letter (A-Z) classifier. This dataset has the same image shape as the tutorial, but a different number of classes (26 instead of 10).

This will test your understanding of:

- Loading a new dataset from `tensorflow_datasets`.
- Adapting the model's **final layer** to match the number of classes.
- Confirming that the rest of the model and training process remains the same.

**The New Dataset: EMNIST/Letters** This dataset contains 145,600 (88,800 training, 14,800 testing) **28x28 grayscale images** of 26 different handwritten capital letters (A-Z).

### Instructions

Use a Google Colab notebook. The only *real* change is in Step 2 (loading) and one line in Step 5 (building the model).

**Step 1: Import Libraries** You'll need `tensorflow`, `tensorflow_datasets` (tfds), `numpy`, and `matplotlib.pyplot`.

```python
import tensorflow as tf
import tensorflow_datasets as tfds  # We'll use this to load EMNIST
import numpy as np
import matplotlib.pyplot as plt
```

**Step 2: Load the Data** Like KMNIST, we'll use `tfds` to load this dataset. I've included the helper code again to convert it back to the simple NumPy arrays you're used to.

```python
# 1. Load the EMNIST/letters data using tfds
(ds_train, ds_test), ds_info = tfds.load(
    'emnist/letters',
    split=['train', 'test'],
    shuffle_files=True,
    as_supervised=True,  # Returns (image, label) tuples
    with_info=True,
)

# 2. Convert the data to the NumPy arrays
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

# 3. Create the class names, from 'A' to 'Z'
#    The labels are 0-25.
class_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 
               'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 
               'U', 'V', 'W', 'X', 'Y', 'Z']
```

*Note: The labels in this dataset are actually 0-25. `tfds` loads them correctly. The EMNIST dataset itself has some quirks, but `tfds` handles them.*

**Step 3: Explore the Data** 100% identical. Check the shapes.

- `train_images.shape` should be `(88800, 28, 28, 1)`.
- `train_labels.shape` should be `(88800,)`.

**Step 4: Preprocess the Data** 100% identical. The pixel values are 0-255.

```python
train_images = train_images / 255.0
test_images = test_images / 255.0
```

**Step 5: Build the Model (THE MAIN CHALLENGE)** This is the core of the exercise. The `input_shape` is the same, but the *output* is different.

- The tutorial's model was for 10 classes (`Dense(10)`).
- This dataset has 26 classes.

```python
model = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28, 1)),
    tf.keras.layers.Dense(128, activation='relu'),
    
    # YOU MUST CHANGE THIS LINE!
    # How many neurons for the final layer?
    tf.keras.layers.Dense(26) 
])

model.summary()
```

**Step 6: Compile the Model** 100% identical. `SparseCategoricalCrossentropy` is perfect. It's built for multi-class problems where the labels are simple integers (which ours are, 0-25).

```python
model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])
```

**Step 7: Train the Model** 100% identical.

```python
model.fit(train_images, train_labels, epochs=10)
```

You should see pretty good accuracy again!

**Step 8 & 9: Evaluate and Make Predictions** The code is identical. You can use all the same plotting functions, and thanks to your `class_names` list, you'll see the model correctly predicting "T", "G", "A", etc.

------



### Bonus Challenge (Optional)

The simple model from the tutorial works well, but can we improve it? A "deeper" model (with more layers) can sometimes learn more complex patterns.

Try modifying **Step 5 (Build the Model)**. After the `Dense(128, activation='relu')` layer, try adding **another** `Dense` layer (e.g., 64 neurons, also with `relu` activation) before the final `Dense(26)` layer.

Your new model would look like this:

```Python
model = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28, 1)),
    tf.keras.layers.Dense(128, activation='relu'),
    
    # Add the new layer
    tf.keras.layers.Dense(64, activation='relu'),
    
    tf.keras.layers.Dense(26)
])
```

Re-compile and re-train this new, "deeper" model. Does the final test accuracy get better or worse?





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

