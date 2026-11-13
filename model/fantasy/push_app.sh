#!/bin/bash
# Copies the built app into the GitHub repo and pushes it (GitHub Pages republishes automatically).
set -e
cd /home/claude/draft-room-27
git fetch -q origin main && git reset -q --soft origin/main
cp /home/claude/app/* .
bash /home/claude/fantasy/sync_model.sh
git add -A
git diff --cached --quiet && { echo "app unchanged"; exit 0; }
git commit -qm "${1:-Update rankings}

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01UQnpVWKkzFbLXmGvV2xQFk"
git push -q origin HEAD:main && echo "app pushed"
