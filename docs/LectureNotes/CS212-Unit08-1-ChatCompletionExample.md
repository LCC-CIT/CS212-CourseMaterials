---
title: Chat Completion Example
description: Chat completion example in the dots and boxex game with an AI opponent.
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

- Use the OpenAI Python SDK, pointed at OpenRouter. Keep the API key in the `OPENROUTER_API_KEY` environment variable, not in your code.
- A request sends a model name and a list of messages. Each message has a `role` (`system`, `user`, or `assistant`) and `content`.
- The reply is in `response.choices[0].message.content`.
- The API is stateless, so every request must include everything the model needs to know.

```python
from dotenv import dotenv_values
from openai import OpenAI

# Read the settings in .env into a dictionary
settings = dotenv_values(".env")

# Point the OpenAI client at OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=settings["OPENROUTER_API_KEY"],
)

# Send the model a system message (rules) and a user message (the question)
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



**Q: What additional code would be needed for a multi-turn chat session?**
(See the notes from the previous class)



## Overiew: Using an LLM as an Opponent in a Game

An LLM will serve as the computer opponent in Dots and Boxes. Your program still runs the game: it keeps track of the board, enforces the rules, and keeps score. On the AI's turn, it sends the board state to the LLM through the OpenRouter API and gets a move back.

Unlike symbolic  game AI (GOFAI[^1]), the LLM doesn't use a search algorithm to look at all possible moves. It reads the board description and suggests a move, which may be a poor choice or even illegal, so your program must validate every move.

Board used in these notes: 3x3 dots (2x2 boxes), rows and columns numbered 0–2.

### The Dots and Boxes Game

Dots and Boxes is a two-player pencil-and-paper game played on a grid of dots. Players take turns drawing a line between two neighboring dots. A player who draws the fourth side of a box claims that box, scores a point, and takes another turn. When all the boxes are claimed, the player with the most boxes wins.

Example code: <a href="https://github.com/LCC-CIT/CS212-Examples/tree/main/DotsAndBoxes" target="_blank">DotsAndBoxes</a> (a console version of the game for two human players, in the CS212-Examples repository on GitHub).

## High-Level Implementation Steps

1. **Define Game State Representation:** Define a text format (JSON) for repersenting the current state of the game board.
2. **Create a System Prompt (Persona):** Prompt the model (any model available through OpenRouter) to adopt the persona of a highly strategic "Dots and Boxes" player and define its output format.
3. **Send the Request:** On the human player's turn, send the current game state to the OpenRouter API (the chat completions endpoint, `https://openrouter.ai/api/v1/chat/completions`).
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

| File                | What it does                                                 |
| ------------------- | ------------------------------------------------------------ |
| `llm_client.py`     | The `ask_llm` function. It sends a system prompt and a user prompt to a model on OpenRouter and returns the reply. |
| `ai_player.py`      | The `AIPlayer` class and helper functions. They describe the board in a prompt, read the move out of the model's reply, and check that the move is legal. |
| `test_ai_player.py` | A test driver. Part 1 checks the prompt and reply code without calling the model. Part 2 asks the model for a real move. |

### Calling the Model

`llm_client.py` is the same pattern as the review example at the top of these notes:

```python
settings = dotenv_values(Path(__file__).with_name(".env"))  # the .env next to this file

def ask_llm(system_prompt, user_prompt):
    api_key = settings.get("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("No OPENROUTER_API_KEY found in the .env file")

    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)
    response = client.chat.completions.create(
        model=MODEL,                        # "baidu/ernie-5.5-flash-preview:free"
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    return response.choices[0].message.content or ""
```

### The Prompts

The system prompt asks for a move as plain text in the same format a human player types, `x1,y1 x2,y2`:

```
You are an AI opponent in the game Dots and Boxes. Reply with ONLY one legal move in the format x1,y1 x2,y2 and nothing else. ...
```

`build_prompt` in `ai_player.py` writes the user prompt. It describes the board, the lines already drawn, and the legal moves. Giving the model the legal moves makes an illegal answer less likely.

```
The board has 3x3 dots, numbered from 0,0 (top left) to 2,2 (bottom right).
Lines already drawn: 0,0 1,0
Legal moves: 1,0 2,0; 0,1 1,1; 1,1 2,1; ...
Which line do you draw?
```

Note that the example labels dots `x,y` (column, row), while the JSON format earlier in these notes uses `r, c` (row, column). Either works, as long as the prompt says which one you use.

### Reading and Checking the Move

Because the reply is plain text, `parse_move` uses a regular expression to find the first `x1,y1 x2,y2` in it. Then `choose_move` checks that the move is legal:

```python
def choose_move(self, game_logic):
    grid = game_logic.grid
    prompt = build_prompt(grid, game_logic.get_valid_moves())
    reply = ask_llm(SYSTEM_PROMPT, prompt)

    move = parse_move(reply)
    if move is None or not grid.is_valid_line(move[0], move[1]):
        raise ValueError(f"The model did not give a legal move. It replied: {reply!r}")
    return move
```

### Handling Errors

If there's no key, the model isn't responding, or its move isn't legal, `choose_move` raises an exception. The game loop in `main.py` catches it, shows the message, and ends the game:

```python
try:
    start, end = current.choose_move(game_logic)
except Exception as error:
    print(f"AI error: {error}")
    print("The game cannot continue without the AI. Goodbye!")
    return
```

### Ideas for Improving the Example

- Change the output to the JSON format shown above and use `response_format` with a JSON schema.
- If the model's move is illegal, send it a follow-up message saying why and ask again instead of ending the game.
- If the model isn't responding, play a move using a simple strategy instead: complete a box if you can, and avoid drawing the third side of a box.
- Give the model more information, such as which boxes are complete and the scores, and see if it plays better.
- Try different models by changing `MODEL` in `llm_client.py`, and compare how well they play.



## Reference

<a href="https://openrouter.ai/models" target="_blank">OpenRouter Models</a>

<a href="https://openrouter.ai/docs/quickstart" target="_blank">OpenRouter Quickstart</a>

<a href="https://openrouter.ai/docs/features/structured-outputs" target="_blank">OpenRouter Structured Outputs</a>

<a href="https://www.youtube.com/watch?v=YVuoIxil9Sw" target="_blank">Building an LLM-Powered Text-Based AI RPG</a>&mdash; This video shows how an LLM can be used to drive game mechanics in a text-based RPG.



[^1]: GOFAI stands for "Good Old-Fashioned AI," a nickname for symbolic AI. It uses hand-written rules and search algorithms, such as minimax, instead of learning from data.

*Parts of this document were drafted using Gemini Flash 2.5 and Opus 5.5 was used for some reivisions*.

---

<a href="http://creativecommons.org/licenses/by-sa/4.0/" target="_blank"><img src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" alt="Creative Commons License"></a> AI Programming 1 lecture notes by <a href="https://profbird.dev" target="_blank">Brian Bird</a>, written in 2025, revised in <time>2026</time>, are licensed under a <a href="http://creativecommons.org/licenses/by-sa/4.0/" target="_blank">Creative Commons Attribution-ShareAlike 4.0 International License</a>. 

---