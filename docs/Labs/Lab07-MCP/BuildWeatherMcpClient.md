<h1>Building a MCP Client</h1>

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Project Setup](#project-setup)
- [Writing the Client Code](#writing-the-client-code)
- [Running the Client](#running-the-client)
- [Expected Interaction](#expected-interaction)
  - [What is happening here?](#what-is-happening-here)
- [References](#references)

## Introduction

In this tutorial, you will build a Model Context Protocol (MCP) client that can connect to any MCP server. You will use the Google Gemini API as the "brain" to decide when to use tools and to generate natural language responses.

This tutorial was adapted from the [Build a Client](https://modelcontextprotocol.io/docs/develop/build-client) tutorial. The purpose was to simplify the tutorial for beginning Python programmers. The main changes were to use `pip` instead of `uv`,  use the [Google Gemini API](https://aistudio.google.com/) instead of the Anthropic Claude API and to not use [Python type hints](https://docs.python.org/3/library/typing.html).

## Prerequisites

- Python 3.10 or higher.
- A Gemini API Key (get one [here](https://aistudio.google.com/)).
- The "Weather" MCP server you built in the previous tutorial (running locally).

## Project Setup

We will use standard Python tools (`venv` and `pip`) to set up the environment. The environment will include the ["official" Python MCP SDK](https://modelcontextprotocol.github.io/python-sdk/) from the Anthropic MCP open-source project. 

- If you don't have one already,  make a new project folder. (If you are using the weather-server from the [Build a Weather MCP Server](BuildWeatherMcpServer.html) tutorial, use the existing `weather-mcp` folder.)

- If this is a new folder that <u>doesn't</u> already have a `weather-venv` sub-folder, then, using a terminal, do the following :

  ```bash
  # Create a virtual environment
  python -m venv weather-venv
  
  # Activate the environment
  # On macOS/Linux:
  source weather-venv/bin/activate
  # On Windows using the Command Prompt:
  weather-venv\Scripts\activate
  ```

  **Notes** 

  - On a Mac, use the command `python3` instead of `python`.
  - On Windows, use the Command Prompt (cmd), not PowerShell.

  

- For both new and existing projects, add the Google Gemini SDK to the `weather-venv` folder:  

  ```bash
  # Inastall the official Gemini SDK
  # Run this command in the venv folder
  pip install mcp google-genai
  ```

  

## Writing the Client Code

Create a file named `client.py`. This script will connect to your local weather server, get the list of tools, send them to Gemini, and handle the conversation loop.

```Python
import asyncio
import os
import sys

# Import MCP classes
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Import Gemini classes
from google import genai
from google.genai import types

# 1. Configuration
# ----------------
# Set your API key here or in your environment variables
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("Error: GEMINI_API_KEY is not set.")
    sys.exit(1)

# Path to the server script you built in the previous tutorial
# IMPORTANT: Update this path to match your file system!
SERVER_SCRIPT_PATH = "/ABSOLUTE/PATH/TO/weather-mcp/server.py"
PYTHON_EXECUTABLE = sys.executable 

async def main():
    # 2. Connect to the MCP Server
    # ----------------------------
    # We define how to launch the server (just like in the config file)
    server_params = StdioServerParameters(
        command=PYTHON_EXECUTABLE,
        args=[SERVER_SCRIPT_PATH],
        env=None
    )

    print("Connecting to server...")
    
    # Establish the connection via standard input/output (stdio)
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Perform the handshake
            await session.initialize()
            
            # 3. Discover Tools
            # -----------------
            # Ask the server what tools it has available
            mcp_tools_list = await session.list_tools()
            
            # Convert MCP tools into the format Gemini expects
            gemini_tools = []
            for tool in mcp_tools_list.tools:
                gemini_tools.append({
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.inputSchema
                })
            
            print(f"Found {len(gemini_tools)} tools.")

            # 4. Initialize Gemini
            # --------------------
            client = genai.Client(api_key=GEMINI_API_KEY)
            
            # Start the conversation loop
            while True:
                user_input = input("\nYou: ")
                if user_input.lower() in ["exit", "quit"]:
                    break

                # 5. Send Request to Gemini
                # -------------------------
                # We send the user's text AND the list of tools
                response = client.models.generate_content(
                    model="gemini-2.0-flash", 
                    contents=user_input,
                    config=types.GenerateContentConfig(
                        tools=[{"function_declarations": gemini_tools}]
                    )
                )

                # 6. Handle Tool Calls
                # --------------------
                # Check if Gemini wants to call a function
                handled_tool = False
                
                # Gemini responses might contain multiple parts (text + function call)
                if response.candidates and response.candidates[0].content.parts:
                    for part in response.candidates[0].content.parts:
                        
                        # If we see a function call...
                        if part.function_call:
                            handled_tool = True
                            call = part.function_call
                            print(f"[Gemini wants to call tool: {call.name}]")
                            
                            # Execute the tool on the MCP Server
                            # We pass the arguments exactly as Gemini provided them
                            result = await session.call_tool(call.name, arguments=call.args)
                            
                            # Get the text result from the server
                            tool_output = result.content[0].text
                            print(f"[Tool Output: {tool_output}]")

                            # Send the result back to Gemini to get a final answer
                            final_response = client.models.generate_content(
                                model="gemini-2.0-flash",
                                contents=[
                                    # 1. Original User Input
                                    types.Content(role="user", parts=[types.Part(text=user_input)]),
                                    # 2. Gemini's Function Call Request
                                    types.Content(role="model", parts=[part]),
                                    # 3. The Result from the Tool
                                    types.Content(
                                        role="user", 
                                        parts=[types.Part(
                                            function_response=types.FunctionResponse(
                                                name=call.name,
                                                response={"result": tool_output}
                                            )
                                        )]
                                    )
                                ],
                                config=types.GenerateContentConfig(
                                    tools=[{"function_declarations": gemini_tools}]
                                )
                            )
                            print(f"Gemini: {final_response.text}")

                # If no tool was called, just print the text response
                if not handled_tool:
                    print(f"Gemini: {response.text}")

if __name__ == "__main__":
    asyncio.run(main())
```



## Running the Client

1. **Set your API Key:**

   - **Mac/Linux:** `export GEMINI_API_KEY="your_actual_key_here"`
   - **Windows:** `set GEMINI_API_KEY=your_actual_key_here`

2. Verify the Server Path:

   Ensure SERVER_SCRIPT_PATH in the code above points to the server.py file you created in the previous tutorial.

3. **Run the script:**

   Bash

   ```
   python client.py
   ```



## Expected Interaction

When you run the script, you should see something like this:

Plaintext

```
Connecting to server...
Found 2 tools.

You: What is the weather in San Francisco?
[Gemini wants to call tool: get-forecast]
[Tool Output: The forecast for 37.7749, -122.4194 is sunny with a high of 75°F.]
Gemini: The weather in San Francisco is sunny with a high of 75°F.

You: Is there a storm in NY?
[Gemini wants to call tool: get-alerts]
[Tool Output: No active weather alerts for NY.]
Gemini: There are currently no active weather alerts for New York.
```



### What is happening here?

1. **Handshake:** Your `client.py` starts the `server.py` process securely.
2. **Discovery:** The client asks the server "What can you do?" (`session.list_tools()`).
3. **Translation:** The client formats these tools for Gemini.
4. **Reasoning:** You ask a question. Gemini analyzes it and decides "I need to use the `get-forecast` tool."
5. **Execution:** Your client takes that decision, sends a command to the MCP server, gets the string result, and feeds it back to Gemini.
6. **Final Response:** Gemini reads the tool output and writes a natural language sentence.



## References

[Build an MCP Client](https://modelcontextprotocol.io/docs/develop/build-client)&mdash;Model Context Protocol Project, an open-source project managed by [Anthropic](https://www.anthropic.com).

[MCP Python SDK](https://modelcontextprotocol.github.io/python-sdk/)&mdash;The "official" SDK from the Anthropic MCP open-source project. The GitHub repository is [here.](https://github.com/modelcontextprotocol/python-sdk)

 [How to use the MCP server in VS Code](https://www.youtube.com/watch?v=91_6PnC9oUU)  
This video demonstrates the "Agent mode" in VS Code and how to access MCP tools within the GitHub Copilot chat interface.



*Note: This tutorial was initially drafted using Gemini 3 (2025).*

---

[![Creative Commons License](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/) AI Programming 1 course materials by [Brian Bird](https://profbird.dev), written in <time>2025</time>, are licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/). 

---

