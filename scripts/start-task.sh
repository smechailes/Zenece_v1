#!/usr/bin/env bash
set -euo pipefail

usage() {
  printf 'Usage: %s <feature|templating|fix|docs|chore|refactor> <short-description>\n' "$0"
  exit 1
}

[[ $# -eq 2 ]] || usage

type="$1"
description="$2"
case "$type" in
  feature|templating|fix|docs|chore|refactor) ;;
  *) usage ;;
esac

slug=$(printf '%s' "$description" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9]+/-/g; s/^-+//; s/-+$//')
[[ -n "$slug" ]] || { printf 'Description must contain letters or numbers.\n' >&2; exit 1; }

if [[ -n "$(git status --porcelain)" ]]; then
  printf 'Working tree is not clean. Commit or stash changes before starting a task.\n' >&2
  exit 1
fi

current_branch=$(git branch --show-current)
if [[ "$current_branch" != "main" ]]; then
  printf 'Switch to main before starting a new task (currently on %s).\n' "$current_branch" >&2
  exit 1
fi

git switch -c "$type/$slug"
printf 'Created branch %s/%s\n' "$type" "$slug"