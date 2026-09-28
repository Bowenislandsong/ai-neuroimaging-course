#!/usr/bin/env bash
# Step 0 + Course Setup for macOS (Apple Silicon MacBook Pro); also supports headless CI checks.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"

case "${1:-}" in
  ''|--setup-ai|--build-site|--check|--check-all) ;;
  *)
    printf 'Usage: ./setup.sh [--setup-ai | --build-site | --check | --check-all]\n' >&2
    exit 2
    ;;
esac

export PATH="/opt/homebrew/bin:/usr/local/bin:$HOME/.local/bin:$PATH"

OS_NAME="$(uname -s 2>/dev/null || echo Unknown)"
ARCH_NAME="$(uname -m 2>/dev/null || echo Unknown)"
MEM_GB=16
if [ "$OS_NAME" = "Darwin" ]; then
  if ! xcode-select -p >/dev/null 2>&1; then
    printf 'Note: Apple Command Line Tools not detected. Run: xcode-select --install\n'
    printf '      Official guide: https://developer.apple.com/documentation/xcode/installing-the-command-line-tools\n'
  fi
  if command -v sysctl >/dev/null 2>&1; then
    MEM_BYTES="$(sysctl -n hw.memsize 2>/dev/null || echo 17179869184)"
    MEM_GB="$(( MEM_BYTES / 1073741824 ))"
  fi
fi

# Select recommended Qwen (coding/tool agent) and Gemma 4 (scientific audit/reasoning) tags for MacBook Pro unified memory.
if [ "$MEM_GB" -ge 32 ]; then
  REC_QWEN="qwen3.6:27b"
  REC_GEMMA="gemma4:26b"
else
  REC_QWEN="qwen3.5:9b"
  REC_GEMMA="gemma4:e4b"
fi

if ! command -v uv >/dev/null 2>&1; then
  if ! command -v curl >/dev/null 2>&1; then
    printf 'Install curl or uv (on macOS: brew install uv), then rerun this script.\n' >&2
    exit 1
  fi
  printf 'Installing uv with its official macOS/Unix installer...\n'
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH="$HOME/.local/bin:$PATH"
fi

if ! command -v uv >/dev/null 2>&1; then
  printf 'uv was installed but is not on PATH. Add ~/.local/bin to PATH (in ~/.zshrc on macOS) and rerun.\n' >&2
  exit 1
fi

uv sync --frozen

setup_macos_agentic_stack() {
  printf '\n=== Step 0: macOS (MacBook Pro) Agentic Setup (Goose + Ollama with Qwen & Gemma) ===\n'
  printf 'Detected platform: %s (%s) | Unified Memory: ~%s GB\n' "$OS_NAME" "$ARCH_NAME" "$MEM_GB"
  printf 'Minimal Apple Developer Prerequisites:\n'
  printf '  - Apple Command Line Tools: xcode-select --install (https://developer.apple.com/documentation/xcode/installing-the-command-line-tools)\n'
  printf '  - Apple Metal & Accelerate: Built into macOS (https://developer.apple.com/metal/)\n'
  printf 'Recommended MacBook Pro models:\n'
  printf '  - Primary Agentic Coder (Qwen):     %s\n' "$REC_QWEN"
  printf '  - Scientific Auditor (Gemma 4):     %s\n' "$REC_GEMMA"

  if ! command -v ollama >/dev/null 2>&1; then
    if [ "$OS_NAME" = "Darwin" ] && command -v brew >/dev/null 2>&1; then
      printf 'Installing Ollama via Homebrew...\n'
      brew install --cask ollama || printf 'Please install Ollama from https://ollama.com/download/mac\n'
    else
      printf 'Ollama not found. On macOS, run: brew install --cask ollama (or download from https://ollama.com/download/mac)\n'
    fi
  fi

  if command -v ollama >/dev/null 2>&1; then
    printf 'Pulling latest Qwen (%s) and Gemma (%s) models for your MacBook Pro...\n' "$REC_QWEN" "$REC_GEMMA"
    ollama pull "$REC_QWEN"
    ollama pull "$REC_GEMMA"
  fi

  if ! command -v goose >/dev/null 2>&1; then
    printf 'Installing Goose CLI for macOS...\n'
    curl -fsSL https://github.com/aaif-goose/goose/releases/download/stable/download_cli.sh | bash
    export PATH="$HOME/.local/bin:$PATH"
  fi

  printf '\nStep 0 complete! Configure Goose to use Ollama:\n'
  printf '  1. Run: goose configure   (Choose Provider: Ollama -> Host: http://localhost:11434 -> Model: %s)\n' "$REC_QWEN"
  printf '  2. Start Goose in this repo: goose session\n'
  printf '  3. Launch JupyterLab:        uv run --frozen jupyter lab notebooks\n'
}

case "${1:-}" in
  '')
    printf '\n=== macOS (MacBook Pro) Course Environment Ready ===\n'
    if [ "$OS_NAME" = "Darwin" ]; then
      printf 'Detected macOS (%s, ~%s GB unified memory).\n' "$ARCH_NAME" "$MEM_GB"
    fi
    printf 'Step 0 (Agentic AI Setup — Goose + Ollama with Qwen & Gemma on MacBook Pro):\n'
    printf '  Minimal Apple Dev Tools:      xcode-select --install\n'
    printf '  Run automated AI setup:       ./setup.sh --setup-ai\n'
    printf '  Or manually pull:             ollama pull %s && ollama pull %s\n' "$REC_QWEN" "$REC_GEMMA"
    printf '  See full Step 0 guide:        curriculum/SETUP.md\n\n'
    printf 'Open the course in JupyterLab:  uv run --frozen jupyter lab notebooks\n'
    printf 'Build course website locally:   ./setup.sh --build-site\n'
    printf 'Validate offline lessons:       ./setup.sh --check\n'
    ;;
  --setup-ai)
    setup_macos_agentic_stack
    ;;
  --build-site)
    uv run --frozen python scripts/build_website.py --output build/site
    ;;
  --check)
    uv run --frozen python scripts/check_repository.py
    uv run --frozen python scripts/validate_notebooks.py
    ;;
  --check-all)
    uv run --frozen python scripts/check_repository.py
    uv run --frozen python scripts/validate_notebooks.py --include-network
    ;;
esac
