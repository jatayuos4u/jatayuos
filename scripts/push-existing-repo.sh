#!/usr/bin/env bash
# Run on the owner's computer after authenticating GitHub CLI.
# Refuses public repositories while development licences remain unresolved.
set -euo pipefail
source_dir=$(cd "$(dirname "$0")/.." && pwd)
repo='jatayuos4u/jatayuos'

for bin in gh git python3 tar; do
  if ! command -v "$bin" >/dev/null; then
    echo "Missing $bin; install it before publishing." >&2
    exit 2
  fi
done
if ! gh auth status >/dev/null 2>&1; then
  echo 'Sign in to your own account using: gh auth login' >&2
  exit 2
fi
account=$(gh api user --jq .login)
if [[ ${account,,} != jatayuos4u ]]; then
  echo "Signed in as $account; expected jatayuos4u. Nothing was changed." >&2
  exit 2
fi
if [[ $(gh repo view "$repo" --json isPrivate --jq .isPrivate) != true ]]; then
  echo "The repository is public. Change $repo to PRIVATE in Settings first; no development source was pushed." >&2
  exit 2
fi
python3 "$source_dir/scripts/preflight.py"
gh auth setup-git
tmp_dir=$(mktemp -d)
trap 'rm -rf "$tmp_dir"' EXIT
gh repo clone "$repo" "$tmp_dir/repo"
cd "$tmp_dir/repo"
files=$(git ls-tree -r --name-only HEAD)
if [[ $files != 'README.md' ]]; then
  echo 'Repository has files beyond its starter README. Review and merge them before pushing.' >&2
  exit 2
fi
tar -C "$source_dir" \
  --exclude='./.git' --exclude='./build' --exclude='./out' \
  --exclude='./__pycache__' --exclude='./JatayuOS-Development-Build-Kit.zip' \
  -cf - . | tar -xf - -C "$tmp_dir/repo"
git add .
if git diff --cached --quiet; then
  echo 'The repository already matches this source; no push was needed.'
  exit 0
fi
git -c user.name='Anup Yadav' -c user.email='jatayuos4u@gmail.com' \
  commit -m 'Add JatayuOS development build kit'
git push origin HEAD:main
echo "Pushed development source to private $repo. No ISO build was dispatched."
