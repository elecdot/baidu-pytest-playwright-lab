set shell := ["bash", "-c"]

### Human/default

ruff:
    uv run ruff check .

test:
    uv run pytest

### Agent/workspace-safe
### Uses workspace-safe cache (`.cache/uv`) to comply with sandbox restrictions.
### See `./scripts/agent-env.sh` for details.

agent-ruff:
    ./scripts/agent-env.sh uv run ruff check .

agent-test:
    ./scripts/agent-env.sh uv run pytest
