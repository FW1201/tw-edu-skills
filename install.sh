#!/usr/bin/env bash
set -euo pipefail
REPO_DIR="$(cd -- "$(dirname -- "$0")" && pwd)"
exec python3 "$REPO_DIR/scripts/install.py" "$@"
