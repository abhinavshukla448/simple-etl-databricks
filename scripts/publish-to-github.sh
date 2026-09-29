#!/usr/bin/env bash
set -euo pipefail

REPO_NAME="${1:-simple-etl-databricks}"
VISIBILITY="${2:-public}"

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if ! command -v gh >/dev/null 2>&1; then
  echo "Install GitHub CLI: brew install gh"
  exit 1
fi

gh auth status

if git remote get-url origin >/dev/null 2>&1; then
  echo "Remote origin already exists:"
  git remote -v
else
  gh repo create "$REPO_NAME" \
    --"$VISIBILITY" \
    --source=. \
    --remote=origin \
    --description "Simple ETL on Databricks Community/Free Edition with GitHub Actions"
fi

git push -u origin main

echo ""
echo "Next: add GitHub Actions secrets in the repo (Settings → Secrets → Actions):"
echo "  DATABRICKS_HOST"
echo "  DATABRICKS_TOKEN"
echo ""
echo "Optional demo PR (if branch exists locally):"
echo "  git push -u origin chore/github-secrets-checklist"
echo "  gh pr create --base main --head chore/github-secrets-checklist --title 'Add GitHub secrets checklist'"
