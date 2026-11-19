---
title: AI Game Opponent
description: Building an AI game opponent for the dots and boxes game.
keywords: OpenAI, chat-completion
generator: Typora
author: Brian Bird
---

**CS 212, AI Programming 1**

<h1>Building an AI Game Opponent</h1>

<h2>Using the Dots and Boxes Game Example</h2>

<h2>Contents</h2>

[TOC]

## Review: Calling a Chat Completion API

From [Calling a Chat-Completion API](CS212-Unit08-1-ChatCompletionAPI.md):

- Use the OpenAI Python SDK, pointed at OpenRouter. Keep the API key out of your code.
- A request sends a model name and a list of messages. Each message has a `role` (`system`, `user`, or `assistant`) and `content`.
- The reply is in `response.choices[0].message.content`.
- The API is stateless, so every request must include everything the model needs to know.

In the example below, the key is in a file named `.env` in the project folder:

```
OPENROUTER_API_KEY=your-key-here
```

Add `.env` to your `.gitignore` file so the key never gets committed. Install the packages with `pip install openai python-dotenv`.

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

# Send the model a system message (rules) and a user message (the question).
response = client.chat.completions.create(
    model="baidu/ernie-5.5-flash-preview:free",
    messages=[
        {"role": "system", "content": "You are a helpful tutor. Answer in two sentences."},
        {"role": "user", "content": "What is a token?"},
    ],
)

# The model's reply is the content of the first choice.
print(response.choices[0].message.content)
```

## Introduction

An LLM will serve as the computer opponent in Dots and Boxes. Your program still runs the game: it keeps track of the board, enforces the rules, and keeps score. On the AI's turn, it sends the board state to the LLM through the OpenRouter API and gets a move back.

Unlike symbolic game AI (GOFAI)[^1], the LLM doesn't use a search algorithm to look at all possible moves. It reads the board description and suggests a move, which may be a poor choice or even illegal, so your program must validate every move.

[^1]: GOFAI stands for "Good Old-Fashioned AI," a nickname for symbolic AI. It uses hand-written rules and search algorithms, such as minimax, instead of learning from data.

Board used in these notes: 3x3 dots (2x2 boxes), rows and columns numbered 0–2.

### The Dots and Boxes Game

Dots and Boxes is a two-player pencil-and-paper game played on a grid of dots. Players take turns drawing a line between two neighboring dots. A player who draws the fourth side of a box claims that box, scores a point, and takes another turn. When all the boxes are claimed, the player with the most boxes wins.

Example code, in the <a href="https://github.com/LCC-CIT/CS212-DotsAndBoxesGame" target="_blank">CS212-DotsAndBoxesGame</a> repository on GitHub:

- <a href="https://github.com/LCC-CIT/CS212-DotsAndBoxesGame/tree/main/DotsAndBoxes" target="_blank">DotsAndBoxes</a>: a console version of the game for two human players.
- <a href="https://github.com/LCC-CIT/CS212-DotsAndBoxesGame/tree/main/DotsAndBoxesWithAI" target="_blank">DotsAndBoxesWithAI</a>: a version with an AI opponent that gets its moves from a model on OpenRouter. It is described in [The Example Code: DotsAndBoxesWithAI](#the-example-code-dotsandboxeswithai) below.

## High-Level Implementation Steps

1. **Define Game State Representation:** Establish a clear, unambiguous text format for the current state of the board.
2. **Create a System Instruction (Persona):** Prompt the model (any model available through OpenRouter) to adopt the persona of a highly strategic "Dots and Boxes" player and define its output format.
3. **Send the Request:** On the AI player's turn, send the current game state to the OpenRouter API (the chat completions endpoint, `https://openrouter.ai/api/v1/chat/completions`).
4. **Parse and Validate the Move:** Your application must receive the model's text output and parse it into a valid move (e.g., coordinates), then update the game board.

## Prompt Templates for Dots and Boxes

You should use a multi-part prompt that includes a **System Instruction** (static for the entire game) and a **User Prompt** (dynamic for each turn).

### 1. System Instruction (Static Setup)

This instruction is sent once per API call, as the message with `"role": "system"`, to define the model's persona, the rules, and the strict output format. **This is the most critical part.**

> **System Prompt:**
>
> ```
> You are an expert, highly strategic AI player of the game "Dots and Boxes" on a 3x3 grid of dots (2x2 boxes). Your sole objective is to win by maximizing closed boxes, focusing on forced moves and chain strategies.
> You will be provided the current game state as a JSON object.
> You MUST analyze the input JSON and respond with ONLY a single, valid, and legal move in the required JSON response format. Do NOT include any explanations, commentary, or extra text outside the required JSON.
> ```

###  2. User Prompt (Dynamic Input)

This is the JSON data structure your application sends to the OpenRouter API (as the content of the `"role": "user"` message) on the AI's turn, detailing the current state of the game.

#### Example JSON Input for Board State

The `//` comments below are only there to explain each part. Real JSON can't contain comments, so leave them out of the JSON your program sends.

```json
{
  "turn": "AI_Player",
  "board_dimensions": "3x3 dots",
  "occupied_lines": [
    // Format: [r1, c1, r2, c2] where the line connects the two coordinates
    // Example: Line from (0, 0) to (0, 1) is taken
    [0, 0, 0, 1],
    // Example: Line from (0, 0) to (1, 0) is taken
    [0, 0, 1, 0],
    // Example: Line from (1, 1) to (2, 1) is taken
    [1, 1, 2, 1]
    // ... list of ALL taken lines ...
  ],
  "closed_boxes": [
    // Format: {"r": r, "c": c, "owner": owner} where (r, c) is the top-left dot of the box
    // Example: Box at (0, 0) is closed and owned by the Human
    {"r": 0, "c": 0, "owner": "Human"},
    // Example: Box at (1, 1) is not yet closed (owner: "None")
    {"r": 1, "c": 1, "owner": "None"}
    // ... list of ALL box states (optional, can be derived from lines) ...
  ],
  "move_request": "Provide your optimal move as a JSON object."
}
```

