# Updates for installed JatayuOS systems

## Decision

Use Debian APT for OS and Jatayu packages. Keep Debian Trixie security and stable updates enabled. Publish Jatayu changes as signed Debian packages from a separate Jatayu repository; ISO artifacts are installation media, not an update channel.

## Package boundaries

- `jatayu-tools`: owner utility application and its own dependencies. Retain its upstream package version; update it by publishing a higher Debian package version.
- `jatayu-branding`: logo, wallpapers, Plymouth, boot artwork, Plasma theme, Calamares branding, launchers and icons. Installed-OS assets should update here; Calamares branding mainly affects the live installer.
- `jatayu-desktop`: Aarambh, web app wrappers, desktop entries and integration code. Transitional `jatayu-integration` should depend on the split packages during migration.
- `jatayu-defaults`: `/etc/skel` defaults and system policies. Do not overwrite existing users' Plasma layout or settings in maintainer scripts. Offer an explicit opt-in “Apply new Jatayu look” action, with backup and preview.
- `jatayu-release`: APT source, repository signing key, package pin policy and update channel identity.

## Publishing path

1. Build each `.deb` in CI, run package install/upgrade tests against a clean Debian Trixie VM and the previous JatayuOS image, and sign the APT Release metadata with an offline-controlled signing key.
2. Publish a versioned APT repository (for example under the project's own domain) with staging and stable channels. Never use an unsigned repository or an `apt-key` style global trust entry. Use a dedicated `Signed-By` keyring in a deb822 source file.
3. First publish to staging; install, upgrade, and rollback via package version on a disposable installed-system VM, including preservation of user files and modified configs. Promote the same packages to stable after checks.
4. Show available Jatayu package updates through Discover/PackageKit. Jatayu Tools can link to the system updater and show Jatayu package versions; it should delegate transactions and authentication to APT/PackageKit rather than implement a second updater.
5. Generate a refreshed ISO from the same signed package versions. Installed systems receive the packages without reinstalling. Keep prior package versions and release notes for rollback.

## Migration and acceptance checks

The current 0.1.0 `jatayu-integration` package owns many files. Before splitting, enumerate every path with `dpkg-deb -c` and assign exactly one new owner. Use appropriate `Replaces`/`Breaks` (or a transition version) so upgrades do not fail with file-overwrite errors. Keep `jatayu-tools`' existing package separate.

Do not publish a repository until the maintainer has selected a domain/storage location, a signing-key custody method, and stable-channel policy. CI can prepare staging packages and VM tests before those decisions.

The ISO needs separate validation for live boot, Calamares install, and installed-system upgrade. A successful package build alone does not establish these results.
