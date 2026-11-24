---
title: Chat Completion API
description: How to integrate AI into an app by calling a chat completion API
keywords: OpenAI, chat-completion
generator: Typora
author: Brian Bird
---

**CS 212, AI Programming 1**

<h1>Calling a Chat-Completion API</h1>

<h2>Contents</h2>

[TOC]

## AI Model APIs

Model APIs are used when adding AI features to your own apps (chat, summarizing, translating, classifying, answering questions).

### Chatbot Clients vs. the API

Most AI companies offer the same models in two different ways:

- **Chatbot client/harness** (ChatGPT, Claude, Gemini apps and websites)
  - For people typing and reading in a chat window.
  - Paid for with a flat subscription (e.g., free, Plus, Pro), usually with usage limits.
- **API service** (programming interface)
  - For programs that send requests to the model and receive responses.
  - Has its own account, API key, and billing, separate from any chatbot subscription.
  - Billed by usage, typically per million *tokens* (input and output priced separately). Larger models cost more.
  - Some providers have a free tier with low rate limits, which is enough for coursework.
- A chatbot subscription usually does not include API access, and API credits do not include a chatbot subscription.

## AI Model API Providers

### Frontier Proprietary Model Providers

These companies provide access to proprietary models that can only be run on servers they control.

| **Company** | **Model Family** | **Most Capable** | **Second** | **Third** | **Fourth** |
| ----------- | ---------------- | ---------------- | ---------- | --------- | ---------- |
| <a href="https://openai.com/" target="_blank">OpenAI</a> | <a href="https://openai.com/chatgpt/overview/" target="_blank">ChatGPT</a> | GPT-6.2 Astra | GPT-6.2 Sol | GPT-6.1 Terra | GPT-6 Luna |
| <a href="https://www.anthropic.com/" target="_blank">Anthropic</a> | <a href="https://www.anthropic.com/claude" target="_blank">Claude</a> | Claude Fable 5.2 | Claude Opus 5.5 | Claude Sonnet 5.5 | Claude Haiku 5.5 |
| <a href="https://deepmind.google/" target="_blank">Google</a> | <a href="https://deepmind.google/models/gemini/" target="_blank">Gemini</a> | Gemini 4 Carbon | Gemini 4 Argon | Gemini 4 Hydrogen | Gemini 3.8 Flash |
| <a href="https://ai.meta.com/" target="_blank">Meta</a> | <a href="https://dev.meta.ai/docs/models" target="_blank">Muse</a> | Muse Wonder | Muse Spark | Muse Ember |  |

- Models are listed from most to least capable. Smaller models are faster and cheaper.
- This list reflects the latest as of Nov.19, 2026. Each company releases new versions often, so check its models page for the current names.

### Open Model Providers

These companies release *open-weight* models, which anyone can download and run on their own servers. Many of them also provide access to the models from their own servers.

- <a href="https://ai.meta.com/" target="_blank">Meta</a>: <a href="https://dev.meta.ai/docs/models" target="_blank">Muse Spark Open and Muse Glimmer</a>
- <a href="https://deepmind.google/" target="_blank">Google</a>: <a href="https://deepmind.google/models/gemma/" target="_blank">Gemma</a>
- <a href="https://www.nvidia.com/" target="_blank">NVIDIA</a>: <a href="https://www.nvidia.com/en-us/ai-data-science/foundation-models/nemotron/" target="_blank">Nemotron</a>
- <a href="https://mistral.ai/" target="_blank">Mistral AI</a>: <a href="https://mistral.ai/models" target="_blank">Mistral</a>
- <a href="https://www.deepseek.com/" target="_blank">DeepSeek AI</a>: <a href="https://www.deepseek.com/" target="_blank">DeepSeek</a>
- <a href="https://www.alibabacloud.com/" target="_blank">Alibaba</a>: <a href="https://qwen.ai/" target="_blank">Qwen</a>
- <a href="https://www.moonshot.ai/" target="_blank">Moonshot AI</a>: <a href="https://www.kimi.com/" target="_blank">Kimi</a>
- <a href="https://z.ai/" target="_blank">Zhipu AI</a>: <a href="https://z.ai/" target="_blank">GLM</a>

### LLM API Aggregators

An LLM API aggregator provides developers with access to many different models and hosting providers through a single, standardized API endpoint. 

- <a href="https://openrouter.ai/" target="_blank">OpenRouter</a>
- <a href="https://opencode.ai/zen" target="_blank">OpenCode Zen</a>
- <a href="https://vercel.com/ai-gateway" target="_blank">Vercel AI Gateway</a>
- <a href="https://huggingface.co/inference/models" target="_blank">Hugging Face Inference Providers</a>



## Working with an API Key

### Get an API Key

