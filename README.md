# INSTALLATION

pip install -U -r requirements.txt

# DEBUGGER ORQUESTATION

We are using langgraph-cli, so:

langgraph dev

# UV usage (scaling improvement and venv management)

We use for 10-100x than pip (improving production version)
https://docs.astral.sh/uv/

uv init
uv add requirements.txt (may include --dev)

# Laboratory environtment

Jupyter notebook (ipykernel)

# Run with uv

uv run langgraph dev

# Refresh changes in directories

uv pip install -e .