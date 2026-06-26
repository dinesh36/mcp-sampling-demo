# MCP Logging and Progress Demo

## Prerequisites

- Python 3.13 (Python 3.14+ is not supported due to a `pydantic-core` build incompatibility)
- [uv](https://docs.astral.sh/uv/) package manager
- A valid Anthropic API key

## Setup

Create a `.env` file in the project root with your Anthropic API key:

```bash
ANTHROPIC_API_KEY=your_key_here
```

Pin the project to Python 3.13 and install dependencies:

```bash
echo "3.13" > .python-version
uv sync
```

## Running the Project

Run the MCP client:

```bash
uv run client.py
```
