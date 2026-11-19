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

## Introduction

An LLM will serve as the computer opponent in Dots and Boxes. Your program still runs the game: it keeps track of the board, enforces the rules, and keeps score. On the AI's turn, it sends the board state to the LLM through the OpenRouter API and gets a move back.

Unlike symbolic game AI (GOFAI)[^1], the LLM doesn't use a search algorithm to look at all possible moves. It reads the board description and suggests a move, which may be a poor choice or even illegal, so your program must validate every move.

[^1]: GOFAI stands for "Good Old-Fashioned AI," a nickname for symbolic AI. It uses hand-written rules and search algorithms, such as minimax, instead of learning from data.

Board used in these notes: 4x4 dots (3x3 boxes), rows and columns numbered 0–3.

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
> You are an expert, highly strategic AI player of the game "Dots and Boxes" on a 4x4 grid of dots (3x3 boxes). Your sole objective is to win by maximizing closed boxes, focusing on forced moves and chain strategies.
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
  "board_dimensions": "4x4 dots",
  "occupied_lines": [
    // Format: [r1, c1, r2, c2] where the line connects the two coordinates
    // Example: Line from (0, 0) to (0, 1) is taken
    [0, 0, 0, 1],
    // Example: Line from (0, 0) to (1, 0) is taken
    [0, 0, 1, 0],
    // Example: Line from (2, 2) to (3, 2) is taken
    [2, 2, 3, 2]
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
  "move": [2, 3, 3, 3]
}
```

- **`"move"`:** A list of four integers `[r1, c1, r2, c2]` representing the two adjacent dots connected by the new line. Your application must validate this move.

Requiring this JSON output format keeps the model from adding conversational text, so your program always gets a reply it can parse. It doesn't guarantee a *legal* move, though. The model might still choose a line that's already taken or one that isn't between two neighboring dots, so your program must check the move and ask again (or pick a fallback move) if it's invalid.



## Reference

<a href="https://openrouter.ai/models" target="_blank">OpenRouter Models</a>

<a href="https://openrouter.ai/docs/quickstart" target="_blank">OpenRouter Quickstart</a>

<a href="https://openrouter.ai/docs/features/structured-outputs" target="_blank">OpenRouter Structured Outputs</a>

<a href="https://www.youtube.com/watch?v=YVuoIxil9Sw" target="_blank">Building an LLM-Powered Text-Based AI RPG</a>&mdash; This video shows how an LLM can be used to drive game mechanics in a text-based RPG.



Note: Parts of this document were drafted using Gemini Flash 2.5 (2025).

---

<a href="http://creativecommons.org/licenses/by-sa/4.0/" target="_blank"><img src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" alt="Creative Commons License"></a> AI Programming 1 lecture notes by <a href="https://profbird.dev" target="_blank">Brian Bird</a>, written in <time>2025</time>, are licensed under a <a href="http://creativecommons.org/licenses/by-sa/4.0/" target="_blank">Creative Commons Attribution-ShareAlike 4.0 International License</a>. 

---