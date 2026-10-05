# SourceForge delivery for JatayuOS

Selected by the maintainer on 5 October 2026 UTC:
ISO and source hosting on SourceForge; website https://jatayuos.in.
The SourceForge project slug and website code repository have not been supplied.
No SourceForge project, public file or website change is claimed here.

## Selected release

Preserve the accepted Build 35 ISO. Use a folder such as
`releases/1.0-udaan/build-35/`; use `sources/build-35/` for corresponding source.
These are proposed folder paths, not existing download URLs. Keep integration
version `1.0~rc3` visible; this is the accepted candidate, not a newly built final ISO.

## Stage the preserved release locally

Clone/download the repository with its binary source supplements, then retain
the extracted original ISO, SHA256SUMS and SOURCE-COMMIT.txt from Build 35.
Keep the reviewed notice ZIP supplied by the maintainer.

Python 3 command, valid on Windows as well as Linux:

```sh
python scripts/prepare-sourceforge-release.py --iso "JatayuOS-1.0-Udaan-amd64.iso" --checksums "SHA256SUMS" --source-commit "SOURCE-COMMIT.txt" --notices "third-party-notices.zip" --output "sourceforge-stage"
```

The script streams the ISO SHA256, checks the exact source commit, ISO descriptor,
manifest/notice upload hashes and ZIP integrity, then stages metadata/notices and
the recovered Creative Studio source supplement. A new empty output folder is
required. Add `--copy-iso` if you want the ISO copied into staging too.

This does not collect all dependency sources or declare publication cleared.
The ISO checksum in the generated release.json is based on verified local bytes.
Do not replace the preserved build SHA256SUMS with a checksum calculated only
from an unverified download, and never use the artifact ZIP digest as the ISO hash.

## Complete the source and rights materials

Follow [the exact source procedure](../legal/SOURCE-PUBLICATION.md).
Use a Debian environment with authenticated source indices; no GitHub Actions
run is needed. The 805 upstream versions require roughly 6.74 GB before extraction.

Publish full exact-version source archives, source hashes and build instructions;
the licensed Build 35 project source export with its subsequent license supplement;
Calamares/Fcitx patch scripts and pinned base sources; complete local app source
and required inputs; all original notices. Include the newer guides as separate
downloads after their publication terms are recorded.

The source catalogue signature verification attempt on 5 October 2026 UTC
could retrieve keys and match Debian's published Trixie fingerprints, but the
four InRelease downloads timed out. Source indices and archives therefore
remain unauthenticated here. Use the actual source collector in an authenticated
Debian environment; an availability report is not a source archive.

Artwork, logos, screenshots and documentation terms remain separate from the
approved software GPL grant. Review the remaining component requirements in
COMPLIANCE.md, including Firefox's downstream distribution route.

## Upload and verify

SourceForge Files uploads are public; a folder called staging or candidate is
not a private draft. Complete required source/rights work before uploading the ISO.

Use the project's Files manager or SourceForge's documented SFTP/rsync endpoint.
For large files, SourceForge recommends resumable rsync. On Windows, the Files
manager or an SFTP client can upload the preserved files without another ISO build.

Upload corresponding sources, license texts, notices, manifest, release metadata,
guides and checksum files, then the verified ISO. Set the intended ISO as the
default download only after the companion files and anonymous downloads pass.
Do not delete the owner's original copy or create a new written source offer.

The SourceForge README is prepared at sourceforge-README.md. Update its preparation
status after verified publication; preserve candidate/version limitations.

## Website download integration

Use the exact SourceForge per-file download URL observed after upload, rather
than guessing a project slug or relying on a generic latest link. Show on the
website: release/candidate label, AMD64 architecture, size, ISO SHA256, checksum
download, notices, source downloads, guides and known limitations. Confirm the
actual website source repository before editing; the connected account currently
exposes only the OS repository.

Update 1.0-udaan-candidate.json with verified ISO size/hash and public URLs.
Check all download links anonymously; hash the delivered ISO bytes. Mark the
release checklist complete only for items with evidence.

Official procedure:
https://sourceforge.net/p/forge/documentation/Release%20Files%20for%20Download/
