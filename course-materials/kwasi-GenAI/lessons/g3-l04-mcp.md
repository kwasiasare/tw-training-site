---
course: kwasi-GenAI
title: Model Context Protocol for tool and data integration
month: 3
monthTitle: Agents & Orchestration
lesson: 4
summary: 'Go from using MCP in Claude Code to understanding it as an engineer: servers, tools, and resources,
  and how an agent connects to them to gain capabilities.'
objectives:
- Define MCP as a standard protocol between an AI host and capability servers
- 'Distinguish the three core server primitives: tools, resources, and prompts'
- Explain how MCP tools map onto the tool_use loop you already know
- Connect an agent to a local (stdio) or remote (URL) MCP server
- Reason about where credentials live and why the server, not the model, holds them
- Choose between writing a custom tool and exposing one through an MCP server
video: g3-l04-mcp.mp4
quiz:
- q: What problem does MCP primarily solve?
  options:
  - It makes the model faster
  - It standardises how an AI host connects to tools and data, so integrations are reusable across hosts
  - It replaces the Messages API
  - It encrypts model weights
  answer: 1
  why: MCP is a standard protocol — write a server once and any MCP-aware host (Claude Code, your agent,
    an IDE) can use it, instead of bespoke integrations per app.
- q: Which three primitives does an MCP server expose?
  options:
  - Models, prompts, weights
  - Tools, resources, and prompts
  - Servers, clients, and hosts
  - Vectors, chunks, and embeddings
  answer: 1
  why: An MCP server exposes tools (actions the model can call), resources (data the model can read),
    and prompts (reusable prompt templates).
- q: How do MCP tools relate to the tool_use loop from earlier lessons?
  options:
  - They bypass the loop entirely
  - Each MCP tool becomes a tool the model can call via tool_use, with the result returned as tool_result
  - They replace stop_reason
  - They only work without an agent
  answer: 1
  why: MCP tools surface to the model as ordinary callable tools; the same plan-act-observe loop runs,
    just with the tool implementations living behind the MCP server.
- q: In one sentence, what is the difference between an MCP tool and an MCP resource?
  answer: A tool is an action the model can invoke; a resource is data the model can read into context.
  why: Tools do things (call an API, run a query); resources expose readable content (a file, a record)
    for the model to consume.
- q: Why is it safer for credentials to live in the MCP server rather than be passed to the model?
  answer: The model only sees the tool's inputs and outputs, never the secret, so a prompt injection or
    leaked transcript can't expose the credential.
  why: Keeping secrets server-side means the model operates on results, not keys — the same boundary principle
    you use to keep secrets out of application code.
- q: When would you expose a capability through an MCP server instead of a plain custom tool?
  answer: When you want the same capability reused across multiple hosts or agents, or shared as a standard
    interface, rather than hard-wired into one app.
  why: MCP shines for reusable, shareable integrations; a one-off tool used by a single agent can just
    be a plain custom tool.
resources:
- label: Model Context Protocol — Introduction
  url: https://modelcontextprotocol.io/introduction
- label: Model Context Protocol — Core concepts (servers, tools, resources)
  url: https://modelcontextprotocol.io/docs/concepts/architecture
- label: Claude Docs — MCP connector
  url: https://platform.claude.com/docs/en/agents-and-tools/mcp-connector
- label: Anthropic — Introducing the Model Context Protocol
  url: https://www.anthropic.com/news/model-context-protocol
---

## From user of MCP to builder of MCP

You already meet MCP every day in Claude Code: that's how it reads your files, runs commands, and talks to your services. This lesson promotes you from *user* to *engineer* — understanding what MCP actually is so you can plug your own agents into tools and data the standard way.

**Model Context Protocol (MCP)** is an open standard for connecting an AI **host** (Claude Code, your agent, an IDE) to **servers** that provide capabilities. The point is reuse: write a GitHub MCP server once, and every MCP-aware host can use it — instead of every application re-implementing its own GitHub integration. If you've ever written a Terraform provider or a Kubernetes operator, the instinct is familiar: a standard interface so many consumers can talk to one capability.

## The three primitives

An MCP server exposes three kinds of thing:

- **Tools** — *actions* the model can invoke. "Create a GitHub issue." "Run this SQL query." These are the same tools from the tool-use loop, just hosted behind a server.
- **Resources** — *data* the model can read into context. A file, a database record, a wiki page. Resources are read, not executed; they hydrate the model's context with relevant content.
- **Prompts** — reusable **prompt templates** the server offers, so a host can present "summarise this PR" as a one-click action with the wording already written.

Tools *do*; resources *provide*; prompts *template*. That three-way split is the whole conceptual model.

## How MCP tools meet the loop you know

Here is the satisfying part: MCP doesn't replace anything you've learned. When a host connects to an MCP server, each MCP tool simply shows up as a tool the model can call. The very same plan-act-observe loop runs — `stop_reason` of `tool_use`, you (or the host) execute the tool, you return a `tool_result`. The only difference is *where the tool runs*: behind the MCP server instead of inline in your code.

```python
# Local MCP server over stdio, used with the tool runner
from anthropic import AsyncAnthropic
from anthropic.lib.tools.mcp import async_mcp_tool
from mcp import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters

client = AsyncAnthropic()
async with stdio_client(StdioServerParameters(command="my-mcp-server")) as (r, w):
    async with ClientSession(r, w) as mcp:
        await mcp.initialize()
        tools = (await mcp.list_tools()).tools
        runner = client.beta.messages.tool_runner(
            model="claude-opus-4-8",
            max_tokens=1024,
            messages=[{"role": "user", "content": "Use the available tools"}],
            tools=[async_mcp_tool(t, mcp) for t in tools],
        )
        async for message in runner:
            print(message)
```

For **remote** servers, Anthropic's API also accepts an `mcp_servers` parameter so Claude connects to a hosted MCP endpoint directly by URL — handy when the server runs as its own service.

## Transports: local and remote

Two shapes you'll meet. **Local (stdio)** servers run as a subprocess on the same machine — Claude Code starts them and talks over standard input and output. Great for filesystem and developer-machine tools. **Remote (URL)** servers run as a network service over HTTP — the right shape for a shared, multi-user integration. The protocol is the same; only the transport differs.

## Where the secrets live

This is the part that should make a security engineer smile. The **credential lives in the server, not in the model**. When an MCP tool calls GitHub, the server holds the token; the model only ever sees the tool's inputs ("create issue titled X") and outputs ("issue #42 created"). A leaked transcript or a prompt-injection attempt can't exfiltrate a secret the model never had. That boundary — the model operates on *results*, the server holds the *keys* — is exactly the secrets-management discipline you already apply in pipelines.

## Custom tool or MCP server?

If a capability is used by exactly one agent and never shared, a plain custom tool (Lesson 2) is the lighter choice. Reach for an MCP server when you want the capability **reused across hosts or agents**, or offered as a standard interface others can plug into. MCP's payoff is reuse and a clean trust boundary, not raw speed.

## Your task

Pick a service you already operate (e.g. your monitoring system or a ticketing tool). On paper, design a tiny MCP server for it: list two **tools** it would expose, one **resource**, and where the API credential would live. Then state, in one sentence, how that server's tools would appear inside the agent loop.
