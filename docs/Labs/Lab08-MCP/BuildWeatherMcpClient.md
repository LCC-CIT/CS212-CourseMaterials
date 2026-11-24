---
title: Building an MCP Client
---

<h1>Building an MCP Client</h1>

<h2>Contents</h2>

[TOC]

## Introduction

In this tutorial, you will build a Model Context Protocol (MCP) client that can connect to any MCP server. You will use a large language model (LLM) as the "brain" to decide when to use tools and to generate natural language responses.

This tutorial was adapted from the <a href="https://modelcontextprotocol.io/docs/develop/build-client" target="_blank">Build a Client</a> tutorial. The purpose was to simplify the tutorial for beginning Python programmers. The main changes were to use the <a href="https://openrouter.ai/" target="_blank">OpenRouter API</a> instead of the Anthropic Claude API and to not use <a href="https://docs.python.org/3/library/typing.html" target="_blank">Python type hints</a>. OpenRouter lets you use models from many companies (Anthropic, OpenAI, Google, and others) with one API key.

## Prerequisites

- The `weather-mcp` project you made in the [Build a Weather MCP Server](BuildWeatherMcpServer.md) tutorial. You don't need to start the server; the client will start it for you.
- An OpenRouter account and API key (see below).

## Project Setup

We will add the client to the `weather-mcp` project you already have. In a terminal, go to the `weather-mcp` folder and run:

```bash
# Install the OpenAI SDK and python-dotenv
uv add openai python-dotenv
```

- **openai**: OpenRouter uses the same API format as OpenAI, so we can use OpenAI's Python SDK to talk to it.
- **python-dotenv**: reads settings, like your API key, from a `.env` file.

### Getting an OpenRouter API Key

1. Go to <a href="https://openrouter.ai/" target="_blank">openrouter.ai</a> and sign up.
2. Go to the <a href="https://openrouter.ai/settings/keys" target="_blank">Keys</a> page and create a key. Copy it; you won't be able to see it again.
3. This tutorial uses a free model. Models whose names end in `:free` cost nothing. They have low daily request limits, which are higher if you have purchased credits.

### Choosing a Model

The model you choose <u>must support tools</u> (also called *tool calling* or *function calling*). If it doesn't, OpenRouter will return an error, or the model will answer without ever calling your weather tools. This <a href="https://openrouter.ai/models?supported_parameters=tools" target="_blank">list of models that support tools</a> shows which ones you can use; filter it by price to see only the free ones. Free model names change over time, so check the list if a name stops working.

Small models that support tools sometimes pass the wrong arguments or skip a tool they should have used. If you get poor results, try a larger model.

### Saving the Key in a .env File

Your API key is like a password, so don't put it in your code. Instead, you will save it in a file named `.env` that stays on your computer.

1. In your `weather-mcp` folder, create a file named `.env` (with nothing before the dot). Put this line in it, with your key in place of `your_key_here`:

   ```
   OPENROUTER_API_KEY=your_key_here
   ```

   **Note**: On Windows, Notepad may save the file as `.env.txt`. Creating the file in VS Code avoids this.

2. Keep the key out of Git. Open the `.gitignore` file in your `weather-mcp` folder (`uv init` made it) and add this line at the end:

   ```
   .env
   ```

   Now, if you push your project to GitHub, your key won't go with it.

## Writing the Client Code

Create a file named `client.py` in your `weather-mcp` folder, next to `server.py`. This script will start your weather server, get its list of tools, send them to the model, and handle the conversation loop.

```python
import asyncio
import json
import os
import sys

# Import MCP classes
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Import the OpenAI SDK (OpenRouter uses the same API format)
from openai import OpenAI

# Import the function that reads the .env file
from dotenv import dotenv_values

# 1. Configuration
# ----------------
# Read the settings in .env into a dictionary.
settings = dotenv_values(".env")
OPENROUTER_API_KEY = settings.get("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    print("Error: No OPENROUTER_API_KEY found in the .env file.")
    sys.exit(1)

# The model to use. It must support tool calling.
MODEL = "google/gemma-4-31b-it:free"

# server.py is in the same folder as this file
SERVER_SCRIPT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "server.py")

async def main():
    # 2. Connect to the MCP Server
    # ----------------------------
    # We define how to launch the server (just like in the config file)
    server_params = StdioServerParameters(
        command=sys.executable,
        args=[SERVER_SCRIPT_PATH]
    )

    print("Connecting to server...")
    
    # Start the server and connect to it via standard input/output (stdio)
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Perform the handshake
            await session.initialize()
            
            # 3. Discover Tools
            # -----------------
            # Ask the server what tools it has available
            mcp_tools_list = await session.list_tools()
            
            # Convert MCP tools into the format the OpenRouter API expects
            tools = []
            for tool in mcp_tools_list.tools:
                tools.append({
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.inputSchema
                    }
                })
            
            print(f"Found {len(tools)} tools.")

            # 4. Connect to OpenRouter
            # ------------------------
            client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=OPENROUTER_API_KEY
            )
            
            # Start the conversation loop
            while True:
                user_input = input("\nYou: ")
                if user_input.lower() in ["exit", "quit"]:
                    break

                # 5. Send Request to the Model
                # ----------------------------
                # We send the user's text AND the list of tools
                messages = [{"role": "user", "content": user_input}]
                response = client.chat.completions.create(
                    model=MODEL,
                    messages=messages,
                    tools=tools
                )
                message = response.choices[0].message

                # 6. Handle Tool Calls
                # --------------------
                # If the model didn't ask for a tool, just print its answer
                if not message.tool_calls:
                    print(f"Assistant: {message.content}")
                    continue

                # Add the model's tool request to the conversation
                messages.append(message)

                # The model may ask for more than one tool call
                for call in message.tool_calls:
                    print(f"[Model wants to call tool: {call.function.name}]")

                    # The arguments come as a JSON string, so convert them to a dictionary
                    arguments = json.loads(call.function.arguments)

                    # Execute the tool on the MCP Server
                    result = await session.call_tool(call.function.name, arguments=arguments)

                    # Get the text result from the server
                    tool_output = result.content[0].text
                    print(f"[Tool Output: {tool_output}]")

                    # Add the result to the conversation
                    messages.append({
                        "role": "tool",
                        "tool_call_id": call.id,
                        "content": tool_output
                    })

                # Send the conversation back to the model to get a final answer
                final_response = client.chat.completions.create(
                    model=MODEL,
                    messages=messages,
                    tools=tools
                )
                print(f"Assistant: {final_response.choices[0].message.content}")

if __name__ == "__main__":
    asyncio.run(main())
```



