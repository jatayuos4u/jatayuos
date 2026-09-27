"""Safety/regression checks that run without building the operating system."""
import pathlib, sys, tempfile, unittest, shutil
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'apps'))
import engine
from PIL import Image

class Files(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=pathlib.Path(self.tmp.name)
        self.source=self.root/'original.png';Image.new('RGBA',(80,40),(255,0,0,120)).save(self.source)
    def tearDown(self):self.tmp.cleanup()
    def test_image_conversion_preserves_original_and_size(self):
        original=self.source.read_bytes();out=self.root/'small.jpg'
        engine.convert_image([str(self.source)],str(out),'JPG',40,85)
        self.assertEqual(self.source.read_bytes(),original)
        with Image.open(out) as im:self.assertEqual(im.size,(40,20));self.assertEqual(im.mode,'RGB')
    def test_output_cannot_overwrite_input(self):
        with self.assertRaises(ValueError):engine.convert_image([str(self.source)],str(self.source))
    def test_output_symlink_is_rejected(self):
        alias=self.root/'alias.png';alias.symlink_to(self.source)
        with self.assertRaises(ValueError):engine.output_path(alias)
    def test_external_svg_rejected_before_rendering(self):
        svg=self.root/'bad.svg';svg.write_text('<svg xmlns="http://www.w3.org/2000/svg"><image href="https://example.com/image.png"/></svg>')
        with self.assertRaises(ValueError):engine.raster(svg)
    def test_svg_entities_rejected(self):
        svg=self.root/'bad.svg';svg.write_text('<!DOCTYPE svg [<!ENTITY x SYSTEM "file:///etc/passwd">]><svg/>')
        with self.assertRaises(ValueError):engine.raster(svg)
    def test_nested_backup_rejected(self):
        src=self.root/'src';src.mkdir();dest=src/'dest';dest.mkdir()
        with self.assertRaises(ValueError):engine.backup(src,dest)
    @unittest.skipUnless(shutil.which('rsync'),'rsync unavailable')
    def test_backup_restore_roundtrip(self):
        src=self.root/'src';src.mkdir();(src/'note.txt').write_text('important user data')
        dest=self.root/'dest';dest.mkdir();engine.backup(src,dest)
        snap=next(dest.iterdir());out=self.root/'restored';engine.restore(snap,out)
        self.assertEqual((out/'note.txt').read_text(),'important user data')
        with self.assertRaises(ValueError):engine.restore(snap,out)

if __name__=='__main__':unittest.main(verbosity=2)
