# Verify the JatayuOS 1.0 Udaan ISO

These instructions apply to [Build #38](https://github.com/jatayuos4u/jatayuos/actions/runs/37589010270).

## Recorded Build #38 verification

**Completed by the maintainer on 7 October 2026**, using sha256sum on the
downloaded ISO on the Acer test laptop, independently of the CI builder.
The maintainer supplied this terminal output:

```text
JatayuOS-1.0-Udaan-amd64.iso: OK
eb7d73a1b1b7ea55174a9caeda2ff2824ec259a3
5a5dbc79f724c8353f1173e55edde3f905d9ddb287272d492930e6730650e040  JatayuOS-1.0-Udaan-amd64.iso
```

This records a matching checksum and the correct build source.
Evidence is the maintainer's supplied command output; the assistant did not
download or independently hash the ISO. The ISO size of 2,373,058,560 bytes is
from CI; no local stat output was supplied. Boot/install testing and verification
of a later public-hosted download remain separate steps.

[Download the recorded checksum](releases/1.0-udaan-build38.SHA256SUMS).

## Download and extract the bundle

Download the private **JatayuOS-1.0-Udaan-ISO** artifact from that run.
Extract the ZIP and open Konsole in the directory containing these files:

- `JatayuOS-1.0-Udaan-amd64.iso`
- `SHA256SUMS`
- `SOURCE-COMMIT.txt`

The temporary Actions artifact expires on **8 October 2026 at 08:09:32 UTC
(13:39:32 IST)**. Keep a copy for verification and permanent hosting.

## Verify the ISO and provenance

Run these commands from that extracted directory:

```sh
sha256sum --check SHA256SUMS
cat SOURCE-COMMIT.txt
stat -c '%n: %s bytes' JatayuOS-1.0-Udaan-amd64.iso
sha256sum JatayuOS-1.0-Udaan-amd64.iso
```

The first command must print:

```text
JatayuOS-1.0-Udaan-amd64.iso: OK
```

Its exit status must be zero. A mismatch, unreadable file or malformed checksum
is not a successful verification. Preserve the original checksum file rather
than replacing it with a newly generated one to make a mismatch disappear.

Expected source commit:

```text
eb7d73a1b1b7ea55174a9caeda2ff2824ec259a3
```

Expected ISO size: **2,373,058,560 bytes**. The final command prints the exact
64-character ISO SHA256 for recording in the release metadata and README.

## Record the result

Preserve the checksum output, source SHA, ISO size, verification date and the
machine/tool used. Send these results to the maintainer for the verified build
record. The checksum status can be changed to independently verified only
after hashing the downloaded ISO and matching the supplied checksum.

This checks that the downloaded bytes match the build bundle. It does not
replace boot/install testing or cryptographically authenticate the distributor
if the checksum and ISO are obtained from an untrusted source. Publish the
verified checksum through the official website/release record; signed checksums
can provide an additional authenticity check.

The Actions artifact ZIP has its own digest:
`78f1fdd5e2b4989ee74c0dbb02e084e79d82c8ff250f39e0fe2aaf71ff46cb77`.
That digest identifies the ZIP archive, **not the ISO inside it**.

## After permanent upload

Download the ISO again from its final public hosting URL and run the same
checksum check. Publish that exact ISO checksum alongside the download and keep
the source commit record with the release material.

Reference: [GNU Coreutils SHA-2 utilities](https://www.gnu.org/software/coreutils/manual/html_node/sha2-utilities.html).
