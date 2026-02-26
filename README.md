# AI Agent

**A small AI coding agent that uses Gemini and function calling to read, write, and run code in a sandboxed directory.**

---

## What is this?

This repo is a **learning project** for building an AI agent. The goal isn’t to ship a product—it’s to understand how an agent works end-to-end: sending a natural-language request to an LLM, having it choose and call tools (list files, read/write files, run Python), and looping until it produces a final answer.

You get a CLI that takes a prompt (e.g. *“list the files in the working directory and summarize `lorem.txt`”*). The agent uses **Google’s Gemini API** with **function calling**: the model decides which tools to call and with what arguments; the app runs those tools, feeds the results back, and repeats until the model responds with text instead of another function call.

---

## What it can do

- **List files and directories** in the sandbox
- **Read file contents**
- **Write or overwrite files**
- **Execute Python files** (with optional arguments)

All of this is limited to a configurable working directory (default: `./calculator`) so the agent can’t touch the rest of your filesystem.

---

## Quick start

1. **Clone and install**

   ```bash
   uv sync
   ```

2. **Set your Gemini API key**

   ```bash
   export GEMINI_API_KEY="your-key-here"
   # or use a .env file with GEMINI_API_KEY=...
   ```

3. **Run the agent**

   ```bash
   uv run python main.py "List files in the working directory and read the first 3 lines of lorem.txt" --verbose
   ```

   Omit `--verbose` for less output.

---

## Project layout (high level)

| Part | Role |
|------|------|
| `main.py` | Entrypoint: CLI, message list, and the agent loop that calls Gemini and handles function calls. |
| `prompts.py` | System prompt that defines the agent’s role and available tools. |
| `call_function.py` | Tool declarations for Gemini + a dispatcher that runs the right function and returns results. |
| `functions/` | Implementations: `get_files_info`, `get_file_content`, `write_file`, `run_python_file`. |
| `config.py` | Model id, client, `WORKING_DIR`, `MAX_ITERS`, etc. |

The loop in `main.py` keeps requesting content from Gemini; when the response includes function calls, the app executes them, appends the results to the conversation, and sends again until the model returns a normal text reply or the iteration limit is hit.

---

## Learning focus

- **Agent loop**: user message → model (with tools) → function calls → execute → feed back → repeat.
- **Tool design**: defining schemas and mapping model choices to real code.
- **Safety and scope**: one working directory, no arbitrary shell access.
- **API usage**: Gemini `generate_content` with `tools` and `system_instruction`.

---

## Requirements

- Python ≥ 3.11  
- A [Gemini API key](https://ai.google.dev/)  
- Dependencies in `pyproject.toml` (e.g. `uv sync` or `pip install -e .`)
