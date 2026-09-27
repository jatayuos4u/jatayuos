# Exact implementation status

This table distinguishes included source from completed product features. No ISO has been assembled or boot-tested in the assistant environment.

| Area | Included in this kit | Still required |
|---|---|---|
| Base image | Trixie AMD64 live-build, package list, Debian builder | Actual package dependency resolution, full build and boot |
| Firefox | Debian firefox-esr, desktop associations and panel launcher | Browser/runtime tests and release distribution review |
| Plasma | Standard Kickoff, bottom panel, original frame, Breeze dark defaults | Exact custom category menu, angled segmented panel, screen-size testing |
| Wallpaper/logo | Original code-drawn placeholders | Clean approved eagle artwork, rights verification, production sizes |
| Boot/login | Plymouth text theme with password/question callbacks; Breeze login background | Full shield/progress design, GRUB visual theme, runtime tests |
| Live welcome | Language/keyboard selections, network entry, Try/Install actions | Automatic Calamares selection transfer; user currently confirms again in installer; full Hindi UI |
| Calamares | Debian sequence retained, branded component, final confirmation enabled, offline GRUB binary strategy | VM install/UEFI/BIOS/Windows/encryption validation; Secure Boot not claimed |
| Aarambh | Curated software checkboxes, authenticated installation, completion state | Accurate download-size preview, cancellation-safe package UI refinements |
| Jatayu Update | Refresh, APT history, Discover update entry | Signed Jatayu repository and cosmetic rollout infrastructure |
| Sanjeevani | Manual dated folder backups, safe restore to new folder | Scheduling, encryption, system snapshots and boot recovery |
| Jaanch | Local kernel/memory/storage/network/service checks, save report | Detailed disk-health/driver diagnostics and redaction review |
| Bhasa Setu | KDE/Fcitx setup entry points, Hindi package installer | Verified input/UI localization on actual desktop |
| Sarkar Setu | Labelled portal links opened in default browser, no credential handling | Live link verification, broader curated directory, translation |
| Jatayu Tools | Single-image convert/resize/compress; images-to-PDF; merge/compress PDFs; PDF-to-images | Full PDF backend tests; multi-image conversion, split/rotate UI, target-byte compression, preview and cancellation |
| Android | Local readiness screen and controls for an already installed Waydroid | Verified Waydroid package/repository integration and runtime installation; Android apps do NOT work out of the box |
| Security | AppArmor packages, firewall defaults, narrow polkit helper, unattended security-update config, zram | Runtime policy/privilege/security tests and real resource measurements |
| Compliance | Notices collection, package/source-version manifest, explicit release checklist | Corresponding-source archive delivery, permissions and final licence selections |

Known engineering risks before spending build minutes:

1. Package names were checked against the downloaded Debian Trixie index, but this is not a complete dependency simulation or live-build run.
2. Desktop defaults and copied Breeze theme paths require testing in the actual Plasma version. Existing users' layouts are not forcibly reset.
3. The image uses dpkg diversions for os-release and Debian's installer GRUB helper. Upgrade migration and uninstall behaviour need review before production release.
4. Firewall and unattended-update settings are build inputs; no effective-policy claim is made without boot tests.
5. The builder uses latest Trixie repository candidates, not a frozen snapshot. Package versions and source references must be retained for each release.
6. Images and PDFs are untrusted input. Current size limits and restricted SVG parsing reduce risk but do not replace backend security updates and sandbox testing.
7. All GUI operations currently prevent closing while active. Fine-grained cancellation is not implemented.

Do not hide these limitations in public release notes or describe this kit as the full completed JatayuOS product.
