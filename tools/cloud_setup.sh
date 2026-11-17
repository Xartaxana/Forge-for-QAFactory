#!/usr/bin/env bash
# Setup script of the cloud environment (Claude Code on the web) for Xartaxana/Forge-for-QAFactory.
# Paste this one line into the environment's "Setup script" field on claude.ai/code:  bash tools/cloud_setup.sh
# Also safe to run by hand on a fresh Linux/macOS clone.
# Idempotent: a second run changes nothing.
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"

# 1. Python deps the forge tools and hooks import (same list as forge-check in CI)
python3 -m pip install -q --user pytest pyflakes==3.2.0 pyyaml openpyxl coverage==7.16.2 || \
  python3 -m pip install -q --break-system-packages pytest pyflakes==3.2.0 pyyaml openpyxl coverage==7.16.2

# 2. `python` must exist: .claude/settings.json hooks call `python tools/...`
if ! command -v python >/dev/null 2>&1; then
  mkdir -p "$HOME/.local/bin"
  ln -sf "$(command -v python3)" "$HOME/.local/bin/python"
  export PATH="$HOME/.local/bin:$PATH"
  PATH_LINE='export PATH="$HOME/.local/bin:$PATH"'
  grep -qxF "$PATH_LINE" "$HOME/.bashrc" 2>/dev/null || echo "$PATH_LINE" >> "$HOME/.bashrc"
fi

# 3. the git gates (a fresh clone has no core.hooksPath)
git -C "$ROOT" config core.hooksPath .githooks

# 4. the per-developer config (untracked by design): created from the committed example when absent
if [ ! -f "$ROOT/tools/dev.config.yaml" ] && [ -f "$ROOT/tools/dev.config.example.yaml" ]; then
  cp "$ROOT/tools/dev.config.example.yaml" "$ROOT/tools/dev.config.yaml"
  echo "tools/dev.config.yaml created from the example (dev slug: see the file)"
fi

# 5. the token for CI reading: the NAME of the variable comes from tools/dev.config.yaml (github_token_env, default
#    GITHUB_TOKEN); only set/unset is printed, never the value
TOKEN_ENV=GITHUB_TOKEN
if [ -f "$ROOT/tools/dev.config.yaml" ]; then
  while IFS= read -r line || [ -n "$line" ]; do
    case "$line" in
      github_token_env:*)
        v="${line#github_token_env:}"; v="${v%%#*}"; v="${v//[\"\' $'\t'$'\r']/}"
        if [[ "$v" =~ ^[A-Za-z_][A-Za-z0-9_]*$ ]]; then TOKEN_ENV="$v"; fi
        break ;;
    esac
  done < "$ROOT/tools/dev.config.yaml"
fi
if [ -n "${!TOKEN_ENV:-}" ]; then echo "token env $TOKEN_ENV: set"; else echo "token env $TOKEN_ENV: unset"; fi

# 6. the cloud clone is shallow (measured t-1281); history-reading tools need the full one. A failure is a note only
if [ "$(git -C "$ROOT" rev-parse --is-shallow-repository 2>/dev/null || true)" = "true" ]; then
  git -C "$ROOT" fetch -q --unshallow >/dev/null 2>&1 || echo "note: git fetch --unshallow failed; the clone stays shallow"
fi

# 7. journal timestamps are naive local times; the cloud VM is UTC unless TZ is set
if [ -z "${TZ:-}" ]; then
  echo "note: TZ is unset; journal timestamps are naive local times, so set TZ in the environment variables (the owner machine is Europe/Paris)"
fi

echo "cloud setup done: python=$(python --version 2>&1) hooksPath=$(git -C "$ROOT" config core.hooksPath)"
