# Building a Weather MCP Server for Claude Desktop

In this tutorial, you will build a Model Context Protocol (MCP) server that provides weather data. This tutorial is adapted from <a href="https://modelcontextprotocol.io/docs/develop/build-server" target="_blank">Build an MCP Server</a> on the Model Context Protocol web site.

This tutorial includes instructions for testing the server with:

- Claude Desktop
- VS Code

## Prerequisites

- Python 3.10 or higher
- <a href="https://claude.ai/download" target="_blank">Claude Desktop App</a> installed
- Basic familiarity with the terminal

## 1. Project Setup

We will use standard Python tools (`venv` and `pip`) to set up the environment.

Bash

```
# 1. Create a project folder
mkdir weather-mcp
cd weather-mcp

# 2. Create a virtual environment
python -m venv venv

# 3. Activate the environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# 4. Install the MCP SDK
pip install mcp
```

## 2. Writing the Server

Create a file named `server.py`. We will use the standard `mcp` library. To keep things simple and avoid complex type definitions, we will define our tool inputs using standard Python dictionaries.

Python

```
import asyncio
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server

# Initialize the server
server = Server("weather-server")

# --- 1. Define the Logic (Plain Python Functions) ---

async def get_forecast(latitude, longitude):
    # In a real app, this would call an API like NWS or OpenWeather
    return f"The forecast for {latitude}, {longitude} is sunny with a high of 75°F."

async def get_alerts(state):
    return f"No active weather alerts for {state}."

# --- 2. Register Tools ---

@server.list_tools()
async def handle_list_tools():
    return [
        types.Tool(
            name="get-forecast",
            description="Get weather forecast for a location",
            inputSchema={
                "type": "object",
                "properties": {
                    "latitude": {"type": "number"},
                    "longitude": {"type": "number"},
                },
                "required": ["latitude", "longitude"],
            },
        ),
        types.Tool(
            name="get-alerts",
            description="Get weather alerts for a state",
            inputSchema={
                "type": "object",
                "properties": {
                    "state": {"type": "string", "description": "Two-letter state code (e.g. CA, NY)"},
                },
                "required": ["state"],
            },
        ),
    ]

@server.call_tool()
async def handle_call_tool(name, arguments):
    if name == "get-forecast":
        return [
            types.TextContent(
                type="text", 
                text=await get_forecast(arguments["latitude"], arguments["longitude"])
            )
        ]
    
    elif name == "get-alerts":
        return [
            types.TextContent(
                type="text", 
                text=await get_alerts(arguments["state"])
            )
        ]
    
    raise ValueError(f"Unknown tool: {name}")

# --- 3. Run the Server (Stdio) ---

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="weather",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())
```

## 3. Configuring Claude Desktop

Now we need to tell the Claude Desktop app where to find this script. We do this by editing a configuration file.

1. **Locate the configuration file:**

   - **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

   *If the file doesn't exist, create it.*

2. Add your server configuration:

   You must use the absolute path to the python executable inside your virtual environment so Claude can run it without needing you to activate the environment manually.

   *Replace `/ABSOLUTE/PATH/TO/` with the actual path on your machine.*

   JSON

   ```
   {
     "mcpServers": {
       "weather-server": {
         "command": "/ABSOLUTE/PATH/TO/weather-mcp/venv/bin/python",
         "args": ["/ABSOLUTE/PATH/TO/weather-mcp/server.py"]
       }
     }
   }
   ```

   > **Note for Windows Users:** Your paths will look like `C:\\Users\\Name\\weather-mcp\\venv\\Scripts\\python.exe`. Remember to use double backslashes `\\` in JSON.

## 4. Testing

1. **Restart Claude Desktop:** You must completely quit and reopen the app for the config to load.

2. **Look for the Icon:** You should see a plug icon (🔌) in the top right of the input box. If you click it, you should see `weather-server` listed with `get-forecast` and `get-alerts`.

3. Ask a Question:

   Type: "What is the weather like at lat 40.7, long -74.0?"1

   Claude will:2

   1. Ask for permission to use the tool.3
   2. Run your Python script in the background.4
   3. See the result ("sunny with a high of 75°F").5
   4. Write a response based on that data.6

## Troubleshooting

If the plug icon doesn't appear or the tool fails:8

1. Check the logs:9
   - **macOS:** `~/Library/Logs/Claude/mcp.log`
   - **Windows:** `%APPDATA%\Claude\logs\mcp.log`
2. Ensure you used the **absolute path** to the python executable in the `venv` folder, not the system python.



## Using VS Code as a Client

To switch this tutorial from **Claude Desktop** to **VS Code (GitHub Copilot)**, you need to change **three** specific sections.

The **Python Server Code** (`server.py`) remains exactly the same. You do not need to touch it.

### 1. Change the "Prerequisites" Section

Replace the Claude Desktop requirement with VS Code requirements.

- **Remove:** `[Claude Desktop App] installed`
- **Add:**
  - **Visual Studio Code** installed.
  - **GitHub Copilot Extension** installed in VS Code.
  - A generic **GitHub Copilot subscription** (active).

### 2. Change the "Configuring the Client" Section

Instead of editing a global config file for Claude, you will create a project-specific config file for VS Code.

**New Instructions:**

1. Inside your `weather-mcp` folder, create a new subfolder named `.vscode`.

2. Inside that folder, create a file named `mcp.json`.

3. Add the following configuration.

   - **Note:** The root key changes from `mcpServers` (Claude) to `servers` (VS Code).

   JSON

   ```
   {
     "servers": {
       "weather-server": {
         "command": "/ABSOLUTE/PATH/TO/weather-mcp/venv/bin/python",
         "args": ["/ABSOLUTE/PATH/TO/weather-mcp/server.py"]
       }
     }
   }
   ```

   *(Remember to use double backslashes `\\` in paths if you are on Windows.)*

### 3. Change the "Testing" Section

You will not use the Claude interface. Instead, you will use the Copilot Chat sidebar.

**New Instructions:**

1. **Reload VS Code:** Press `Cmd+Shift+P` (macOS) or `Ctrl+Shift+P` (Windows), type "Reload Window", and press Enter to ensure the new config is loaded.

2. **Open Copilot Chat:** Click the Chat icon in the sidebar.

3. **Check for Tools:** Look for a **paperclip icon** or an **Agent/Tools** dropdown in the chat input area. You should see `weather-server` listed.

4. Ask a Question:

   Type: "What is the weather like at lat 40.7, long -74.0?"

   Copilot will:

   1. Detect the intent to use a tool.
   2. Execute your local `server.py`.
   3. Display the result ("sunny with a high of 75°F") and answer your question.

------

... <a href="https://www.youtube.com/watch?v=91_6PnC9oUU" target="_blank">How to use the MCP server in VS Code</a> ...

This video is relevant because it visually demonstrates the "Agent mode" in VS Code and how to access MCP tools within the GitHub Copilot chat interface, which replaces the Claude Desktop testing steps.

---

The draft of this tutorial was produced by Gemini 3 (2025).

---

