#!/usr/bin/env python3
"""Verify the preserved Build 35 ISO and stage local SourceForge release files.
Never builds, uploads, changes repository visibility, or declares license clearance.
"""
import argparse
import hashlib
import json
import re
import shutil
import stat
import sys
import zipfile
from pathlib import Path, PurePosixPath

COMMIT = '95afcb80e3517d8930557d4fb1ba9a20a92b7f7f'
ISO_NAME = 'JatayuOS-1.0-Udaan-amd64.iso'
MANIFEST_HASH = '6f964ab87bc2969cf62cede0281e956a67e72b3e5b5e3b3cd6e9b02ae783c858'
NOTICES_HASH = '42cc525296c43aa4f21b1d145ff5d373d24f1d852a5bc3a3dcd07aa4d1751958'


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(4 * 1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def expected_iso_hash(path):
    matches = []
    for line in Path(path).read_text().splitlines():
        match = re.fullmatch(r'([0-9a-fA-F]{64})[ \t]+\*?(.+)', line)
        if match and match[2] in (ISO_NAME, './' + ISO_NAME):
            matches.append(match[1].lower())
    if len(matches) != 1:
        raise ValueError('SHA256SUMS must contain exactly one entry for ' + ISO_NAME)
    return matches[0]


def validate_notices(path):
    with zipfile.ZipFile(path) as archive:
        names = set()
        for info in archive.infolist():
            name = PurePosixPath(info.filename)
            if (name.is_absolute() or '..' in name.parts or '\\' in info.filename
                    or re.match(r'^[A-Za-z]:', info.filename)
                    or stat.S_ISLNK(info.external_attr >> 16)):
                raise ValueError('Unsafe notice ZIP entry: ' + info.filename)
            if info.filename in names:
                raise ValueError('Duplicate notice ZIP entry: ' + info.filename)
            names.add(info.filename)
        if archive.testzip() is not None:
            raise ValueError('Notice ZIP integrity failure')


def prepare(args):
    repo = Path(__file__).resolve().parents[1]
    iso = Path(args.iso).resolve()
    notices = Path(args.notices).resolve()
    manifest = repo / 'docs/legal/build35/package-manifest.tsv'
    if iso.name != ISO_NAME:
        raise ValueError('Use the original ISO filename: ' + ISO_NAME)
    if Path(args.source_commit).read_text().strip() != COMMIT:
        raise ValueError('SOURCE-COMMIT.txt does not identify the accepted Build 35')
    if sha256(manifest) != MANIFEST_HASH:
        raise ValueError('Preserved manifest differs from the reviewed upload')
    if sha256(notices) != NOTICES_HASH:
        raise ValueError('Notice ZIP differs from the reviewed upload')
    validate_notices(notices)
    expected = expected_iso_hash(args.checksums)
    if sha256(iso) != expected:
        raise ValueError('ISO SHA256 does not match preserved build SHA256SUMS')
    with iso.open('rb') as stream:
        stream.seek(32769)
        if stream.read(5) != b'CD001':
            raise ValueError('File lacks the expected ISO9660 descriptor')
    output = Path(args.output).resolve()
    output.mkdir(parents=True, exist_ok=True)
    if any(output.iterdir()):
        raise ValueError('Use a new empty output directory')
    inputs = {
        'package-manifest.tsv': manifest,
        'third-party-notices.zip': notices,
        'LICENSE': repo / 'LICENSE',
        'COPYRIGHT.md': repo / 'COPYRIGHT.md',
        'README.md': repo / 'docs/releases/sourceforge-README.md',
        'jatayu-tools-2.0.2-source.tar.gz': repo / 'vendor/jatayu-tools-2.0.2-source.tar.gz',
    }
    for name, source in inputs.items():
        if not source.is_file():
            raise ValueError('Missing release input: ' + str(source))
    required_space = sum(p.stat().st_size for p in inputs.values())
    if args.copy_iso:
        required_space += iso.stat().st_size
    if shutil.disk_usage(output).free < required_space + 32 * 1024 * 1024:
        raise ValueError('Not enough free space for staging')
    for name, source in inputs.items():
        shutil.copyfile(source, output / name)
    (output / 'SOURCE-COMMIT.txt').write_text(COMMIT + '\n')
    if args.copy_iso:
        shutil.copyfile(iso, output / ISO_NAME)
        if sha256(output / ISO_NAME) != expected:
            raise ValueError('Copied ISO hash differs')
    metadata = {
        'schema_version': 1,
        'project': 'JatayuOS',
        'website': 'https://jatayuos.in',
        'release_name': '1.0 Udaan — accepted Build 35 candidate',
        'source_commit': COMMIT,
        'runtime_integration_version': '1.0~rc3',
        'iso': {'filename': ISO_NAME, 'sha256': expected,
                'size_bytes': iso.stat().st_size, 'staged': args.copy_iso},
        'original_software_license': 'GPL-3.0-or-later',
        'public_iso_url': None,
        'publication_ready': False,
        'remaining': ['Exact corresponding-source collection and publication',
                      'Artwork/documentation rights and component review',
                      'SourceForge account/project access and upload',
                      'Website download URL and anonymous download verification'],
    }
    (output / 'release.json').write_text(json.dumps(metadata, indent=2) + '\n')
    hashes = [(p.name, sha256(p)) for p in output.iterdir() if p.is_file() and p.name != ISO_NAME]
    hashes.append((ISO_NAME, expected))
    (output / 'SHA256SUMS').write_text(''.join(digest + '  ' + name + '\n' for name, digest in sorted(hashes)))
    print('ISO matches preserved checksum and source commit. Release metadata staged at', output)
    if not args.copy_iso:
        print('Upload the original verified ISO separately; it was not copied into staging.')
    print('Source and rights review still required before public ISO upload.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--iso', required=True)
    parser.add_argument('--checksums', required=True, help='Original build SHA256SUMS')
    parser.add_argument('--source-commit', required=True, help='Original SOURCE-COMMIT.txt')
    parser.add_argument('--notices', required=True, help='Reviewed third-party-notices.zip')
    parser.add_argument('--output', required=True)
    parser.add_argument('--copy-iso', action='store_true', help='Copy verified ISO into staging')
    try:
        prepare(parser.parse_args())
    except (OSError, ValueError, zipfile.BadZipFile) as error:
        print('Release preparation failed:', error, file=sys.stderr)
        raise SystemExit(1)


if __name__ == '__main__':
    main()
