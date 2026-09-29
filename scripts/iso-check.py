#!/usr/bin/env python3
import pathlib,subprocess,sys
p=pathlib.Path(sys.argv[1]); size=p.stat().st_size
print(f'ISO: {size:,} bytes ({size/1024**3:.2f} GiB). No ISO size cap is enforced.')
subprocess.run(['xorriso','-indev',str(p),'-report_el_torito','plain'],check=True)
for path in ['/live/filesystem.squashfs','/live/vmlinuz','/live/initrd.img']:
    r=subprocess.run(['xorriso','-indev',str(p),'-ls',path],text=True,capture_output=True)
    if r.returncode: raise SystemExit(f'ISO missing expected live file: {path}\n{r.stderr}')
print('ISO structure check passed. Boot and installation still require VM tests.')

