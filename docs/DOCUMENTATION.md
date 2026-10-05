# JatayuOS documentation inventory

Edition 2, prepared 5 October 2026 for final-version source. The original ten
owner VM captures are preserved under `docs/screenshots/build35/`. The images
show Build 35; they do not prove a final-version ISO has been built or tested.

| Committed document | Edition | Pages | Bytes |
| --- | --- | ---: | ---: |
| [USER-MANUAL.pdf](../assets/USER-MANUAL.pdf) | 2 | 16 | 8920494 |
| [INSTALLATION-GUIDE.pdf](../assets/INSTALLATION-GUIDE.pdf) | 2 | 6 | 4395160 |
| [FAQ.pdf](../assets/FAQ.pdf) | 2 | 5 | 53126 |

## Committed-file SHA256 values

```text
bd52f1a2dd0880578109539d8450e179f69a2753da71d478e505c448babd6ba4  assets/USER-MANUAL.pdf
ebb102d5d070d7b261fef0e39fd710324e78c869567100958e9ffddc4974b502  assets/INSTALLATION-GUIDE.pdf
5a72ea8722969745c32ab046e3aa92de949c8ccd90d9c4a1f699c3da0e211979  assets/FAQ.pdf
```

Regenerate with `python3 scripts/generate-documentation.py`. ReportLab and
DejaVu fonts are required. This command writes the three illustrated PDFs,
About and the offline README; the build runs it before packaging. PDF metadata
is deterministic in the same runtime; hashes may differ with dependency versions.
Verify the actual ISO-bundled files and publish hashes for the delivered files.

The accepted Build 35 ISO still contains the older bundled PDFs. The separately
delivered edition 1 guides and their hashes remain preserved in
[candidate metadata](releases/1.0-udaan-candidate.json). Do not substitute these
edition 2 hashes for those historical files.

The User Manual covers all ten captures, desktop applications, updates, time,
Waydroid, troubleshooting and credits. The Installation Guide covers checksum
verification, live boot, clean installation, Windows UEFI manual dual boot and
first installed login. The FAQ covers installation, updates, application scope,
Android, backups and support. All 27 pages were rendered and visually reviewed.

See [quick guide](USER-GUIDE.md), [screenshot provenance](SCREENSHOTS.md) and
[final preparation metadata](releases/1.0-udaan-final.json). Documentation/artwork
publication permissions remain a separate release gate from software licensing.
