# ADK Data Analyst Agent

A small demo project for the AI Study Group showing how to build a data-analyst-style agent that can answer questions about a local SQLite products database using the Google ADK agent framework and a Toolbox tool server.

## Overview
This repository contains:
- A simple SQLite database with synthetic product data.
- A Toolbox toolset (`tools.yaml`) exposing read-only SQL tools (list categories, query by category, sort by price, etc.).
- A minimal ADK `Agent` definition that loads those tools and can be used to power a web UI (`adk web`) or programmatic interactions.

The flow is:
1) Create/populate `products.db`.
2) Run the Toolbox server so the tools are available over HTTP.
3) Start the ADK web UI or otherwise run the agent, which will call the tools to answer questions.


## Tech Stack
- Language: Python (requires 3.11+)
- Agent framework: `google-adk` (Gemini-based)
- Tooling:
  - `toolbox-core` + standalone Toolbox server binary (HTTP server providing tools from `tools.yaml`)
  - Task runner: `just` (optional, but recommended)
  - Package/dependency management: `uv` (with `pyproject.toml`, `requirements.txt`, and `uv.lock`)
- Database: SQLite (local file)


## Requirements
- Python 3.11+
- uv (https://github.com/astral-sh/uv)
- just (https://github.com/casey/just)
- curl (to download the Toolbox binary via the provided recipe)
- SQLite installed on your system (optional; Python’s sqlite3 is used to create the DB)

Optional but likely needed depending on your environment:
- A modern browser (for the `adk web` UI)


## Quick Start
The project includes a `justfile` with tasks to set up and run everything. If you don’t have `just`, you can read the underlying commands in the "What the recipes do" section below.

0) Set up your secrets and environment variables:

```bash
# One-time setup
just env
```

Then go and edit your `.env` file with your Gemini API Key. See the "Environment Variables" section below for more details.

1) Create and activate a virtual environment, lock/sync dependencies:

```bash
# One-time setup
just setup

# Activate the venv in your current shell (macOS/Linux bash/zsh)
source .venv/bin/activate
```

2) Download the Toolbox binary appropriate for your OS and start it:

```bash
# Download toolbox into data_analyst_agent/toolbox (macOS/Linux)
just get_toolbox

# Start the Toolbox server on port 7000
just toolbox
# (leave this terminal running)
```

3) Create and populate the sample database:

```bash
# In a new terminal (venv activated)
just data
```

4) Start the ADK web UI:

```bash
# In another terminal (venv activated)
just web
```

At this point you should have:
- Toolbox server running on http://127.0.0.1:7000
- ADK web UI started via `adk web` typically in http://127.0.0.1:8000

How to actually use the agent within `adk web` depends on your ADK setup and version. See the TODOs below.


## Environment Variables
The agent file (`data_analyst_agent/agent.py`) calls `load_dotenv('../.env')`, which means it expects a `.env` file at the repository root. The repository includes a convenience recipe to create one from a template if present:

```bash
just env
```

- `GOOGLE_GENAI_USE_VERTEXAI` Leave this as "0" unless you're using Vertex AI from GCP as model provider.
- `GOOGLE_API_KEY` Your Gemini API Key. You can get one free from Google AI Studio. 
- `AGENT_WORKSPACE_PATH` The path to the root of the repository.

## Scripts and Commands
These are defined in the `justfile`:

- `just setup`
  - Creates a virtual environment with `uv venv`
  - Locks dependencies from `pyproject.toml` into `requirements.txt` via `uv pip compile`
  - Syncs the environment with `uv pip sync`

- `just lock`
  - Regenerates `requirements.txt` from `pyproject.toml`

- `just sync`
  - Installs/syncs dependencies from `requirements.txt` into the active venv

- `just lint`
  - Runs `ruff check .`

- `just format`
  - Runs `ruff format .`

- `just data`
  - Runs `data_analyst_agent/setup_db.py` to create `products.db`
  - Moves the generated `products.db` into `data_analyst_agent/`

- `just get_toolbox`
  - Downloads the Toolbox binary for your platform into `data_analyst_agent/toolbox`

- `just toolbox`
  - Runs the Toolbox server:
    ```
    data_analyst_agent/toolbox --tools-file "data_analyst_agent/tools.yaml" --port 7000
    ```

- `just web`
  - Starts the ADK web UI:
    ```
    adk web
    ```

Note: `install` recipe exists but uses `uv pip install -r pyproject.toml`. That invocation is unusual; `uv pip install` typically expects a requirements file or a package spec. Prefer using `setup`/`sync`.


## Project Structure
```
.
├── README.md
├── adk-data-analyst-agent.iml
├── data_analyst_agent
│   ├── __init__.py
│   ├── agent.py
│   ├── products.db           # created by `just data` (then moved here)
│   ├── setup_db.py           # creates and populates the SQLite DB
│   ├── toolbox               # toolbox binary (downloaded by `just get_toolbox`)
│   └── tools.yaml            # toolbox definitions and toolset
├── justfile                  # task runner recipes
├── pyproject.toml            # project metadata and dependencies (primary source)
├── requirements.txt          # compiled lock from pyproject (do not edit by hand)
└── uv.lock                   # uv lockfile
```


## Running Programmatically (optional)
The module `data_analyst_agent/agent.py` defines a `root_agent` configured with the `products-toolset` from `tools.yaml`. If you want to experiment in Python:

```python
# Example (may vary based on google-adk API surface)
from data_analyst_agent.agent import root_agent

# TODO: replace with the actual invocation method for your google-adk Agent
# e.g., response = root_agent.run("What are the products in Electronics?")
# print(response)
```

Since the public API of `google-adk` may evolve, consult its documentation for the correct invocation method. The provided web UI (`adk web`) is the recommended starting point for interactive exploration.


## Tools Definition
`data_analyst_agent/tools.yaml` defines:
- A SQLite source at `data_analyst_agent/products.db`.
- Toolset `products-toolset` with tools:
  - `get-categories`
  - `search-products-by-category` (param: `category`)
  - `get-products-sorted-by-price`
  - `get-low-stock-products`
  - `get-average-price-by-category` (param: `category`)

Make sure the Toolbox server is started pointing to this file:
```
data_analyst_agent/toolbox --tools-file "data_analyst_agent/tools.yaml" --port 7000
```

## Testing
No automated tests are currently included in this repository.

TODOs:
- Add unit tests for database setup and tool queries.
- Add integration tests that run the toolbox server and exercise the agent’s tool calls.


## Linting and Formatting
- Lint: `ruff check .`
- Format: `ruff format .`

Both are also available via `just lint` and `just format`.

## License
MIT
