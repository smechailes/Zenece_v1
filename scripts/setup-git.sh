#!/usr/bin/env bash
set -euo pipefail

git config core.hooksPath githooks
chmod +x scripts/*.sh githooks/commit-msg
printf 'Git hooks enabled from githooks/\n'