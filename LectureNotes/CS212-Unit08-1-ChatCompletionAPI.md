---
title: Chat Completion API
description: How to integrate AI into an app by call a chat completion API 
keywords: OpenAI, chat-completion
generator: Typora
author: Brian Bird
---

**CS 210, Intro to AI Programming**

<h1>Calling a Chat-Completion API</h1>

| Topics                                   |                                                              |
| ---------------------------------------- | ------------------------------------------------------------ |
| 1. What is AI, Python                    | 6. ANN: Image recognition                                    |
| 2.  Symbolic AI                          | 7. Generative AI                                             |
| 3. Classical machine learning: training  | 8. <mark>Calling the chat completion API</mark>              |
| 4. Classical machine learning: inference | 9. Agentic AI with MCP                                       |
| 5. More ML + History of AI               | 10. Social and ethical issues  <br />Term project completion |
|                                          | 11. Final project presentation                               |

<h2>Contents</h2>

[TOC]

## Tools and Concepts

### Google AI Studio

Google AI Studio is a web-based development environment used for prototyping and building applications with the Gemini family of generative AI models. It functions as a unified interface for rapid iteration and implementation of AI features.

Developers can do these things in AI Studio:

#### In the Prompt Playground (Interactive):

- **Test and refine prompts** across text, image, and video modalities.

- **Adjust model parameters** (e.g., temperature, top-p) for desired output characteristics.

- **Utilize Google Search grounding** to provide real-time, external data to the model.

#### In the Settings or Dashboard (Configuration)

- **Manage and structure data** for model fine-tuning (if supported by the specific Gemini model version).
  - *(Note: Model tuning itself is usually a separate flow managed in the AI Studio Dashboard, not the interactive playground.)*
- **Export tested code snippets** in various languages (e.g., Python, Node.js) for direct integration via the Gemini API.
  - *(This is often done by clicking a "Get Code" button adjacent to the playground, which generates code based on your current prompt and parameter settings).*



## How To Use the Gemini API

### Get an API Key

1. Get a Gemini Account.

2. In Google AI Studio, in the lower left, click on "Get API key".
3. Click on "Create API Key" (in the top right).
   - Give the key a name and create a project.
   - Create the key
   - Check to make sure billing is listed as the Free tier".

### Install the Gemini SDK

```bash
pip install -q -U google-genai
```

### Make a Request

The code below can be run from an interactive Python session, but first an environment variable must be set for the API key:

In command prompt:  `set GEMINI_API_KEY="YOUR_API_KEY"`  
In PowerShell:  `$env:GEMINI_API_KEY="YOUR_API_KEY"`   
In MacOS terminal: `export GEMINI_API_KEY="<YOUR_API_KEY>"`

```python
from google import genai

# The client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash", contents="Explain how AI works in a few words"
)
print(response.text)
```





## Appendix

### Gemini Model Parameters

The Gemini models in Google AI Studio offer several key parameters (*hyperparameters*) that control the quality, style, and structure of the generated output. Understanding these allows you to fine-tune the model's behavior for specific tasks, balancing creativity and factual consistency.

Here are the main model generation parameters:

| **Parameter**                | **Description**                                              | **Typical Range**               | **Impact of Higher Value**                                   |
| ---------------------------- | ------------------------------------------------------------ | ------------------------------- | ------------------------------------------------------------ |
| **Temperature**              | Controls the **randomness** or *creativity* of the response. It mathematically scales the probability distribution of the next token selection. | 0.0 - 2.0                       | **More Creative/Diverse:** The model is more likely to select lower-probability tokens, leading to more varied, surprising, and sometimes less coherent output. |
| **Top-P** (Nucleus Sampling) | Selects the smallest set of most probable tokens whose cumulative probability exceeds the value $P$. | 0.0 - 1.0                       | **More Diverse/Adaptive:** Dynamically increases the selection pool size in contexts where the probability distribution is flat (many good options) and narrows it when the distribution is sharp (one clear choice). |
| **Top-K**                    | Limits the number of most probable tokens the model can choose from for the next word. | 1 to \text{Max Vocabulary Size} | **More Diverse/Wider Pool:** Allows the model to sample from a larger, but fixed, set of the most likely next tokens. A value of $K=1$ is *greedy decoding* (always picks the single most probable token). |
| **Max Output Tokens**        | Sets the maximum length (in tokens) the model is allowed to generate in a single response. | Model-Dependent                 | **Longer Responses:** Allows for more extensive and detailed output, up to the model's context window limit. |
| **Stop Sequences**           | A list of specific strings (e.g., `\n\n`, `---`, `\nUser:`) that, if generated, will cause the model to immediately stop generating further text. | \text{Custom strings}           | **Structured Output:** Enforces a specific end-point, which is crucial for creating structured outputs like code blocks or delimited lists. |
| **Frequency Penalty**        | Controls the likelihood of the model using tokens that have **already appeared** in the generated output. | (Typically 0.0 - 1.0)           | **Less Repetitive:** Penalizes frequently used words, discouraging repetition and promoting new, more diverse vocabulary within the response. |

