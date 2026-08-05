---
title: Unit 1 Overview
description: What's AI
keywords: Classical AI, Symbolic AI, GOFAI
generator: Typora
author: Brian Bird
---

**CS 210, Intro to AI Programming**

<h1>Overview of AI</h1>



| Topics                                   |                           |
| ---------------------------------------- | ------------------------- |
| 1. What is AI, <mark>Python</mark>       | 6. ANN: Image recognition |
| 2.  Symbolic AI                          | 7. Generative AI          |
| 3. Classical Machine Learning: Training  | 8. Custom chatbot         |
| 4. Classical Machine Learning: Inference | 9. LLM fine-tuning        |
| 5. Midterm                               | 10. Ethics                |
|                                          | 11. Final                 |



<h2>Contents</h2>

[TOC]

## Learning a New Programming Language

Most programming languages have many things in common:

- They implement *algorithms*&mdash;think of an algorithm as a recipe or set of instructions for doing something.
- They have a way to implement the three common *control structures*:
  - Sequence
  - Selection
  - Repetition
- There are ways to define and call functions (aka procedures, methods, subroutines)
- There are ways to represent structured data:
  - Strings
  - Arrays 
    Python has lists, which are similar. The NumPy library provides actual arrays.
  - Dictionaries

Once you've learned how to work with these concepts in one language, it's mostly just a mater of learning the new syntax for the next language you learn.



## Installing Python and Running a Program

### Windows

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

