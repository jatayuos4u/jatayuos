"""Exercise authenticated Android actions without starting a real service."""
from pathlib import Path
import runpy
import unittest
from unittest.mock import patch

HELPER=Path(__file__).resolve().parents[1]/'scripts/jatayu-admin'

class AndroidActions(unittest.TestCase):
    def invoke(self,arguments,initialized=True):
        with patch('sys.argv',[str(HELPER),*arguments]), \
             patch('os.geteuid',return_value=0), \
             patch('pathlib.Path.is_file',return_value=initialized), \
             patch('subprocess.run') as run:
            runpy.run_path(str(HELPER),run_name='__main__')
            return run.call_args_list

    def test_start_uses_only_fixed_service(self):
        calls=self.invoke(['android-start'])
        self.assertEqual(len(calls),1)
        self.assertEqual(calls[0].args[0],['/usr/bin/systemctl','start','waydroid-container.service'])
        self.assertTrue(calls[0].kwargs['check'])

    def test_stop_uses_only_fixed_service(self):
        calls=self.invoke(['android-stop'])
        self.assertEqual(calls[0].args[0],['/usr/bin/systemctl','stop','waydroid-container.service'])

    def test_uninitialized_start_rejected(self):
        with self.assertRaises(SystemExit):self.invoke(['android-start'],initialized=False)

    def test_service_argument_injection_rejected(self):
        with self.assertRaises(SystemExit):self.invoke(['android-start','ssh.service'])

    def test_unprivileged_start_rejected(self):
        with patch('sys.argv',[str(HELPER),'android-start']),patch('os.geteuid',return_value=1000),patch('subprocess.run') as run:
            with self.assertRaises(SystemExit):runpy.run_path(str(HELPER),run_name='__main__')
            run.assert_not_called()
