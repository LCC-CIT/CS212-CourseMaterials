<h1>Build a Weather MCP Server</h1>

[TOC]

## Introduction

In this tutorial, you will build a Model Context Protocol (MCP) server that provides weather forecasts and alerts. This tutorial was adapted from [Build an MCP Server](https://modelcontextprotocol.io/docs/develop/build-server). The purpose was to simplify the tutorial for beginning Python programmers. The main changes were to use `pip` instead of `uv`,  use the ["official" MCP Server SDK](https://modelcontextprotocol.github.io/python-sdk/) and to not use [Python type hints](https://docs.python.org/3/library/typing.html).

This tutorial includes instructions for testing the server with two different MCP clients: 

- Claude Desktop
- VS Code

### Prerequisites

- Python 3.10 or higher.
- [Claude Desktop App](https://claude.ai/download) or [Visual Studio Code](https://code.visualstudio.com) installed.



## Project Setup

We will use standard Python tools (`venv` and `pip`) to set up the environment. The environment will include the ["official" Python MCP SDK](https://modelcontextprotocol.github.io/python-sdk/) from the Anthropic MCP open-source project. 

- First make a new project folder with a name like `weather-mcp`
  - In that folder, using a terminal, do the following :

```bash
# 1. Create a virtual environment
python -m venv weather-venv

# 2. Activate the environment
# On macOS/Linux:
source weather-venv/bin/activate
# On Windows:
weather-venv\Scripts\activate

# 3. Install the official Python MCP SDK with CLI tools
# and install httpx, a modern, fast, asynchronous HTTP client library
cd weather-venv
pip install "mcp[cli]" httpx
cd ..
```

**Note**: on a Mac, use the command `python3` instead of `python`.

## Writing the Server

Create a file named `server.py` in *weather-mcp*. To keep things simple and avoid complex type definitions, we will define our tool inputs using standard Python dictionaries.

```python
import asyncio
import httpx
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server

# Create and initialize the server object
server = Server("weather-server")

# NWS requires a User-Agent header to identify your app
NWS_HEADERS = {
    "User-Agent": "weather-mcp-server/1.0",
    "Accept": "application/geo+json"
}

# --- 1. Define the Logic ---

async def get_forecast(latitude, longitude):
    """
    Fetches the weather forecast for a specific location from the NWS API.

    Args:
        latitude (float): The latitude of the location.
        longitude (float): The longitude of the location.

    Returns:
        str: A formatted string containing the forecast for the next few periods.
    """
    async with httpx.AsyncClient() as client:
        # Step 1: Get the Grid Point (NWS requires converting Lat/Long to a Grid ID)
        # We round coordinates to 4 decimal places to avoid API errors
        lat_clean = f"{float(latitude):.4f}"
        long_clean = f"{float(longitude):.4f}"
        points_url = f"https://api.weather.gov/points/{lat_clean},{long_clean}"
        
        response = await client.get(points_url, headers=NWS_HEADERS)
        response.raise_for_status()
        points_data = response.json()

        # Extract the forecast URL from the metadata
        forecast_url = points_data["properties"]["forecast"]

        # Step 2: Get the actual Forecast
        response = await client.get(forecast_url, headers=NWS_HEADERS)
        response.raise_for_status()
        forecast_data = response.json()

        # Format the next few periods into a readable string
        periods = forecast_data["properties"]["periods"]
        text = []
        for p in periods[:3]:  # Just show the next 3 periods
            text.append(f"{p['name']}: {p['detailedForecast']}")
        
        return "\n".join(text)

async def get_alerts(state):
    """
    Fetches active weather alerts for a specific US state.

    Args:
        state (str): Two-letter state code (e.g., 'CA', 'TX').

    Returns:
        str: A formatted string listing active alerts or a message indicating none.
    """
    # NWS requires uppercase state codes (e.g., "TX")
    state = state.upper()
    url = f"https://api.weather.gov/alerts/active?area={state}"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=NWS_HEADERS)
        response.raise_for_status()
        data = response.json()

        if not data.get("features"):
            return f"No active alerts for {state}."

        alerts = []
        for feature in data["features"][:5]: # Limit to 5 alerts
            props = feature["properties"]
            alerts.append(f"• {props['event']}: {props['headline']}")
        
        return "\n".join(alerts)

# --- 2. Register Tools ---

@server.list_tools()
async def handle_list_tools():
    """
    Defines the tools available to the client (LLM).

    Returns:
        list[types.Tool]: A list of tool definitions including their names,
                          descriptions, and input schemas (JSON Schema).
    """
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
    """
    Executes a tool call requested by the client.

    Args:
        name (str): The name of the tool to execute.
        arguments (dict | None): The arguments provided by the client.

    Returns:
        list[types.TextContent]: The output of the tool execution wrapped in an MCP text content object.
    
    Raises:
        ValueError: If the tool name is unknown.
    """
    try:
        if name == "get-forecast":
            result = await get_forecast(arguments["latitude"], arguments["longitude"])
            return [types.TextContent(type="text", text=result)]
        
        elif name == "get-alerts":
            result = await get_alerts(arguments["state"])
            return [types.TextContent(type="text", text=result)]
        
        raise ValueError(f"Unknown tool: {name}")

    except httpx.HTTPStatusError as e:
        # Handle API errors gracefully
        return [types.TextContent(type="text", text=f"API Error: {e}")]
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error: {str(e)}")]

# --- 3. Run the Server ---

async def main():
    """
    Main entry point for the MCP server.
    
    Sets up the standard input/output (stdio) streams and runs the server
    loop to handle incoming requests from the client.
    """
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



## Testing

### Configuring Claude Desktop as a Client

Now we need to tell the Claude Desktop app where to find this script. We do this by editing a configuration file.

1. **Locate the configuration file:**

   - **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows:** `C:\Users\YourUserName\AppData\Roaming\Claude\claude_desktop_config.json`

   *If the file doesn't exist, create it.*

2. Add your server configuration:

   You must use the absolute path to the python executable inside your virtual environment so Claude can run it without needing you to activate the environment manually.

   *Replace `/ABSOLUTE/PATH/TO/` with the actual path on your machine.*

   ```json
   {
     "mcpServers": {
       "weather-server": {
         "command": "/ABSOLUTE/PATH/TO/weather-mcp/weather-venv/bin/python",
         "args": ["/ABSOLUTE/PATH/TO/weather-mcp/server.py"]
       }
     }
   }
   ```
   
   > **Note for Windows Users:** Your *command* path will be: `C:\\ABSOLUTE\\PATH\\TO\\weather-mcp\\weather-venv\\Scripts\\python.exe`. Your *args* path will also use `\\` delimiters.

#### Testing with Claude Desktop

1. **Restart Claude Desktop:** You must quit and reopen the app for the config to load.

2. **Look for the weather-server:** Click on the "select tools" button, you should see *weather-server.* If you click it, you should see  *get-forecast* and *get-alerts*.

3. **Ask a Question**:

   - For the weather forecast, you can ask either by latitude and logitude <u>or</u> by city and state. For example:
     - What is the forecast for lat 44.0521, lon 123.0868?
     - What is the forecast for Springfield, OR?

   Claude will:
   
   1. Ask for permission to use the tool.
   2. Run your Python script in the background.
   3. Get the result ("sunny with a high of 75°F").
   4. Write a response based on that data.



### Configuring VS Code as a Client

To switch from Claude Desktop to VS Code (GitHub Copilot) as a client, you only need to make a configuration file for use with VS Code. Nothing needs to be changed in the server code.

Instead of creating  a global config file like you did for Claude, you will create a project-specific config file for VS Code.

**Instructions:**

1. Inside your `weather-mcp` folder, create a new subfolder named `.vscode`.

2. Inside that folder, create a file named `mcp.json`.

3. Add the following configuration.

   - **Note:** The root key in the JSON changes from `mcpServers` (for Claude) to `servers` (for VS Code).

   ```json
   {
     "servers": {
       "weather-server": {
         "command": "/ABSOLUTE/PATH/TO/weather-mcp/venv/bin/python",
         "args": ["/ABSOLUTE/PATH/TO/weather-mcp/server.py"]
       }
     }
   }
   ```
   
   *(On Windows, remember to use double backslashes `\\` in paths and that the python command is in `Scripts` not `bin`.)*

#### Testing with VS Code

Use the Copilot Chat sidebar.

**Instructions:**

1. **Reload VS Code:** Press `Cmd+Shift+P` (macOS) or `Ctrl+Shift+P` (Windows), type "Reload Window", and press Enter to ensure the new config is loaded.

2. **Open Copilot Chat:** Click the Chat icon in the sidebar.

3. **Select agent mode:** In the agent/ask/plan drop-down, select agent. 

4. **Enable the weather server tool.** Click on the *configure tools* icon. In the list of tools, you should see `weather-server` listed. Check it's checkbox.

5. Ask a Question:

   - For the weather forecast, you can ask either by latitude and logitude <u>or</u> by city and state. For example:
     - What is the forecast for lat 44.0521, lon 123.0868?
     - What is the forecast for Springfield, OR?

   Claude will:

   1. Ask for permission to use the tool.
   2. Run your Python script in the background.
   3. Get the result ("sunny with a high of 75°F").
   4. Write a response based on that data.



## Troubleshooting

If the *weather-server* doesn't appear in the list of tools or the tool fails:

1. Check the logs:
   - **macOS:** `~/Library/Logs/Claude/mcp.log`
   - **Windows:** `%APPDATA%\Claude\logs\mcp.log`
2. Ensure you used the <u>absolute path</u> to the python executable in the `weather-venv` folder, not the system python.



## References

[Build an MCP Server](https://modelcontextprotocol.io/docs/develop/build-server)&mdash;Model Context Protocol Project, an open-source project managed by [Anthropic](https://www.anthropic.com).

[MCP Python SDK](https://modelcontextprotocol.github.io/python-sdk/)&mdash;The "official" SDK from the Anthropic MCP open-source project. The GitHub repository is [here.](https://github.com/modelcontextprotocol/python-sdk)

 [How to use the MCP server in VS Code](https://www.youtube.com/watch?v=91_6PnC9oUU)  
This video demonstrates the "Agent mode" in VS Code and how to access MCP tools within the GitHub Copilot chat interface.



*Note: This tutorial was initially drafted using Gemini 3 (2025).*

---

[![Creative Commons License](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/) AI Programming 1 course materials by [Brian Bird](https://profbird.dev), written in <time>2025</time>, are licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/). 

---