Download the latest [Python installer](https://www.python.org/downloads/) and run it.

- If Python isn't installed, then install it using the custom setup. Check the "Python Launcher" box in the "Optional Features" dialog.
- If Python is installed, but not py, then choose the "Modify" option. In the "Optional Features" dialog, check the box for "Python Launcher".

#### Run Hello World

1. **Create the "Hello World" Script**

```python
# A simple program to print a greeting
print("Hello, World! Python is running.")
```

Save the file as **`hello.py`** 

2. **Run the Program in Command Prompt (CMD) or PowerShell**

   Open the Command Prompt:

   - Press the **Windows Key + R**, type `cmd`, and press Enter. (Or use the Windows search bar to find "Command Prompt" or "PowerShell").

   - Use the `cd` (Change Directory) command to move to the folder where you saved your script. If you saved it to `C:\PythonProjects`, you would type: `cd C:\PythonProjects`

3. **Execute the Script:**

Use the `python` command followed by the file name:

```
python hello.py
```

(If `python` doesn't work, try using `py hello.py` instead.)

**Output:** The Terminal will display the result:

```
Hello, World! Python is running on Windows.
```



### MacOS

While macOS comes with a system version of Python pre-installed, it's outdated and should not be used for development. We will install a modern version using **Homebrew**, the popular package manager for macOS.

#### Check the version of Python

In the Terminal, run:

```
python3 --version
```

If it's older than 3.12 (or whtever the latest version is) then upate it.

#### Install or Update Python

##### Install Homebrew (If You Don't Have It)
Homebrew is a tool that makes installing developer software on Mac incredibly easy.

**Open the Terminal:**

Press `Cmd + Space` and type "Terminal," then press Enter.

**Run the Homebrew installation command:**

Copy and paste the following line into your Terminal and press Enter

```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

The script will prompt you to enter your administrator password (it won't display as you type) and press Enter.

Follow any final on-screen instructions, such as adding Homebrew to your system's PATH.

##### Install Python

Once Homebrew is installed, installing Python is a single command.

In the Terminal, run:

```
brew install python
```

Homebrew will download and install the latest stable version of Python (typically Python 3.x).

**Verify the Installation**

After the installation completes, confirm that the correct version is now recognized by your system.

Check the Python version:

In the Terminal, run:

```
python3 --version
```

You should see output confirming the version you just installed (e.g., `Python 3.12.2`).

#### Run Hello World

1. **Create your Python file:** Use a text editor to create a file named `hello.py` and add the following content:

   ```python
   # A simple program to print a greeting
   print("Hello, World! Python is running.")
   ```

1. **Open Terminal and Navigate:** Open your Terminal and navigate to the directory where you saved `hello.py` (using the `cd` command).

2. **Run the script:** Execute the file using the Python 3 interpreter:

   ```bash
   python3 hello.py
   ```

3. **Output:** The Terminal will display the output:

   ```bash
   Hello, World! Python is running.
   ```

## Using VS Code for Python Programming 

### Install the Python Extension

- Go to the Extensions view (`Ctrl+Shift+X`).
- Search for "Python" and install the official extension by Microsoft.

### Use the Debugger

1. **Open Your Project Folder**
   - Open the folder containing your `.py` files in VS Code.
2. **Select the Python Interpreter**
   - Press `Ctrl+Shift+P` and type `Python: Select Interpreter`.
   - Choose the interpreter you want to use (e.g., Python 3.x).
3. **Set Breakpoints**
   - Open the Python file you want to debug.
   - Click in the gutter to the left of the line numbers to set breakpoints.
4. **Start Debugging**
   - Open the file you want to run (for example, `main.py`).
   - Press `F5` to start debugging, or click the green "Run and Debug" button in the Run view (`Ctrl+Shift+D`).
   - The debugger will stop at your breakpoints, and you can inspect variables, step through code, etc.
5. **Debug Controls**
   - Use the debug toolbar at the top to step over (`F10`), step into (`F11`), continue (`F5`), or stop (`Shift+F5`).
6. **Inspect Variables**
   - Use the "Variables" pane in the Run view to see local and global variables.
   - Hover over variables in the editor to see their values.

**Tips**

- You can add `"args": ["arg1", "arg2"]` to your `.vscode/launch.json` if your script needs command-line arguments.
- You can use the integrated terminal (`Ctrl+``) to run scripts normally with `python your_script.py`.

## Learning Python

### Distinctives of Python

- No curly braces! Indentation is used to delineate blocks of code. 
- Dynamic typing: You don't need to declare the data types of variables.
- Interpreted, not compiled.
- No `;` to terminate lines. The end of the line is the end of the line.
- Python has a distinctive *pythonic* style which is described in the [PEP-8 style guide](https://peps.python.org/pep-0008/).

Here is an implementation of the classic "FizzBuzz" program[^1] in Python:

```python
# FizzBuzz program
for i in range(1, 10):
      output = ""

      # Check for divisibility by 3
      if i % 3 == 0:
          output += "Fizz"

      # Check for divisibility by 5
      if i % 5 == 0:
          output += "Buzz"

      # If output is still empty, print the number
      if output == "":
          print(i)
      else:
          print(output)
```



### Programming Paradigms of Python

- **Multi‑paradigm, but not in equal balance**  
  While Python supports OOP, functional programming, and procedural code, its sweet spot blends object orientation with functional elements — without the ceremony of C++ or Java’s class scaffolding.
- **Dynamic typing and duck typing**: Python favors type flexibility at runtime over compile‑time enforcement. Class types are implicit — *if it quacks and walks like a duck, it’s treated like a duck*.
- **First‑class functions**: You can pass, return, and store functions just like data, which supports a more functional style than many C‑family languages.

Here is an [example of Object Oriented Programming in Python](Unit01-Files/oopCar.py). This car simulator illustrates these of OOP concepts:

- **Composition:** The `Car` class *has-a* an `Engine` instance.
- **Inheritance:** `Driver` and `Passenger` *are-a* special types of `Occupant`.
- **Encapsulation:** The car's state (like fuel level and running status) is managed internally by the `Engine` class.



### Exercise

Translate a simple game from either [JavaScript](Unit01-Files/dieBattle.js) or [C#](Unit01-Files/dieBattle.cs) into Python. 

The game is "die battle": two players each roll a single six-sided die, and the player with the higher number wins. It requires defining three simple classes:

1. **`Die`**: Represents the physical object that can be rolled.
2. **`Player`**: Represents a participant who interacts with the die.
3. **`DiceBattle`**: Orchestrates the game flow and holds the game state (the players and the die).

[The solution is here](Unit01-Files/dieBattle.py).



## Reference

- [Python Tutorial](https://docs.python.org/3/tutorial/)&mdash;Python web site
- [Using Python in VS Code](https://code.visualstudio.com/docs/python/python-tutorial)&mdash;Visual Studio Code web site
- [PEP 8 – Style Guide for Python Code](https://peps.python.org/pep-0008/)&mdash;Official Python Web Site
  - [Summary of the Style Guide]()&mdash;Google Gemini and Brian Bird


- [Python: The Documentary | An origin story](https://www.youtube.com/watch?v=GfH4QL4VqJ0)&mdash;CultRepo Video

  

Note: Parts of this document were drafted with assistance from Gemini 2.5 Flash 9/30/25


---



[![Creative Commons License](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/) Intro to AI Course Materials by [Brian Bird](https://profbird.dev), written in <time>2025</time>, are licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/). 

[^1]: The FizzBuzz program iterates from 1 up to some specified limit.    It prints "Fizz" for multiples of 3, "Buzz" for multiples of 5, "FizzBuzz" for multiples of both, or just the number.