## Running the Client

In your `weather-mcp` folder, run:

```bash
uv run client.py
```

Type a question at the `You:` prompt. Type `exit` or `quit` to stop.

## Expected Interaction

When you run the script, you should see something like this. Your forecast and alerts will depend on the weather that day, and the model's wording will vary.

```
Connecting to server...
Found 2 tools.

You: What is the weather in Eugene, OR?
[Model wants to call tool: get-forecast]
[Tool Output: Today: A chance of rain after 2pm. Cloudy. High near 58, with temperatures falling to around 56 in the afternoon. South southeast wind 3 to 8 mph. Chance of precipitation is 40%. New rainfall amounts less than a tenth of an inch possible.
Tonight: Rain likely before 10pm. Mostly cloudy, with a low around 48. South wind 6 to 9 mph. Chance of precipitation is 60%.
Wednesday: A slight chance of rain after 4pm. Partly sunny. High near 63, with temperatures falling to around 60 in the afternoon. South wind around 7 mph. Chance of precipitation is 20%.]
Assistant: It's cloudy in Eugene today with a high near 58°F and a 40% chance of rain this afternoon. Rain is likely tonight, with a low around 48°F.

You: Are there any weather alerts for NY?
[Model wants to call tool: get-alerts]
[Tool Output: • High Wind Watch: High Wind Watch issued November 24 at 1:20AM EST until November 27 at 1:00AM EST by NWS Upton NY]
Assistant: Yes. The National Weather Service has issued a High Wind Watch for parts of New York, in effect until 1:00 AM EST on November 27.
```

### What is happening here?

1. **Startup:** Your `client.py` starts the `server.py` process and connects to it.
2. **Discovery:** The client asks the server "What can you do?" (`session.list_tools()`).
3. **Translation:** The client converts these tools into the format the OpenRouter API expects.
4. **Reasoning:** You ask a question. The model analyzes it and decides "I need to use the `get-forecast` tool."
5. **Execution:** Your client takes that decision, sends a command to the MCP server, gets the string result, and adds it to the conversation.
6. **Final Response:** The client sends the conversation back to the model, which reads the tool output and writes a natural language answer.

To keep the code simple, the client doesn't remember earlier questions, so each question starts a new conversation. Also, if the model asks for another tool after it sees the first result, the client prints `Assistant: None`. If that happens, try asking your question a different way.

## References

<a href="https://modelcontextprotocol.io/docs/develop/build-client" target="_blank">Build an MCP Client</a>&mdash;Model Context Protocol Project, an open-source project managed by <a href="https://www.anthropic.com" target="_blank">Anthropic</a>.

<a href="https://modelcontextprotocol.github.io/python-sdk/" target="_blank">MCP Python SDK</a>&mdash;The "official" SDK from the Anthropic MCP open-source project. The GitHub repository is <a href="https://github.com/modelcontextprotocol/python-sdk" target="_blank">here.</a>

<a href="https://openrouter.ai/docs/quickstart" target="_blank">OpenRouter Quickstart</a> and <a href="https://openrouter.ai/docs/features/tool-calling" target="_blank">Tool Calling</a>&mdash;OpenRouter's documentation for the API used in this tutorial.

<a href="https://pypi.org/project/python-dotenv/" target="_blank">python-dotenv</a>&mdash;The package that reads the `.env` file.


*Note: This tutorial was initially drafted using Gemini 3 (2025).*

---

<a href="http://creativecommons.org/licenses/by-sa/4.0/" target="_blank"><img src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" alt="Creative Commons License"></a> AI Programming 1 course materials by <a href="https://profbird.dev" target="_blank">Brian Bird</a>, written in <time>2025</time>, are licensed under a <a href="http://creativecommons.org/licenses/by-sa/4.0/" target="_blank">Creative Commons Attribution-ShareAlike 4.0 International License</a>. 

---

