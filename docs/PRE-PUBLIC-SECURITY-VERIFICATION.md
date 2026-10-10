# Pre-publication security verification — 10 October 2026

## Scope and status

This repository is still private. Do **not** change visibility based solely on keyword searches or this document.

The final Build #38 GitHub Actions job 112685755564 (run 37589010270) was retrievable. A bounded preliminary review of its 4.36-million-character log found no matches for common GitHub token prefixes, PEM private-key headers, or simple password/token/key assignments. This is **not** comprehensive clearance. GitHub may mask secrets in logs, and other builds and Git history were not examined.

## Full local repository scan (maintainer action)

Do this in a trusted workstation with Git and a reputable secret scanner installed. Avoid pasting scan output containing suspected credentials into public GitHub issues or chats.

1. Clone using an authenticated GitHub client (account access to the private repo is required):
   ```sh
   gh repo clone jatayuos4u/jatayuos
   cd jatayuos
   git fetch --all --tags --prune
   ```
2. Install and run the current version of [Gitleaks](https://github.com/gitleaks/gitleaks) following its official installation guidance. Scan complete history, rather than only the working directory:
   ```sh
   gitleaks git --redact --report-format json --report-path ../jatayuos-gitleaks-redacted.json .
   ```
   Confirm your installed version supports these options (`gitleaks git --help`). A nonzero scan exit code typically requires investigating findings, not ignoring them.
3. Independently review configuration, past commits, screenshots, PDFs, archived sources, packed binaries, and Actions logs for access keys, private information, absolute paths, machine IDs, tokens, session credentials, internal email addresses or user information.
4. Treat every detected credential as compromised, **rotate/revoke it first**, then assess whether history rewriting is needed before publication. Removing a file from the current branch does not erase it from Git history. Review GitHub's sensitive-data-removal guidance before any history rewrite.
5. Store the complete scan evidence privately, recording date, scanner version, scanned refs and the final result. Do not commit unredacted findings.

## Publication rights (separate from secrets)

- [ ] Determine the owner-provided logo/wallpaper/screenshots documentation rights and licensed inputs.
- [ ] Resolve pending Firefox downstream redistribution/trademark route.
- [ ] Collect and make available license-required corresponding source, patches and build materials for the *actual Build #38 package manifest*.
- [ ] Distribute complete third-party notices alongside released binaries under the applicable licenses.
- [ ] Review bundled firmware and codecs individually.
- [ ] Preserve accurate Build #38 source, ISO SHA256 and release metadata. Existing v1.0-udaan tag currently refers to Build #37.
- [ ] Verify public ISO hosting and hash a fresh downloaded copy.

## Approval criteria

Make repository public **only** after historical secrets/private-content review and rights to publish committed content have been confirmed. Distribute the ISO **only** after the separate binary licensing/source/hosting checks are complete. Document explicit maintainer approval for each step.
