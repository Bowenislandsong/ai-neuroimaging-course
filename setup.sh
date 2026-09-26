#!/usr/bin/env bash
# Install the locked course environment; optionally validate the notebooks.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"

case "${1:-}" in
  ''|--check|--check-all) ;;
  *)
    printf 'Usage: ./setup.sh [--check | --check-all]\n' >&2
    exit 2
    ;;
esac

if ! command -v uv >/dev/null 2>&1; then
  if ! command -v curl >/dev/null 2>&1; then
    printf 'Install curl or uv, then rerun this script.\n' >&2
    exit 1
  fi
  printf 'Installing uv with its official installer...\n'
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH="$HOME/.local/bin:$PATH"
fi

if ! command -v uv >/dev/null 2>&1; then
  printf 'uv was installed but is not on PATH. Add ~/.local/bin to PATH and rerun.\n' >&2
  exit 1
fi

uv sync --locked

case "${1:-}" in
  '')
    printf '\nReady. Open the course with: uv run --locked jupyter lab notebooks\n'
    printf 'Validate the offline lessons with: ./setup.sh --check\n'
    ;;
  --check)
    uv run --locked python scripts/check_repository.py
    uv run --locked python scripts/validate_notebooks.py
    ;;
  --check-all)
    uv run --locked python scripts/check_repository.py
    uv run --locked python scripts/validate_notebooks.py --include-network
    ;;
esac
