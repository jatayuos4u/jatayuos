#!/usr/bin/env python3
"""Reassemble the unchanged, owner-supplied package and verify every byte."""
from pathlib import Path
import hashlib, json, os, tarfile
ROOT=Path(__file__).resolve().parents[1]
def prepare():
    manifest=json.loads((ROOT/'vendor/wallpaper-package.json').read_text())
    out=ROOT/'out';out.mkdir(exist_ok=True)
    target=out/'jatayu-wallpaper_1.2.1_all.deb'
    temporary=target.with_suffix('.tmp')
    whole=hashlib.sha256();total=0
    try:
        with temporary.open('wb') as output:
            for part in manifest['parts']:
                data=(ROOT/part['file']).read_bytes()
                if len(data)!=part['size'] or hashlib.sha256(data).hexdigest()!=part['sha256']:
                    raise ValueError('Wallpaper part checksum mismatch: '+part['file'])
                output.write(data);whole.update(data);total+=len(data)
        if whole.hexdigest()!=manifest['sha256'] or total!=manifest['size']:
            raise ValueError('Complete wallpaper package checksum mismatch')
        os.replace(temporary,target)
    finally:
        temporary.unlink(missing_ok=True)
    doc=ROOT/'overlay/usr/share/doc/jatayu-wallpaper';doc.mkdir(parents=True,exist_ok=True)
    with tarfile.open(doc/'application-source.tar.gz','w:gz') as archive:
        archive.add(ROOT/'vendor/jatayu-wallpaper-source',arcname='jatayu-wallpaper-source',filter=lambda info: None if '__pycache__' in info.name else info)
    print('Wallpaper 1.2.1: original package checksum PASS; application source bundled.')
    return target
if __name__=='__main__':prepare()
