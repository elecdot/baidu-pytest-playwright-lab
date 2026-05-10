#!/usr/bin/env bash

# Codex's sandbox workspace-write only allows certain paths to write;
# Even if uv is just running, it may still need to write to/lock the cache.
# This includes the uv cache directory in the workspace-safe paths.
export UV_CACHE_DIR="${UV_CACHE_DIR:-.cache/uv}"
exec "$@"
