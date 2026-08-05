---
title: AI Game Opponent
description: Building an AI game opponent for the dots and boxes game.
keywords: OpenAI, chat-completion
generator: Typora
author: Brian Bird
---

**CS 210, Intro to AI Programming**

<h1>Building an AI Game Opponent</h1>

<h2>Using the Dots and Boxes Game Example</h2>

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

## Introduction

Using the Gemini API to implement an opponent for "Dots and Boxes" requires you to treat the Large Language Model (LLM) not as a player that thinks algorithmically, but as a **reasoning engine** that interprets the game state and outputs a move in a specific, parsable format. This relies heavily on **structured prompting** and a clean representation of the game board.

## High-Level Implementation Steps

1. **Define Game State Representation:** Establish a clear, unambiguous text format for the current state of the board.
2. **Create a System Instruction (Persona):** Prompt the Gemini model to adopt the persona of a highly strategic "Dots and Boxes" player and define its output format.
3. **Send the Request:** On the human player's turn, send the current game state to the Gemini API.
4. **Parse and Validate the Move:** Your application must receive the model's text output and parse it into a valid move (e.g., coordinates), then update the game board.

## Prompt Templates for Dots and Boxes

You should use a multi-part prompt that includes a **System Instruction** (static for the entire game) and a **User Prompt** (dynamic for each turn).

### 1. System Instruction (Static Setup)

This instruction is sent once per API call to define the model's persona, the rules, and the strict output format. **This is the most critical part.**

> **System Prompt:**
>
> ```
> You are an expert, highly strategic AI player of the game "Dots and Boxes" on a 4x4 grid. Your sole objective is to win by maximizing closed boxes, focusing on forced moves and chain strategies.
> You will be provided the current game state as a JSON object.
> You MUST analyze the input JSON and respond with ONLY a single, valid, and legal move in the required JSON response format. Do NOT include any explanations, commentary, or extra text outside the required JSON.
> ```

###  2. User Prompt (Dynamic Input)

This is the JSON data structure your application sends to the Gemini API on the AI's turn, detailing the current state of the game.

#### Example JSON Input for Board State

```json
{
  "turn": "AI_Player",
  "board_dimensions": "4x4",
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
    // Format: [r, c, owner] where (r, c) is the top-left dot of the box
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

In your API call, you would set the `response_mime_type` to `application/json` and provide a schema defining this structure.

#### Required JSON Output from Gemini

```json
{
  "move": [2, 3, 3, 3]
}
```

- **`"move"`:** A list of four integers `[r1, c1, r2, c2]` representing the two adjacent dots connected by the new line. Your application must validate this move.

By enforcing the JSON output format, you eliminate the risk of the model adding conversational text, ensuring a clean, machine-readable response every time.



## Reference

[Free Gemini Pro Subscription for Students](https://gemini.google/sg/students/?hl=en)

[Google AI Studio](https://aistudio.google.com/app/)

[Google Gemini API Docs](https://ai.google.dev/gemini-api/docs)

[Building an LLM-Powered Text-Based AI RPG](https://www.youtube.com/watch?v=YVuoIxil9Sw)&mdash; This video shows how an LLM can be used to drive game mechanics in a text-based RPG.



Note: Parts of this document were drafted using Gemini Flash 2.5 (2025).

---

[![Creative Commons License](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/) Intro to AI Programming lecture notes by [Brian Bird](https://profbird.dev), written in <time>2025</time>, are licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/). 

---