### 3. Required JSON Response Format (Output)

In your API call, you would set `response_format` to `{"type": "json_schema", ...}` and provide a schema defining this structure. (Not every model on OpenRouter supports structured outputs, so choose one that does.)

#### Required JSON Output from the Model

```json
{
  "move": [1, 2, 2, 2]
}
```

- **`"move"`:** A list of four integers `[r1, c1, r2, c2]` representing the two adjacent dots connected by the new line. Your application must validate this move.

Requiring this JSON output format keeps the model from adding conversational text, so your program always gets a reply it can parse. It doesn't guarantee a *legal* move, though. The model might still choose a line that's already taken or one that isn't between two neighboring dots, so your program must check the move and ask again (or pick a fallback move) if it's invalid.

## The Example Code: DotsAndBoxesWithAI

The <a href="https://github.com/LCC-CIT/CS212-DotsAndBoxesGame/tree/main/DotsAndBoxesWithAI" target="_blank">DotsAndBoxesWithAI</a> example follows the four steps above, with a simpler output format: the model replies with plain text instead of JSON.

### Setup

1. Install the packages: `pip install -r requirements.txt` (installs `openai` and `python-dotenv`).
2. Copy `.env.example` to `.env` in the project folder and put your key in it:
   ```
   OPENROUTER_API_KEY=your-key-here
   ```
   The project's `.gitignore` already lists `.env`.
3. Run `python main.py` and type `AI` when asked for a player's type.

### Where the AI Code Is

| File | What it does |
| --- | --- |
| `llm_client.py` | Builds the prompt, calls OpenRouter, and parses the reply into a move. |
| `ai_player.py` | The `AIPlayer` class. It asks `llm_client` for a move, checks that the move is legal, and picks a random legal move if it isn't. |

### The Prompts

The system prompt asks for a move as plain text in the same format a human player types, `x1,y1 x2,y2`:

```
You are an AI opponent for the Dots and Boxes game. Return ONLY one legal move in the format: x1,y1 x2,y2. ...
```

The user prompt is a list of labeled lines rather than JSON. It includes the board size, the lines already drawn, the completed boxes, the scores, whose turn it is, and the list of legal moves. Giving the model the legal moves makes an illegal answer less likely.

```
BOARD_SIZE: 3
LINES_DRAWN_COUNT: 2
LINES_DRAWN: [0,0 1,0; 0,0 0,1]
...
VALID_MOVES: [1,0 2,0; 0,1 1,1; ...]
RETURN: one move in format 'x1,y1 x2,y2'
```

Note that the example labels dots `x,y` (column, row), while the JSON format earlier in these notes uses `r, c` (row, column). Either works, as long as the prompt says which one you use.

### Sending the Request and Parsing the Reply

This is the core of `request_move` in `llm_client.py`, slightly shortened:

```python
settings = dotenv_values(ENV_FILE)          # ENV_FILE is the .env next to llm_client.py
api_key = settings.get("OPENROUTER_API_KEY")
if not api_key:
    return None                             # No key: the caller picks a random move

client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)
response = client.chat.completions.create(
    model=MODEL,                            # "baidu/ernie-5.5-flash-preview:free"
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": dynamic_prompt},
    ],
)
text = (response.choices[0].message.content or "").strip()

# Find the first "x1,y1 x2,y2" in the reply and turn it into two (x, y) tuples.
match = MOVE_REGEX.search(text)
if not match:
    return None
x1, y1, x2, y2 = map(int, match.groups())
return (x1, y1), (x2, y2)
```

Because the reply is plain text, the code uses a regular expression to find the move instead of parsing JSON. The whole call is inside a `try` block, so a network error or a bad reply also returns `None`.

### Validating the Move

`AIPlayer.choose_move` only uses the model's move if it is in the list of legal moves. If there is no key, the call fails, or the move is illegal, it picks a random legal move instead. This way the game keeps working even when the model gives a bad answer or you're offline.

### Ideas for Improving the Example

- Change the output to the JSON format shown above and use `response_format` with a JSON schema.
- If the model's move is illegal, send it a follow-up message saying why and ask again before falling back.
- Replace the random move with a simple strategy: complete a box if you can, and avoid drawing the third side of a box.
- Try different models by changing `MODEL` in `llm_client.py`, and compare how well they play.



## Reference

<a href="https://openrouter.ai/models" target="_blank">OpenRouter Models</a>

<a href="https://openrouter.ai/docs/quickstart" target="_blank">OpenRouter Quickstart</a>

<a href="https://openrouter.ai/docs/features/structured-outputs" target="_blank">OpenRouter Structured Outputs</a>

<a href="https://www.youtube.com/watch?v=YVuoIxil9Sw" target="_blank">Building an LLM-Powered Text-Based AI RPG</a>&mdash; This video shows how an LLM can be used to drive game mechanics in a text-based RPG.



Note: Parts of this document were drafted using Gemini Flash 2.5 (2025).

---

<a href="http://creativecommons.org/licenses/by-sa/4.0/" target="_blank"><img src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" alt="Creative Commons License"></a> AI Programming 1 lecture notes by <a href="https://profbird.dev" target="_blank">Brian Bird</a>, written in <time>2025</time>, are licensed under a <a href="http://creativecommons.org/licenses/by-sa/4.0/" target="_blank">Creative Commons Attribution-ShareAlike 4.0 International License</a>. 

---