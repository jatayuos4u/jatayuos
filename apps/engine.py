"""Jatayu offline operations. No shell execution and no in-place document writes.

Development source; licensing decision for original project code is pending.
"""
from pathlib import Path
import datetime, json, os, shutil, subprocess, tempfile, warnings
from PIL import Image, ImageOps

Image.MAX_IMAGE_PIXELS = 40_000_000
warnings.simplefilter('error', Image.DecompressionBombWarning)
FORMATS = {'JPG':'JPEG', 'JPEG':'JPEG', 'PNG':'PNG', 'WEBP':'WEBP', 'BMP':'BMP'}

def command(argv, timeout=180):
    r = subprocess.run([str(x) for x in argv], capture_output=True, text=True, timeout=timeout)
    if r.returncode:
        raise RuntimeError((r.stderr or r.stdout or f'Exit {r.returncode}')[-3000:])
    return r.stdout

def source_file(value):
    p=Path(value).expanduser().resolve(strict=True)
    if not p.is_file(): raise ValueError('Choose a regular input file.')
    if p.stat().st_size > 512*1024*1024: raise ValueError('Development limit: 512 MiB per input file.')
    return p

def output_path(value):
    p=Path(value).expanduser().absolute()
    if p.exists() or p.is_symlink(): raise ValueError('Output exists. Choose a new filename to preserve your original.')
    if not p.parent.is_dir(): raise ValueError('Output directory does not exist.')
    return p

def publish(temp, output):
    # link creates destination exclusively; no race can overwrite a user's file.
    os.link(temp, output)

def raster(p):
    if p.suffix.lower()=='.svg':
        raw=p.read_bytes()
        if len(raw)>4*1024*1024: raise ValueError('SVG too large.')
        import xml.etree.ElementTree as ET
        if b'<!DOCTYPE' in raw.upper() or b'<!ENTITY' in raw.upper(): raise ValueError('SVG entities are not allowed.')
        root=ET.fromstring(raw)
        for node in root.iter():
            tag=node.tag.split('}')[-1].lower()
            if tag in {'script','foreignobject','image','use','style'}: raise ValueError('Only self-contained simple SVG artwork is supported.')
            for key,val in node.attrib.items():
                if key.split('}')[-1].lower()=='href' or 'url(' in val.lower(): raise ValueError('External/resource SVG references are not supported.')
        with tempfile.TemporaryDirectory(prefix='jatayu-svg-') as d:
            dest=Path(d)/'image.png'
            command(['rsvg-convert','--width','2048','--height','2048','--keep-aspect-ratio','--output',dest,p])
            with Image.open(dest) as im: return im.copy()
    with Image.open(p) as im:
        im.load()
        return ImageOps.exif_transpose(im).copy()

def convert_image(inputs, output, fmt='PNG', width=0, quality=85):
    p=source_file(inputs[0]); out=output_path(output)
    im=raster(p)
    if width:
        if not 16<=int(width)<=8192: raise ValueError('Width must be 16–8192 pixels.')
        im.thumbnail((int(width),8192),Image.Resampling.LANCZOS)
    fmt=FORMATS[fmt.upper()]
    if fmt in {'JPEG','BMP'}:
        bg=Image.new('RGB',im.size,'white')
        if im.mode in {'RGBA','LA'}: bg.paste(im,mask=im.getchannel('A'))
        else: bg.paste(im.convert('RGB'))
        im=bg
    im.info.clear()
    with tempfile.TemporaryDirectory(dir=out.parent,prefix='.jatayu-') as d:
        dest=Path(d)/'out'
        im.save(dest,format=fmt,quality=int(quality),optimize=True)
        publish(dest,out)
    return f'Saved {out}\n{out.stat().st_size:,} bytes. Original preserved; metadata not copied.'

def images_to_pdf(inputs,output):
    if not 1<=len(inputs)<=30: raise ValueError('Select 1–30 images per document in this development build.')
    out=output_path(output)
    with tempfile.TemporaryDirectory(dir=out.parent,prefix='.jatayu-') as d:
        pages=[]
        for n,p in enumerate(inputs):
            im=raster(source_file(p)); im.thumbnail((3508,3508),Image.Resampling.LANCZOS)
            bg=Image.new('RGB',im.size,'white')
            if im.mode in {'RGBA','LA'}: bg.paste(im,mask=im.getchannel('A'))
            else: bg.paste(im.convert('RGB'))
            page=Path(d)/f'{n}.pdf'; bg.save(page,'PDF',resolution=150); pages.append(page)
            im.close(); bg.close()
        target=Path(d)/'merged.pdf'
        command(['qpdf','--empty','--pages',*pages,'--',target])
        publish(target,out)
    return f'Saved {out}'

