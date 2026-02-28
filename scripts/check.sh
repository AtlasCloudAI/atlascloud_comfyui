#!/usr/bin/env bash
# Run before push/PR: lint + tests. Same as CI (build-pipeline.yml).
# Usage: ./scripts/check.sh   or   bash scripts/check.sh

set -e
cd "$(dirname "$0")/.."

echo "==> Installing dev dependencies..."
pip install -q -e ".[dev]"

echo "==> Running ruff (lint)..."
ruff check .

echo "==> Running pytest..."
pytest tests/ -v

echo "==> Check passed. Safe to push."
