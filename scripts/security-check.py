#!/usr/bin/env python3
"""Read-only source and workflow checks; never builds, installs or downloads."""
import ast
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
errors = []
python_count = shell_count = 0
for path in ROOT.rglob("*"):
    relative = path.relative_to(ROOT)
    if any(part in {".git", "build", "out", "__pycache__"} for part in relative.parts):
        continue
    if not path.is_file():
        continue
    if path.suffix == ".py" or relative.as_posix() == "scripts/jatayu-admin":
        python_count += 1
        try:
            ast.parse(path.read_text(), filename=str(relative))
        except (SyntaxError, UnicodeError) as error:
            errors.append(str(error))
    elif path.suffix == ".sh" or path.name.endswith(".hook.chroot") or relative.as_posix() in {
        "scripts/postinst", "scripts/jatayu", "scripts/jatayu-webapp",
        "scripts/jatayu-live-installer",
    }:
        shell_count += 1
        result = subprocess.run(["bash", "-n", str(path)], capture_output=True, text=True)
        if result.returncode:
            errors.append(f"{relative}: {result.stderr.strip()}")

# All workflow action references must be immutable. This is intentionally a
# narrow policy check, not a substitute for a complete YAML/Actions validator.
for path in (ROOT / ".github/workflows").glob("*.yml"):
    text = path.read_text()
    for action in re.findall(r"^\s*-?\s*uses:\s*([^\s#]+)", text, re.M):
        if not re.fullmatch(r"[^@]+@[0-9a-f]{40}", action):
            errors.append(f"{path.name}: unpinned action {action}")
    if "pull_request_target:" in text:
        errors.append(f"{path.name}: privileged PR trigger requires separate review")
    if "persist-credentials: false" not in text:
        errors.append(f"{path.name}: checkout credentials must not persist")
    if not re.search(r"^permissions:\n  contents: read\n", text, re.M):
        errors.append(f"{path.name}: expected read-only workflow token")

build = (ROOT / ".github/workflows/build-iso.yml").read_text()
if re.search(r"^  (push|pull_request|schedule|workflow_run):", build, re.M):
    errors.append("Full ISO workflow must remain manual-only")
if "inputs.confirm == 'BUILD'" not in build:
    errors.append("Full ISO workflow must require explicit BUILD confirmation")
if "${{" in build.split("      - name: Build once in Debian 13", 1)[1].split("        run: |", 1)[1].split("      - name:", 1)[0]:
    errors.append("Do not interpolate workflow inputs directly into builder shell")

print(f"Checked {python_count} Python and {shell_count} shell sources; workflow security policy.")
if errors:
    print("\n".join(errors), file=sys.stderr)
    sys.exit(1)
print("Source security checks PASS; no ISO assembly or package installation performed.")