def merge_pdf(inputs,output):
    if not 2<=len(inputs)<=50: raise ValueError('Select 2–50 PDFs in merge order.')
    out=output_path(output); src=[source_file(x) for x in inputs]
    with tempfile.TemporaryDirectory(dir=out.parent,prefix='.jatayu-') as d:
        temp=Path(d)/'merged.pdf'; command(['qpdf','--empty','--pages',*src,'--',temp]); publish(temp,out)
    return f'Saved {out}'

def compress_pdf(inputs,output,quality='ebook'):
    out=output_path(output); p=source_file(inputs[0])
    if quality not in {'screen','ebook','printer'}: raise ValueError('Unknown quality preset')
    with tempfile.TemporaryDirectory(dir=out.parent,prefix='.jatayu-') as d:
        temp=Path(d)/'compressed.pdf'
        command(['gs','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=pdfwrite','-dCompatibilityLevel=1.6',f'-dPDFSETTINGS=/{quality}',f'-sOutputFile={temp}',p])
        publish(temp,out)
    return f'Saved {out}\nBefore: {p.stat().st_size:,} bytes; after: {out.stat().st_size:,} bytes. Compression may be lossy or increase size.'

def pdf_to_images(inputs,output):
    p=source_file(inputs[0]); out=output_path(output)
    info=command(['pdfinfo',p])
    pages=next((int(x.split(':')[1]) for x in info.splitlines() if x.startswith('Pages:')),0)
    if not 1<=pages<=100: raise ValueError('Development limit: 1–100 pages.')
    with tempfile.TemporaryDirectory(dir=out.parent,prefix='.jatayu-') as d:
        command(['pdftoppm','-png','-r','120','-scale-to','2400',p,str(Path(d)/'page')])
        out.mkdir()  # fails if another process created the output directory
        for f in Path(d).glob('page-*.png'): shutil.move(str(f),out/f.name)
    return f'Saved page images to {out}'

def backup(source,destination):
    src=Path(source).expanduser().resolve(strict=True); root=Path(destination).expanduser().resolve(strict=True)
    if not src.is_dir() or not root.is_dir(): raise ValueError('Choose source and destination folders.')
    if src==root or src in root.parents or root in src.parents: raise ValueError('Backup destination and source must be separate, non-nested folders.')
    name='JatayuBackup-'+datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f')
    target=root/name; target.mkdir(mode=0o700)
    try:
        command(['rsync','-rt','--links','--safe-links','--exclude=.cache/','--exclude=.local/share/Trash/','--',str(src)+'/',str(target/'files')+'/'],timeout=7200)
        (target/'manifest.json').write_text(json.dumps({'format':1,'source_name':src.name,'created':datetime.datetime.now().isoformat()},indent=2))
    except Exception:
        (target/'INCOMPLETE').write_text('Backup did not complete. Do not rely on this snapshot.')
        raise
    return f'Backup complete: {target}\nKeep a copy on a separate physical drive. This is not a system snapshot.'

def restore(source,destination):
    src=Path(source).resolve(strict=True); out=output_path(destination)
    if (src/'INCOMPLETE').exists(): raise ValueError('This backup is incomplete.')
    manifest=json.loads((src/'manifest.json').read_text())
    if manifest.get('format')!=1 or not (src/'files').is_dir(): raise ValueError('Not a Jatayu file backup.')
    if src in out.parents: raise ValueError('Restore outside the backup folder.')
    out.mkdir(mode=0o700)
    command(['rsync','-rt','--links','--safe-links','--',str(src/'files')+'/',str(out)+'/'],timeout=7200)
    return f'Restored to new folder: {out}. Existing personal files were not overwritten.'

def diagnostics():
    sections=[]
    for label,args in [('Kernel',['uname','-srmo']),('Memory',['free','-h']),('Storage',['df','-h','/']),('Network status',['nmcli','-t','-f','STATE,CONNECTIVITY','general']),('Failed services',['systemctl','--failed','--no-pager'])]:
        try: data=command(args,timeout=10)
        except Exception as e: data=str(e)
        sections.append(label+'\n'+data)
    return '\n\n'.join(sections)+'\n\nLocal report only. Review before sharing; no upload was performed.'

