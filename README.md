# JatayuOS integrated development build kit

JatayuOS — Made In India Operating System.

Prepared for Anup Yadav • Debian 13 Trixie • AMD64 • Firefox ESR

**This archive contains source/configuration, not a finished ISO.** No GitHub Actions build has been triggered. Local ISO assembly was blocked by the execution environment's missing mount/chroot capabilities. No claim is made that the first build will succeed or meet a 2 GB ISO/RAM target.

The kit prepares one integrated development image: KDE Plasma, Firefox ESR, Discover, System Settings, Calamares, firmware, Indian input tools, Jatayu desktop/boot branding configuration, live welcome, Aarambh and the seven utility entry points. Read **docs/STATUS.md** for implemented versus incomplete features before using runner minutes.

## Cheapest build route: your own Debian 13 VM

Use a dedicated 64-bit Debian 13 installation or VM with working internet. The build must have administrator privileges and support mounts/chroot. Allocate enough disk for downloaded packages, the uncompressed root filesystem and output images; 25 GB free is a working preflight target, not a measured final requirement. Building locally consumes no GitHub Actions minutes.

Extract the kit, open a terminal in its folder, then run:

```bash
python3 scripts/preflight.py
sudo bash scripts/build.sh
```

The build script installs builder dependencies and adds firmware repository components inside that dedicated environment. Do not run it on an important daily-use installation without reviewing it. It does not select or write a physical installation disk. Test installation only inside a disposable VM initially.

Output is `out/JatayuOS-0.1-dev-amd64.iso`, with `SHA256SUMS`, package/source-version manifest, third-party notices and a build log. These files exist only after the build completes. The archive does not contain a prebuilt ISO.

## One manual GitHub Actions build

The source is maintained at https://github.com/jatayuos4u/jatayuos. The workflow is manual-only. No build runs when source is pushed.

The repository's starter README was public on 27 September 2026. Until the original-code licence and distribution review are complete, change it to **Private** in the repository's Settings → General → Danger Zone → Change repository visibility. On your computer, install Git and [GitHub CLI](https://cli.github.com/), run `gh auth login`, extract the whole source ZIP, and run `bash scripts/push-existing-repo.sh` from the extracted `jatayuos-build` folder. The script checks that the account is `jatayuos4u`, the repository is private and still has only its starter README, then pushes the source. It does not dispatch the ISO workflow. Do not paste credentials in chat.

1. Open **Actions → Manual JatayuOS development ISO → Run workflow** in the repository.
2. Type `BUILD` in the confirmation input. This starts one job with a **60-minute maximum**, not a guaranteed duration or cost.
3. Download the ISO/report artifact and build log promptly. Retention is three days to limit artifact storage. Storage quota and runner-minute charging depend on your GitHub account; no free allowance is assumed.
4. If it fails, download the log and inspect the error before retrying. Do not click Run repeatedly. No automatic retry or scheduled build is configured.

GitHub uses a privileged, temporary Debian 13 Docker builder. The workflow does not publish a release, push commits, upload to another service, or configure credentials. Its GitHub token is read-only. Action major versions are used for this development kit; pin reviewed commit hashes before production use.

## Budget controls

- Static checks run before the build; package candidate checks run before root filesystem assembly.
- Single architecture and job; manual trigger only; no matrix, push/PR triggers, image generation or recurring jobs.
- Fast zstd compression trades some ISO size for lower build CPU time. Under 2 GB is not guaranteed.
- ISO artifact upload uses no extra ZIP compression; artifact retention is short.
- Local builds retain live-build package caches. No large cross-run GitHub cache is uploaded by default, to avoid storage costs.
- A 60-minute job limit prevents an unbounded run but may stop a slow first build. Review the log before deciding to raise it.

## Source kit contents

- `packages.list`, `auto-config.sh`, `hooks/`: live-build configuration.
- `apps/`: shared Python/Qt interfaces and offline processing engine.
- `overlay/`: desktop entries, polkit policy, Plasma defaults, Calamares/Plymouth branding.
- `assets/`: original temporary vector artwork and local notices.
- `scripts/`: preflight, Debian package assembly, ISO assembly and structure checks.
- `tests/`: local file-safety and conversion tests.
- `docs/`: status, compliance and boot/install checklist.

Python/Qt was selected for this first development handoff to avoid compiling seven separate applications. Debian packages supply the runtime. No Electron runtime is used. Qt smoke checks outside Trixie are not proof of Trixie desktop compatibility.

## Important safety and release limits

The approved eagle desktop remains the target. This kit uses original temporary vector artwork because the supplied images were screenshots and their redistribution rights have not been established. No rights-uncleared user artwork is embedded. Do not market the placeholder as the approved final design.

This is an integrated **development** build, not production-ready or security-certified software. Do not publicly redistribute the image until artwork, Firefox/package distribution requirements, corresponding-source access and the project's own licence choice are resolved. Source and notice obligations are not met solely by including this kit.

Next action: run the kit once in a suitable local Debian VM if possible. If GitHub is your only builder, use the manual workflow once, save its log, and test the resulting ISO in a disposable VM before any real disk installation.