1. Create an account at <a href="https://openrouter.ai/" target="_blank">openrouter.ai</a>.
2. Open the <a href="https://openrouter.ai/settings/keys" target="_blank">API Keys</a> page and click "Create API Key".
   - Give the key a name.
   - Optionally set a credit limit on the key.
   - Copy the key right away; it is shown only once.
3. Models whose names end in `:free` cost nothing. They have low daily request limits, which are higher if you have purchased credits. Other models are billed per token from prepaid credits.

Treat the key like a password: don't put it in your code or commit it to a repository.

### Install the SDK

OpenRouter uses the same API format as OpenAI, so the OpenAI Python SDK works with it. The `python-dotenv` package reads your API key from a `.env` file:

```bash
pip install openai python-dotenv
```

- Requires Python 3.10 or newer. The Python that comes with macOS may be older. Check with `python --version` (Windows) or `python3 --version` (macOS/Linux).
- On macOS/Linux, use `python3` and `pip3` if `python` and `pip` aren't found. On Windows, `py -m pip install openai python-dotenv` works if `pip` isn't found.
- Install into a virtual environment to keep projects separate. On macOS, see [Installing the OpenAI SDK on macOS](#installing-the-openai-sdk-on-macos). On Windows:

  ```bash
  python -m venv .venv
  .venv\Scripts\activate
  ```

- Check the install with `pip show openai python-dotenv`.

### Save the Key in a .env File

To keep the key out of your code, save it in a file named `.env` in your project folder:

```
OPENROUTER_API_KEY=YOUR_API_KEY
```

- The file name is just `.env`, with nothing before the dot. On Windows, Notepad may save it as `.env.txt`. Creating the file in VS Code avoids this.
- Add `.env` to your `.gitignore` file so the key never gets committed.
- Run your script from the project folder, so the program finds the `.env` file.

### Make a Request

```python
from dotenv import dotenv_values
from openai import OpenAI

# Read the settings in .env into a dictionary.
settings = dotenv_values(".env")

# Point the OpenAI client at OpenRouter instead of OpenAI.
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=settings["OPENROUTER_API_KEY"],
)

response = client.chat.completions.create(
    # Model names have the form provider/model. Pick one on openrouter.ai/models.
    model="google/gemma-4-31b-it:free",
    messages=[{"role": "user", "content": "Explain how AI works in a few words"}],
)
print(response.choices[0].message.content)
```

- To use a different model, change only the `model` string. The rest of the code stays the same.
- Free model names change over time. Check the <a href="https://openrouter.ai/models" target="_blank">models list</a> (filter by price) if a name stops working.

## Messages and Roles

A chat-completion request contains a list of *messages*. Each message is a dictionary with a `role` and `content`.

| **Role**      | **Who writes it**         | **Purpose**                                                  |
| ------------- | ------------------------- | ------------------------------------------------------------ |
| `system`      | The developer             | Sets the model's behavior, tone, and rules (e.g., "You are a helpful tutor. Answer in two sentences."). Usually the first message. |
| `user`        | The person using the app  | The question or instruction.                                 |
| `assistant`   | The model                 | The model's earlier replies.                                 |

```python
messages = [
    {"role": "system", "content": "You are a helpful tutor. Answer in two sentences."},
    {"role": "user", "content": "What is a token?"},
]
response = client.chat.completions.create(model="google/gemma-4-31b-it:free", messages=messages)
print(response.choices[0].message.content)
```

- The reply is in `response.choices[0].message.content`. Its `role` is `assistant`.
- Some models handle the `system` role differently or ignore it. Check the model's documentation if it doesn't seem to follow the instructions.

## Multi-Turn Chats

The API is *stateless*: the model does not remember earlier requests. To have a conversation, the app must resend the whole conversation with every request.

1. Start a list of messages (usually with a `system` message).
2. Append the user's message and send the list.
3. Append the model's reply to the list as an `assistant` message.
4. Repeat from step 2 for each new user message.

```python
messages = [{"role": "system", "content": "You are a helpful tutor. Answer in two sentences."}]

while True:
    user_input = input("You: ")
    if user_input.lower() in ("quit", "exit"):
        break
    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="google/gemma-4-31b-it:free",
        messages=messages,
    )
    reply = response.choices[0].message.content
    print("AI:", reply)

    messages.append({"role": "assistant", "content": reply})
```

- Every request sends all previous messages again, so longer conversations use more tokens and cost more.
- Each model has a *context window*, a limit on the total tokens it can read in one request. Long conversations must be shortened (e.g., drop or summarize the oldest messages).
- The app, not the model, decides what history to include. It can edit, trim, or reset the list at any time.



## Appendix

### Model Parameters

Most chat models, including those available through OpenRouter, offer several key parameters (*hyperparameters*) that control the quality, style, and structure of the generated output. Understanding these allows you to fine-tune the model's behavior for specific tasks, balancing creativity and factual consistency.

Here are the main model generation parameters. In the API request they are written in lowercase with underscores (`temperature`, `top_p`, `max_tokens`, `stop`, `frequency_penalty`). Not every model supports every parameter.

| **Parameter**                | **Description**                                              | **Typical Range**               | **Impact of Higher Value**                                   |
| ---------------------------- | ------------------------------------------------------------ | ------------------------------- | ------------------------------------------------------------ |
| **Temperature**              | Controls the **randomness** or *creativity* of the response. It mathematically scales the probability distribution of the next token selection. | 0.0 - 2.0                       | **More Creative/Diverse:** The model is more likely to select lower-probability tokens, leading to more varied, surprising, and sometimes less coherent output. |
| **Top-P** (Nucleus Sampling) | Selects the smallest set of most probable tokens whose cumulative probability exceeds the value P. | 0.0 - 1.0                       | **More Diverse/Adaptive:** Dynamically increases the selection pool size in contexts where the probability distribution is flat (many good options) and narrows it when the distribution is sharp (one clear choice). |
| **Top-K**                    | Limits the number of most probable tokens the model can choose from for the next word. | 1 to the vocabulary size | **More Diverse/Wider Pool:** Allows the model to sample from a larger, but fixed, set of the most likely next tokens. A value of K=1 is *greedy decoding* (always picks the single most probable token). |
| **Max Output Tokens**        | Sets the maximum length (in tokens) the model is allowed to generate in a single response. | Model-Dependent                 | **Longer Responses:** Allows for more extensive and detailed output, up to the model's context window limit. |
| **Stop Sequences**           | A list of specific strings (e.g., `\n\n`, `---`, `\nUser:`) that, if generated, will cause the model to immediately stop generating further text. | Custom strings           | **Structured Output:** Enforces a specific end-point, which is crucial for creating structured outputs like code blocks or delimited lists. |
| **Frequency Penalty**        | Controls the likelihood of the model using tokens that have **already appeared** in the generated output. | -2.0 - 2.0           | **Less Repetitive:** Penalizes frequently used words, discouraging repetition and promoting new, more diverse vocabulary within the response. |

A common strategy is to use *Temperature* as the primary control for creativity and leave *Top-P* and *Top-K* at their default values so they don't restrict the model.

The OpenAI SDK has arguments for `temperature`, `top_p`, `max_tokens`, `stop`, and `frequency_penalty`. Other parameters, such as `top_k`, must be passed with the `extra_body` argument, and not every model supports them.



### Installing the OpenAI SDK on macOS

OpenRouter can be used from Python with the **OpenAI SDK**, which is installed with the Python package installer, **`pip`**, not Homebrew (`brew`). Homebrew is primarily a package manager for macOS system tools and command-line applications.

#### Python SDK Installation

```bash
pip install openai python-dotenv
```

#### Best Practice: Use a Virtual Environment

It's highly recommended to use a virtual environment to manage dependencies for your Python projects and avoid conflicts with other applications:

1. **Create a virtual environment:**

   ```bash
   python3 -m venv venv-openrouter
   ```

2. **Activate the environment:**

   ```bash
   source venv-openrouter/bin/activate
   ```

3. **Install the SDK:**

   ```bash
   pip install openai python-dotenv
   ```

4. **Deactivate when done:**

   ```bash
   deactivate
   ```



## Reference

- <a href="https://openrouter.ai/" target="_blank">OpenRouter</a>&mdash;Official Web Site
  - [Sign up for OpenRouter](https://openrouter.ai/sign-up/)
    The account is free. You can skip providing a payment method.
  - [OpenRouter QuickStart](https://openrouter.ai/docs/quickstart)
    With code samples in Python and TypeScript
  - [Chat Completion Reference](https://openrouter.ai/docs/api/api-reference/chat/create-a-chat-completion)
    With examples in all major languages and an AI assistant on the page.
  
- <a href="https://github.com/openai/openai-python" target="_blank">OpenAI Python SDK</a>&mdash;OpenAI GitHub Repo

- [Model Ranking and Price Comparison](https://profbird.github.io/OpenCodeInfo/)&mdash;Brian Bird

- [Notes on Gemini AI Studio and API](CS212-Unit08-1-ChatCompletionAPI_Gemini.md)&mdash;Brian Bird



*Parts of this document were drafted using Gemini Flash 2.5 and revised using Claude Sonnet 5.5.*

---

<a href="http://creativecommons.org/licenses/by-sa/4.0/" target="_blank"><img src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" alt="Creative Commons License"></a> AI Programming 1 lecture notes by <a href="https://profbird.dev" target="_blank">Brian Bird</a>, written in 2025 and revised in <time>2026</time>, are licensed under a <a href="http://creativecommons.org/licenses/by-sa/4.0/" target="_blank">Creative Commons Attribution-ShareAlike 4.0 International License</a>. 

---