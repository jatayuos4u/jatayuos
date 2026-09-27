#!/usr/bin/env bash
# Creates a private source repository. Does not dispatch an ISO build.
set -euo pipefail
cd "$(dirname "$0")/.."

repo='jatayuos4u/jatayuos'
if ! command -v gh >/dev/null; then
  echo 'Install GitHub CLI (gh): https://cli.github.com/' >&2
  exit 2
fi
if ! command -v git >/dev/null; then
  echo 'Install Git before running this script.' >&2
  exit 2
fi
if ! gh auth status >/dev/null 2>&1; then
  echo 'Sign in with: gh auth login' >&2
  exit 2
fi
account=$(gh api user --jq .login)
if [[ ${account,,} != jatayuos4u ]]; then
  echo "Signed in as $account, but this script targets jatayuos4u. Switch account or edit and review the repo variable." >&2
  exit 2
fi
if gh repo view "$repo" >/dev/null 2>&1; then
  echo "Repository $repo already exists. Nothing was changed; inspect it before pushing." >&2
  exit 2
fi
if [[ -d .git ]]; then
  echo 'This folder already has Git history. Review it before publishing; nothing was changed.' >&2
  exit 2
fi
if [[ ! -f .github/workflows/build-iso.yml ]]; then
  echo 'Missing manual-only ISO workflow. Extract the whole kit, including hidden .github.' >&2
  exit 2
fi
python3 scripts/preflight.py
git init -b main
git add .
git -c user.name='Anup Yadav' -c user.email='jatayuos4u@gmail.com' commit -m 'Add JatayuOS development build kit'
gh repo create "$repo" --private --description 'JatayuOS Debian 13 development build source' --source . --remote origin --push
echo "Created private repository: https://github.com/$repo"
echo 'No ISO workflow was dispatched. Run it manually only when ready to spend Actions minutes.'
