#!/usr/bin/env bash
# Setup script of the cloud environment (Claude Code on the web) for Xartaxana/Forge-for-QAFactory.
# STAGED COPY: at the move it goes to tools/cloud_setup.sh; its one-line call is pasted into the environment's
# "Setup script" field on claude.ai/code (docs/migration/MIGRATION_PLAN.md, step D6: "Cloud: claude.ai/code -> the
# environment for the forge, Setup script `bash tools/cloud_setup.sh`"). Also safe to run by hand on a fresh Linux/macOS clone.
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

# 5. the GitHub CLI for CI reading (gh run list / view); the token comes from the environment, never from a file
command -v gh >/dev/null 2>&1 || echo "note: gh CLI missing; CI is read in the browser or after installing gh"

echo "cloud setup done: python=$(python --version 2>&1) hooksPath=$(git -C "$ROOT" config core.hooksPath)"
