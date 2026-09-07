#!/usr/bin/env bash
set -euo pipefail

version_file="VERSION"
current=$(tr -d '[:space:]' < "$version_file")
if [[ ! "$current" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  printf 'VERSION must contain a SemVer value, found: %s\n' "$current" >&2
  exit 1
fi

branch=$(git branch --show-current)
[[ "$branch" == "main" ]] || { printf 'Releases must be cut from main.\n' >&2; exit 1; }
[[ -z "$(git status --porcelain)" ]] || { printf 'Working tree must be clean before releasing.\n' >&2; exit 1; }

latest_tag=$(git describe --tags --match 'v[0-9]*' --abbrev=0 2>/dev/null || true)
range="$latest_tag..HEAD"
[[ -n "$latest_tag" ]] || range="HEAD"
subjects=$(git log --format='%s%n%b' "$range")

major=0
minor=0
patch=0
if printf '%s\n' "$subjects" | grep -Eq 'BREAKING CHANGE|^[a-z]+(\([^)]*\))?!:'; then major=1
elif printf '%s\n' "$subjects" | grep -Eq '^feat(\([^)]*\))?:'; then minor=1
elif printf '%s\n' "$subjects" | grep -Eq '^(fix|perf|refactor)(\([^)]*\))?:'; then patch=1
fi

if (( !major && !minor && !patch )); then
  printf 'No release-worthy Conventional Commits found since %s.\n' "${latest_tag:-the beginning}" >&2
  exit 1
fi

IFS=. read -r major_version minor_version patch_version <<< "$current"
if (( major )); then
  ((major_version += 1)); minor_version=0; patch_version=0
elif (( minor )); then
  ((minor_version += 1)); patch_version=0
else
  ((patch_version += 1))
fi
next="$major_version.$minor_version.$patch_version"

printf '%s\n' "$next" > "$version_file"
git add "$version_file"
git commit -m "chore(release): v$next"
git tag -a "v$next" -m "Release v$next"
printf 'Created release v%s\n' "$next"