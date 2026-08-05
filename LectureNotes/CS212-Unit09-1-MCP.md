---
title: Agents and MCP
description: How to use an MCP server for agentic AI 
keywords: MCP, Agentic AI
generator: Typora
author: Brian Bird
---

**CS 210, Intro to AI Programming**

<h1>Model Context Protocol (MCP)</h1>

| Topics                                   |                                                              |
| ---------------------------------------- | ------------------------------------------------------------ |
| 1. What is AI, Python                    | 6. ANN: Image recognition                                    |
| 2.  Symbolic AI                          | 7. Generative AI                                             |
| 3. Classical machine learning: training  | 8. Calling the chat completion API                           |
| 4. Classical machine learning: inference | 9. <mark>Model Context Protocol</mark>                       |
| 5. More ML + History of AI               | 10. Social and ethical issues  <br />Term project completion |
|                                          | 11. Final project presentation                               |

<h2>Contents</h2>

[TOC]

## Introduction



![McpArchitectureDiagram](Images/McpArchitectureDiagram.png)

1. **The Client is the Orchestrator:** The diagram correctly places the **MCP Client (App)** in the center. In the MCP architecture, the "Host" application (like Claude Desktop or an IDE) is responsible for maintaining the connection to the LLM and the connections to the MCP Servers. The Servers do not talk directly to the LLM; they talk to the Client.
2. **LLM as a "Brain" (Not a Router):** The connection shows `App <--> LLM`. This is accurate. The App sends the user's prompt and the available tool definitions to the LLM. The LLM returns a "tool call" (a decision to use a specific tool), which the App then executes against the MCP Server.
3. **Separation of Server and Tool:** You have distinct boxes for `MCP Server 1` and `FS` (File System). This is a crucial distinction. The **MCP Server** acts as a translator/adapter. It speaks the MCP protocol on one side and the specific API of the tool (like standard file I/O or the GitHub API) on the other.
4. **Local vs. Remote Abstraction:** The diagram correctly identifies that MCP can handle both:
   - **Local Server (via Stdio):** Represented by the FS example. This runs as a subprocess on the user's machine.
   - **Remote Server (via SSE/HTTP):** Represented by the "Remote server" label. MCP supports connecting to agents or servers running on different infrastructure.



## Examples of MCP Hosts

These are freely available applications that incorporate MCP client code so that they can use MCP servers.

- Claude Desktop

- Visual Studio Code

- LM Studio





## Reference

[What is the Model Context Protocol (MCP)?](https://modelcontextprotocol.io/docs/getting-started/intro)&mdash;Model Context Protocol Project web site by Anthropic.

[Use MCP Servers](https://lmstudio.ai/docs/app/mcp)&mdash;LM Studio documentation.



*Note: Some parts of this document were drafted using Gemini 3.0 (2025).*

---

[![Creative Commons License](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/) Intro to AI Programming lecture notes by [Brian Bird](https://profbird.dev), written in <time>2025</time>, are licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/). 

---