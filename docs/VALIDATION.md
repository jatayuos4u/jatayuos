# Local validation report

Validated 27 September 2026. This is source/package validation, NOT an ISO build report.

- 93 package names matched downloaded Debian Trixie package indexes (main and non-free-firmware).
- Python AST parsing and shell syntax checks passed.
- Seven image/file/backup safety tests passed, including an actual rsync backup/restore round trip.
- The jatayu-integration 0.1.0 all-architecture Debian package was assembled and its control metadata inspected.
- The workflow parsed successfully; its only trigger is workflow_dispatch and it has a 60-minute job limit.
- SVG, polkit XML and Calamares branding YAML parsed successfully.
- No GitHub job was dispatched; no GitHub runner minutes were used.

Not verified: full package dependency resolution; live-build completion; ISO boot; offline Calamares installation; default layout rendering; production Qt 6 GUI behaviour; PDF backends; Android; security controls; legal release clearance; RAM/ISO-size claims.

The runtime had no effective mount/chroot capabilities, so a privileged ISO build was not attempted. The environment also changed during the conversation; an earlier Qt Tools-window smoke invocation succeeded, but no current full Qt screen suite was verified. Do not treat that single invocation as GUI acceptance.
