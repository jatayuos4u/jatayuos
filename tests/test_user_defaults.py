import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

spec=importlib.util.spec_from_file_location('user_defaults',Path(__file__).resolve().parents[1]/'apps/user-defaults.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)

class Places(unittest.TestCase):
    def initialize(self, home):
        mapping={'DESKTOP':'Desktop','DOCUMENTS':'Documents','DOWNLOAD':'Downloads','MUSIC':'Music','PICTURES':'Pictures','VIDEOS':'Videos'}
        with patch.object(module.Path,'home',return_value=home),patch.dict(module.os.environ,{'XDG_CONFIG_HOME':str(home/'.config'),'XDG_DATA_HOME':str(home/'.local/share'),'XDG_STATE_HOME':str(home/'.local/state')}),patch.object(module.subprocess,'run'),patch.object(module.subprocess,'check_output',side_effect=lambda command,**kw:str(home/mapping[command[1]])+'\n'):
            module.initialize()
    def test_new_account_and_no_reset(self):
        with tempfile.TemporaryDirectory() as temp:
            home=Path(temp);self.initialize(home)
            target=home/'.local/share/user-places.xbel'
            root=ET.parse(target).getroot()
            self.assertEqual([b.findtext('title') for b in root.findall('bookmark')],['Home','Desktop','Documents','Downloads','Music','Pictures','Videos','Trash','Network'])
            root.remove(root.findall('bookmark')[2]);ET.ElementTree(root).write(target)
            edited=target.read_bytes();self.initialize(home)
            self.assertEqual(target.read_bytes(),edited)
    def test_existing_bookmarks_preserved_and_backed_up(self):
        with tempfile.TemporaryDirectory() as temp:
            home=Path(temp);target=home/'.local/share/user-places.xbel';target.parent.mkdir(parents=True)
            original=b'<xbel version="1.0"><bookmark href="smb://server/share"><title>My Share</title></bookmark></xbel>'
            target.write_bytes(original);self.initialize(home)
            self.assertEqual(ET.parse(target).getroot().find('bookmark').get('href'),'smb://server/share')
            self.assertEqual(target.with_name('user-places.xbel.jatayu-backup').read_bytes(),original)
    def test_invalid_bookmarks_not_overwritten(self):
        with tempfile.TemporaryDirectory() as temp:
            home=Path(temp);target=home/'.local/share/user-places.xbel';target.parent.mkdir(parents=True);target.write_text('invalid')
            with self.assertRaises(ET.ParseError):self.initialize(home)
            self.assertEqual(target.read_text(),'invalid')
