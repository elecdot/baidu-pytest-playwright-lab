set shell := ["bash", "-c"]

### Human/default

ruff:
    uv run ruff check .

format:
    uv run ruff format .

test:
    uv run pytest

test-headed:
    uv run pytest --headed

failure-demo:
    uv run python scripts/failure_demo_generator.py

### Agent/workspace-safe
### Uses workspace-safe cache (`.cache/uv`) to comply with sandbox restrictions.
### See `./scripts/agent-env.sh` for details.

agent-ruff:
    ./scripts/agent-env.sh uv run ruff check .

agent-format:
    ./scripts/agent-env.sh uv run ruff format .

agent-test:
    ./scripts/agent-env.sh uv run pytest

agent-failure-demo:
    ./scripts/agent-env.sh uv run python scripts/failure_demo_generator.py
