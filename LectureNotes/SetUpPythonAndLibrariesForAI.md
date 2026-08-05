---
title: Installing scikit-learn and tensor flow
description: How to set up a computer to use Python to work with the scikit-learn and tensorflow AI libraries.
keywords: ML, numpy, scikit-learn, tensroflow, python
generator: Typora
author: Brian Bird
---

<h1>Set Up Python Packages for ML</h1>

**CS 212, AI Programming 1**

| Topics                               |                                   |
| ------------------------------------ | --------------------------------- |
| <mark>Overview, History of AI</mark> | Generative AI                     |
| Machine Learning: Symbolic           | Using LLMs in custom applications |
| Machine Learning: Statistical        | Custom chatbot creation           |
| Neural networks                      | LLM fine-tuning                   |
| Image recognition                    | Social and ethical issues of AI   |



<h2>Contents</h2>

[TOC]

## Python Packages We Will Use

### NumPy
NumPy is a scientific computing library for efficient array processing, offering fast, flexible multi-dimensional arrays that outperform native Python lists. It adds additional array features that used by many scientific and machine learning libraries.

### scikit-learn
Scikit-learn is a library for traditional machine learning in Python, built on NumPy arrays. It offers a consistent interface to a wide range of models and tools, many beyond the scope of this course. As you deepen your understanding, the [official documentation](https://scikit-learn.org/stable/documentation.html) is an essential resource.

### TensorFlow with Keras
TensorFlow is a widely adopted, open-source framework and toolkit developed by Google. It provides deep learning neural network functionality and includes Keras, a user-friendly Python API (programming interface). 

- provides direct access to the GPU.

### Pillow

The Pillow library is an image-processing library

### Matplotlib

Matplotlib is for plotting.



## Setup Instructions for Windows

### Install Python and the Python Launcher

#### Check for Python and the Python Launcher

Open a Power Shell Terminal on your computer and check to see if Python is installed on your system using this command:

```powershell
python --version
```

If it is installed, the version number will be reported.

Check to see if the Python launcher is installed:

```powershell
py --version
```

If it is installed, the version number will be reported.

#### Install One or Both if Missing

Download the latest Python installer and run it.

- If Python isn't installed, then install it using the custom setup. Check the "Python Launcher" box in the "Optional Features" dialog.
- If Python is installed, but not py, then choose the "Modify" option. In the "Optional Features" dialog, check the box for "Python Launcher".

### Set Up a Virtual Environment

**1. Use a TensorFlow Compatible Version of Python**

TensorFlow currently (8/26/2025) works with python 3.9&mdash;3.12,  Check your Python version (if Python is installed)

```bash
python --version
```

If it's older than 3.9 or newer than 3.12.x (where x is any number) then install 3.12 using WinGet.[^1].

```powershell
winget install --id Python.Python.3.12
```

**2. Create a Virtual Environment**

Navigate to the folder you want to use for your project or create one. For example:

```powershell
cd C:\Users\YourUserName\Projects\
```

Then create the *virtual environment*[^2]. You can name the virtual environment anything you like, in this example it is "ml-venv":

```bash
py -3.12 -m venv ml-venv
```

This creates a folder named `ml-venv` containing the isolated Python environment.

**2. Activate the Environment**

```powershell
.\ml-venv\Scripts\activate
```

Your terminal prompt will change to show you're inside the virtual environment. Change directories to the new folder:

```powershell
cd ml-venv
```

Now any `pip install` commands will apply only to this project.

**4. Install Packages for the Project**

Before installing packages it is a good idea to update pip. This will upgrade pip within your virtual environment:

```powershell
python -m pip install --upgrade pip
```

Install the dependencies for this project:

```powershell
pip install numpy
pip install scipy
pip install matplotlib
pip install scikit-learn
pip install tensorflow
pip install pillow
```

**5. Deactivate When Done**

To exit the virtual environment:

```bash
deactivate
```



## Setup Instructions for MacOS

### Install Python

TensorFlow for MacOS currently (8/26/2025) requires python 3.9 or 3.10, it won't work with newer versions. Check your Python version (if it is installed)

```bash
python --version
```

If it's older than 3.9 or newer than 3.10.x (where x is any number) then install 3.10 using Homebrew, a MacOS package manager[^3].

```bash
brew update
brew install python@3.10
```

This will install Python 3.10 on your computer at a location like: `/usr/local/bin/python3.10`

### Install Libraries

```bash
xcode-select --install
pip3 install --upgrade pip
pip3 install numpy
pip3 install scipy
pip3 install matplotlib
pip3 install scikit-learn
pip3 install tensorflow-macos==2.12.0
pip3 install tensorflow-metal==1.0.0
pip3 install pillow
```

- For TensorFlow, specify version 2 to ensure that the proper version of the Keras library is included.
- Metal is Apple’s low-level, high-performance graphics and compute API that provides direct access to the GPU.
- The Pillow library is an image-processing library
- Matplotlib is for plotting.

### Set Up a Virtual Environment

**1. Create a Virtual Environment**

Navigate to your project directory or create one:

```bash
mkdir Projects/pdl
cd Projects/pdl
```

Then create the *virtual environment*[^2]:

```bash
/usr/local/bin/python3.10 -m venv
```

This creates a folder named `venv` containing the isolated Python environment.

**2. Activate the Environment**

```bash
source venv/bin/activate
```

Your terminal prompt will change to show you're inside the virtual environment. Now any `pip3 install` commands will apply only to this project.

**4. Install Your Packages**

Install the dependencies for this project:

```bash
pip3 install --upgrade pip
pip3 install numpy
pip3 install scipy
pip3 install matplotlib
pip3 install scikit-learn
pip3 install tensorflow-macos==2.12.0
pip3 install tensorflow-metal==1.0.0
pip3 install pillow
```

**5. Deactivate When Done**

To exit the virtual environment:

```bash
deactivate
```

## References

- *Practical Deep Learning: A Python-Based Introduction*, 2nd Edition, Ronald T. Kneusel, 2025, No Starch Press. 
  Chapter 0: The operating Environment, Installing the Toolkits

- [Install scikit-Learn](https://scikit-learn.org/stable/install.html)&mdash;scikit-learn.org

- [Install Tensorflow 2](https://www.tensorflow.org/install)&mdash;tensorflow.org
- [Getting Started with Tensorflow Metal](https://developer.apple.com/metal/tensorflow-plugin/)&mdash;Apple Developer

---

[![Creative Commons License](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/) AI Programming 1 lecture notes by [Brian Bird](https://profbird.dev), written in <time>September 2025</time>, are licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/). 

MS Copilot with GPT-5 was used to draft parts of these notes.

[^1]: WinGet, the [Windows Package Manager](https://github.com/microsoft/winget-cli?tab=readme-ov-file),  is installed by default on Windows 11 and can be installed on Windows 10. 
[^2]: A Python virtual environment is like a sandbox for your Python projects—it isolates dependencies so that each project can have its own specific versions of packages, without interfering with others or your system-wide Python setup. It creates a folder (venv) containing: a) A copy of the Python interpreter. b) A local pip installer. c) A clean site-packages directory for your project’s dependencies. When you activate it, your shell temporarily switches to using that isolated Python and pip. 
[^3]: Homebrew is not installed by default on MacOS. See the [Homebrew website](https://brew.sh/) for installation instructions.  Another popular package manager for MacOS is [MacPorts](https://www.macports.org/).  ↩