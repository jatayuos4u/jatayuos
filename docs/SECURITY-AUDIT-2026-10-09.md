# ISO build security audit — 9 October 2026

Reviewed source: `d3b3d4e49f071bb3acbce233411c3630479d1ff2` on main. This is a source-level audit of the complete committed ISO build workflow and its build, packaging, generation, image-configuration and release-helper scripts. It is not a vulnerability certification of the ISO or every upstream package.

## Scope and findings

| Surface reviewed | Findings and disposition |
| --- | --- |
| .github/workflows/build-iso.yml | Read-only contents permission, exact checkout SHA, hosted-runner cleanup guard, 50-minute timeout and serialized builds already exist. Fix persisted checkout credentials, mutable Action refs, automatic trigger-file builds and direct input interpolation in builder shell. |
| auto-config.sh; scripts/build.sh; scripts/build-fcitx.sh | Debian 13, HTTPS live-build mirrors, signed APT metadata, pinned Calamares/Fcitx source versions, fail-fast shell and capability checks. Retain. Privileged container and mutable debian:trixie remain explicit follow-up risks. Backports builder source uses HTTP; APT signature verification is retained, but HTTPS should be evaluated in the next builder revision. |
| scripts/package.sh; scripts/postinst; hooks/0900-jatayu.hook.chroot; apps/configure-image.py | Fixed package stage, root-owned package output, preserved conffiles, service checks, firewall deny-incoming default, security updates and time sync. Retain image behavior. These scripts execute as root and must only run from reviewed source in a disposable builder. |
| scripts/prepare-wallpaper.py; vendor/wallpaper-package.json; scripts/preflight.py | Wallpaper parts and complete package and Jatayu Tools package are SHA256 checked before use. Existing full preflight also needs binary assets, PDFs and wallpaper parts; do not label new lightweight checks as that full preflight. |
| scripts/patch-calamares.py; tests/partition-plan-check.py; tests/check-image.py; scripts/iso-check.py | Asserted patch anchors, before/after hashes for upstream partition and bootloader modules, assembled-image assertions and ISO structure checks. Retain; static validation cannot replace boot/install acceptance. |
| scripts/generate-files.py; scripts/prepare-boot-art.py; scripts/generate-documentation.py; scripts/generate-illustrated-guides.py; scripts/generate-installation-guide.py | Local configuration/art/PDF generation from committed inputs. No remote script execution identified in these generators. Generation mutates source assets and overlay; therefore the new PR checks do not run generators. |
| scripts/jatayu; scripts/jatayu-webapp; scripts/jatayu-admin; scripts/jatayu-live-installer; committed Polkit policy | Fixed executables, allowlisted privileged software/actions, live-session checks for installer/layout, admin authentication for install/refresh/Android. Retain. Owner-selected weak-password allowance remains a security tradeoff; changing it requires a separate product decision and runtime validation. |
| scripts/collect-release-sources.py | Validated source identities, exact APT source versions, .dsc SHA256/size verification and dpkg-source extraction. Keep APT authentication enabled. Source extraction should run as an unprivileged user in a disposable workspace. |
| scripts/prepare-sourceforge-release.py | Safe ZIP-name/link checks and preserved checksums. This is a Build 35 helper and must not stage Build 38 as if it were Build 35. Leave historical helper untouched; use final release records for publication. |
| scripts/create-github-repo.sh; scripts/push-existing-repo.sh | Owner/account/private-repository and starter-content checks. Existing comments describing no automatic build can be stale for the original workflow; proposed manual-only workflow removes that hazard after merge. These helpers were read, not executed. |

No AGENTS.md exists in the audited tree. All 22 files under scripts/, the image hook, auto-config and image configuration were included. Binary package internals, generated artwork, every vendored dependency, historical commits and repository secrets were not exhaustively audited. No claim of a complete secrets scan or OS CVE scan is made.

## Proposed hardening

- Disable checkout credential persistence before source is mounted into the root builder.
- Pin checkout and upload-artifact to full upstream commit IDs verified through GitHub refs. Keep the existing v4 action family.
- Make ISO assembly workflow_dispatch-only with BUILD confirmation and existing branch restrictions. The old trigger file is retained as history but has no automatic build effect.
- Pass precheck selection through an environment variable and a shell argument array.
- Add a five-minute, read-only source-check job on ordinary pull_request/push events. No secrets, privileged container, dependency installs, documentation generation or ISO assembly.
- Check Python/shell syntax and narrow workflow security invariants. Run existing mocked helper and user-default tests.
- Add private vulnerability-reporting guidance.

## Validation and preservation

Local checks passed: syntax for 25 Python and 12 shell sources, workflow policy, YAML parsing and eight mocked regression tests. Negative checks rejected mutable Action refs, restored automatic ISO triggers and persisted checkout credentials. Actionlint was unavailable; the policy checker explicitly does not replace it. Full preflight, APT simulation, binary verification, image assembly, ISO boot/install tests and complete dependency CVE scanning were not run.

The accepted Build 38 record identifies source `eb7d73a1b1b7ea55174a9caeda2ff2824ec259a3` and ISO SHA256 `5a5dbc79f724c8353f1173e55edde3f905d9ddb287272d492930e6730650e040`. Existing release v1.0-udaan still targets `45b7d1f76dea0184b0fcf7dd1c900f4edf139552` (Build 37). This provenance mismatch is recorded for a separate publication review; this PR does not retag or edit the release.

No ISO, release/tag, build-trigger file, existing release metadata, package, branding, installer or runtime configuration is changed. No full ISO workflow is dispatched. These changes harden future repository automation; they do not retrofit the already-built ISO.

## Follow-up settings for the maintainer

These are recommendations, not applied account/repository changes:

1. Enable account 2FA/passkeys and review collaborator, GitHub App and token access.
2. Protect main and release tags against force-push/deletion. Require PR review and the source checks after the workflow is available on main; ensure there is an actual independent reviewer if requiring approvals on a sole-maintainer repository.
3. Restrict allowed Actions and require full SHA pinning where the repository plan supports it. Retain read-only default workflow permissions.
4. Evaluate secret scanning/push protection and dependency alerts where available for the private repository and plan. Never post a suspected secret in a public issue.
5. Review container digest pinning and precheck isolation in a later builder change, with lightweight dependency validation before authorizing an ISO rebuild. Debian repositories intentionally track updates rather than an immutable package snapshot.
6. Preserve a separate copy of the finalized ISO and checksum. Existing one-day Actions artifact retention is not permanent release storage; this audit did not download or rehash the ISO.
