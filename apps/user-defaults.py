#!/usr/bin/env python3
"""Initialize directories and Places before Plasma opens file dialogs."""
import os
from pathlib import Path
import subprocess
import tempfile
import xml.etree.ElementTree as ET

def initialize():
    home=Path.home()
    config=Path(os.environ.get('XDG_CONFIG_HOME',home/'.config'))
    data=Path(os.environ.get('XDG_DATA_HOME',home/'.local/share'))
    state=Path(os.environ.get('XDG_STATE_HOME',home/'.local/state'))/'jatayu'
    marker=state/'places-v1'
    if marker.exists():return
    subprocess.run(['xdg-user-dirs-update'],check=True)
    entries=[('Home',home,'user-home')]
    for key,label,icon in [('DESKTOP','Desktop','user-desktop'),('DOCUMENTS','Documents','folder-documents'),('DOWNLOAD','Downloads','folder-download'),('MUSIC','Music','folder-music'),('PICTURES','Pictures','folder-pictures'),('VIDEOS','Videos','folder-videos')]:
        path=Path(subprocess.check_output(['xdg-user-dir',key],text=True).strip())
        if path==home:continue  # Respect an explicitly disabled user directory.
        path.mkdir(parents=True,exist_ok=True)
        entries.append((label,path,icon))
    target=data/'user-places.xbel'
    if target.exists():
        # Never replace malformed or user-managed content with an empty file.
        root=ET.parse(target).getroot()
    else:root=ET.Element('xbel',{'version':'1.0'})
    existing={b.get('href') for b in root.iter('bookmark')}
    ET.register_namespace('bookmark','http://www.freedesktop.org/standards/desktop-bookmarks')
    desired=[(label,path.as_uri(),icon) for label,path,icon in entries]
    desired += [('Trash','trash:/','user-trash'),('Network','remote:/','network-workgroup')]
    changed=False
    for label,url,icon in desired:
        if url in existing:continue
        bookmark=ET.SubElement(root,'bookmark',{'href':url})
        ET.SubElement(bookmark,'title').text=label
        info=ET.SubElement(bookmark,'info')
        metadata=ET.SubElement(info,'metadata',{'owner':'http://freedesktop.org'})
        ET.SubElement(metadata,'{http://www.freedesktop.org/standards/desktop-bookmarks}icon',{'name':icon})
        metadata=ET.SubElement(info,'metadata',{'owner':'http://www.kde.org'})
        ET.SubElement(metadata,'isSystemItem').text='true'
        changed=True
    if changed:
        data.mkdir(parents=True,exist_ok=True)
        if target.exists():
            backup=target.with_name('user-places.xbel.jatayu-backup')
            if not backup.exists():backup.write_bytes(target.read_bytes())
        fd,name=tempfile.mkstemp(dir=data,prefix='.jatayu-places-')
        try:
            with os.fdopen(fd,'wb') as stream:ET.ElementTree(root).write(stream,encoding='utf-8',xml_declaration=True)
            os.replace(name,target)
        finally:Path(name).unlink(missing_ok=True)
    state.mkdir(parents=True,exist_ok=True)
    marker.write_text('Standard Places initialized; future edits belong to the user.\n')

if __name__=='__main__':initialize()
