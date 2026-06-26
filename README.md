# MCP Sampling Demo

A minimal demo of **MCP sampling** — a pattern where the MCP server delegates LLM calls back to the client instead of calling the Anthropic API directly. Also demonstrates **MCP logging and progress notifications** for real-time feedback during long-running tool operations.

## Architecture

```
client.py  →  (stdio)  →  server.py
   ↑                           |
   |   sampling_callback       | ctx.session.create_message(...)
   └───────────────────────────┘
         (back to client via MCP)
              ↓
        Anthropic API
```

- **`server.py`** — MCP server built with `FastMCP`. Exposes a `summarize` tool that uses `ctx.session.create_message(...)` to delegate the LLM call back to the client. Emits log messages and progress updates at 20%, 50%, and 100% during execution.
- **`client.py`** — MCP client that launches the server as a subprocess over stdio. Registers a `sampling_callback` to fulfill LLM requests via the Anthropic API, a `logging_callback` to print server log messages, and a `progress_callback` to display progress updates.

## Logging & Progress Notifications

The `summarize` tool emits three progress checkpoints:

| Stage | Progress | Log message | Delay |
|-------|----------|-------------|-------|
| Start | 20% | Starting summarization... | 2s |
| LLM request | 50% | Sending request to LLM via sampling... | 1s |
| Done | 100% | Summarization complete. | 3s |

Sample output:

```
[Server Log] Starting summarization...
[Progress] 20.0/100.0 (20.0%)
[Server Log] Sending request to LLM via sampling...
[Progress] 50.0/100.0 (50.0%)
[Server Log] Summarization complete.
[Progress] 100.0/100.0 (100.0%)
```

## Prerequisites

- Python 3.13 (Python 3.14+ is not supported due to a `pydantic-core` build incompatibility)
- [uv](https://docs.astral.sh/uv/) package manager
- A valid Anthropic API key

## Setup

Create a `.env` file in the project root:

```bash
ANTHROPIC_API_KEY=your_key_here
```

Pin the project to Python 3.13 and install dependencies:

```bash
echo "3.13" > .python-version
uv sync
```

## Running

```bash
uv run client.py
```
