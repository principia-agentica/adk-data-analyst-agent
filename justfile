# --- Variables ---
# Define the lock file name so we can reuse it
REQUIREMENTS_FILE := "requirements.txt"
TOOLBOX_VERSION := "0.16.0"

# Default command to run if no other is specified
default: lint format

# Lint the code using ruffa
lint:
    @just sync
    @ruff check .

# Format the code using ruff
format:
    @just sync
    @ruff format .

# Set up the development environment from scratch
setup:
    @echo "Setting up virtual environment..."
    @uv venv
    @echo "✅ Virtual environment created."
    @just lock
    @just sync
    @echo "✅ Environment setup complete. Run 'source .venv/bin/activate' to activate."

# Lock the project dependencies into a requirements.txt file
lock:
    @echo "Locking dependencies from pyproject.toml -> {{REQUIREMENTS_FILE}}..."
    @uv pip compile pyproject.toml -o {{REQUIREMENTS_FILE}}
    @echo "✅ Dependencies locked."

# Sync the virtual environment with the lock file
sync:
    @echo "Syncing environment with {{REQUIREMENTS_FILE}}..."
    @uv pip sync {{REQUIREMENTS_FILE}}
    @echo "✅ Environment synced."

# Fetch the sample data needed for the project
data:
    @just sync
    @uv run data_analyst_agent/setup_db.py
    @mv products.db data_analyst_agent
    @echo "✅ Database setup complete."

# Create the local .env file from the example template
env:
    @if [ ! -f .env ]; then \
        echo "Creating .env file from .env.example..."; \
        cp .env.example .env; \
        echo "✅ .env file created. Please fill in your secrets."; \
    else \
        echo ".env file already exists. Skipping."; \
    fi

get_toolbox:
    @download_url=""; \
    if [ "$(uname)" = "Darwin" ]; then \
        if [ "$(uname -m)" = "arm64" ]; then \
            echo "macOS (Apple Silicon) detected" \
            download_url="https://storage.googleapis.com/genai-toolbox/v{{TOOLBOX_VERSION}}/darwin/arm64/toolbox"; \
        else \
            echo "macOS (Apple Intel) detected" \
            download_url="https://storage.googleapis.com/genai-toolbox/v{{TOOLBOX_VERSION}}/darwin/amd64/toolbox"; \
        fi \
    else \
        echo "Linux detected" \
        download_url="https://storage.googleapis.com/genai-toolbox/v{{TOOLBOX_VERSION}}/linux/amd64/toolbox"; \
    fi; \
    if [ -n "$download_url" ]; then \
        echo "Downloading Toolbox from $download_url"; \
        curl -O "$download_url"; \
        chmod +x toolbox; \
        mv toolbox data_analyst_agent; \
    else \
        echo "No download URL determined for this platform.\n For **Windows**, download the executable from: https://storage.googleapis.com/genai-toolbox/v{{TOOLBOX_VERSION}}/windows/amd64/toolbox.exe"; \
    fi


toolbox:
    @data_analyst_agent/toolbox --tools-file "data_analyst_agent/tools.yaml" --port 7000

toolbox-ui:
    @data_analyst_agent/toolbox --ui --tools-file "data_analyst_agent/tools.yaml"

web:
    @adk web
