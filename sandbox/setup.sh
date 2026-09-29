#!/usr/bin/env bash
# Set up the Panic Pantry teaching sandbox for the matched comparison:
# - make sandbox/panic-pantry its own git repo (nested repo is intentional)
# - commit the starter state and tag it "starter"
# - create two matched worktrees: worktrees/single-agent and worktrees/orchestrated
# Idempotent: re-running recreates the worktrees from the starter tag.
# WARNING: re-running discards any learner work inside the worktrees.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PANTRY="$SCRIPT_DIR/panic-pantry"
WORKTREES="$SCRIPT_DIR/worktrees"

cd "$PANTRY"

if [ ! -d .git ]; then
  git init -b main
  echo "[setup] initialized git repo in $PANTRY"
fi

# Local identity so commits work on a fresh classroom VM.
git config user.name >/dev/null 2>&1 || git config user.name "Panic Pantry Instructor"
git config user.email >/dev/null 2>&1 || git config user.email "instructor@panic-pantry.local"

bash scripts/reset.sh >/dev/null
echo "[setup] sandbox reset to starter state"

git add -A
if ! git rev-parse -q --verify HEAD >/dev/null 2>&1; then
  git commit -m "starter"
  echo "[setup] created starter commit"
elif ! git diff --cached --quiet; then
  git commit -m "starter"
  echo "[setup] committed starter updates"
else
  echo "[setup] starter commit already up to date"
fi
git tag -f starter >/dev/null
echo "[setup] tag 'starter' -> $(git rev-parse --short HEAD)"

mkdir -p "$WORKTREES"
for name in single-agent orchestrated; do
  path="$WORKTREES/$name"
  git worktree remove --force "$path" >/dev/null 2>&1 || true
  rm -rf "$path"
  git worktree prune
  git branch -D "$name" >/dev/null 2>&1 || true
  git worktree add -b "$name" "$path" starter >/dev/null
  (cd "$path" && bash scripts/reset.sh >/dev/null)
  echo "[setup] worktree '$name' -> $path (branch $name @ $(git -C "$path" rev-parse --short HEAD))"
done

echo "[setup] worktrees:"
git worktree list
echo "[setup] done"
