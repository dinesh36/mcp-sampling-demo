# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Setup & Running

Requires `ANTHROPIC_API_KEY` set as an environment variable.

```bash
uv sync          # install dependencies
uv run client.py # run the demo
```

## Architecture

This project demonstrates **MCP sampling** — a pattern where the MCP server delegates LLM calls back to the client rather than calling Claude directly.

**`server.py`** — MCP server built with `FastMCP`. Exposes a single `summarize` tool that calls `ctx.session.create_message(...)` to request a sampling operation from the connected client. The server never touches the Anthropic API directly.

**`client.py`** — MCP client that launches the server as a subprocess over stdio. It registers a `sampling_callback` which receives the server's sampling requests and fulfills them by calling the Anthropic API (`claude-sonnet-4-0`). After connecting, it calls the `summarize` tool to trigger the full round-trip.

**Data flow:**
```
client.py  →  (stdio)  →  server.py
   ↑                           |
   |   sampling_callback       | ctx.session.create_message(...)
   └───────────────────────────┘
         (back to client via MCP)
              ↓
        Anthropic API
```

The model used for sampling is hardcoded in `client.py` at the `model` variable (line 14).