A common strategy is to use *Temperature* as the primary control for creativity, setting *Top-P* and *Top-K* to high default values (e.g., P=0.95, K=40) to allow the model to operate without too many restrictions.

---



### Setting an Environment Variable

The standard and most secure way to use your Gemini API key with the Python SDK is by setting it as the **`GEMINI_API_KEY`** environment variable.

The steps for setting this variable depend on your operating system and, for macOS/Linux, the shell you use.

####  macOS / Linux (Terminal)

In macOS and Linux, environment variables are typically set in your shell's configuration file (most modern macOS systems use **Zsh**, while many Linux distributions use **Bash**).

1. **Open your terminal's configuration file** (replace `~/.zshrc` with `~/.bashrc` or `~/.bash_profile` if you use Bash):

   Bash

   ```
   nano ~/.zshrc
   ```

2. **Add the export command** to the end of the file, replacing `<YOUR_API_KEY>` with your actual Gemini API key:

   Bash

   ```
   export GEMINI_API_KEY="<YOUR_API_KEY>"
   ```

3. **Save and close** the file (in `nano`, press $\text{Ctrl}+\text{X}$, then $\text{Y}$, and then $\text{Enter}$).

4. **Load the new variable** into your current terminal session:

   Bash

   ```
   source ~/.zshrc
   ```

5. **Verify** it was set correctly:

   Bash

   ```
   echo $GEMINI_API_KEY
   ```

This makes the variable **persistent**, so it will be available every time you open a new terminal window.

#### Windows (Command Prompt or PowerShell)

On Windows, you can set a **persistent user-level environment variable** via the command line, which will be available in new terminal sessions (both Command Prompt and PowerShell).

##### 1. Set the Persistent Variable

Execute the following command, replacing `<YOUR_API_KEY>` with your actual key:

- **In Command Prompt (`cmd`):**

  DOS

  ```
  setx GEMINI_API_KEY "YOUR_API_KEY"
  ```

- **In PowerShell:**

  PowerShell

  ```
  [Environment]::SetEnvironmentVariable("GEMINI_API_KEY", "YOUR_API_KEY", "User")
  ```

##### 2. Apply and Verify

- The `setx` command makes the variable persistent, but **it only takes effect in new terminal windows**. **Close your current terminal and open a new one.**
- **Verify** it was set correctly in the new window:

| **Shell**          | **Command to Verify**      |
| ------------------ | -------------------------- |
| **Command Prompt** | `echo %GEMINI_API_KEY%`    |
| **PowerShell**     | `echo $env:GEMINI_API_KEY` |

> 💡 **Temporary Variable:** If you only need the key for the current session (it will disappear when the window closes), you can use `set GEMINI_API_KEY="YOUR_API_KEY"` in Command Prompt or `$env:GEMINI_API_KEY="YOUR_API_KEY"` in PowerShell. In a MacOS terminal use: `export GEMINI_API_KEY="<YOUR_API_KEY>"`

---



### Installing the google-genai on MacOS

The official and recommended way to install the **Google GenAI SDK** (the Python library that provides the `google-genai` package) is by using the Python package installer, **`pip`**, not Homebrew (`brew`).

Homebrew (`brew`) is primarily a package manager for macOS system tools and command-line applications. While there is a separate package for the **Gemini Command Line Interface (CLI)** that you *can* install with Homebrew, the Python SDK used in your code example must be installed using `pip`.

Here are the correct installation methods:

#### Python SDK Installation (Recommended)

To install the official **`google-genai`** Python library, use `pip` in your terminal:1

Bash

```
pip install google-genai
```

#### Best Practice: Use a Virtual Environment

It's highly recommended to use a virtual environment to manage dependencies for your Python projects and avoid conflicts with other applications:

1. **Create a virtual environment:**

   Bash

   ```
   python3 -m venv venv-genai
   ```

2. **Activate the environment:**

   Bash

   ```
   source venv-genai/bin/activate
   ```

3. **Install the SDK:**

   Bash

   ```
   pip install google-genai
   ```

4. **Deactivate when done:**

   Bash

   ```
   deactivate
   ```

#### Gemini CLI Installation (Optional Alternative)

If you were trying to install a command-line tool to **interact with Gemini directly from your terminal**, you would use Homebrew for the **`gemini-cli`** package:

Bash

```
brew install gemini-cli
```

This is a separate tool from the Python SDK and is used for non-scripted, terminal-based interaction.

To see a step-by-step guide on setting up the CLI, you can watch this video: [Google Gemini CLI: AI in Your Terminal (Windows • Linux • macOS)](https://www.youtube.com/watch?v=xqvprnPocHs). This video provides instructions for installing and using the command-line interface, which is the tool that can be installed using Homebrew.



## Reference

[Free Gemini Pro Subscription for Students](https://gemini.google/sg/students/?hl=en)

[Google AI Studio](https://aistudio.google.com/app/)

[Google Gemini API Docs](https://ai.google.dev/gemini-api/docs)



Note: Parts of this document were drafted using Gemini Flash 2.5 (2025).

---

[![Creative Commons License](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/) Intro to AI Programming lecture notes by [Brian Bird](https://profbird.dev), written in <time>2025</time>, are licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/). 

---