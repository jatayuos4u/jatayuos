import os,sys,tempfile,subprocess
from pathlib import Path
cfg=Path(tempfile.mkdtemp())/'bus.conf'
cfg.write_text('''<!DOCTYPE busconfig PUBLIC "-//freedesktop//DTD D-Bus Bus Configuration 1.0//EN" "http://www.freedesktop.org/standards/dbus/1.0/busconfig.dtd"><busconfig><type>session</type><listen>tcp:host=127.0.0.1,port=0</listen><auth>ANONYMOUS</auth><allow_anonymous/><policy context="default"><allow send_destination="*" eavesdrop="true"/><allow receive_sender="*" eavesdrop="true"/><allow own="*"/></policy></busconfig>''')
bus=subprocess.Popen(['dbus-daemon','--nofork','--print-address=1','--config-file='+str(cfg)],stdout=subprocess.PIPE,text=True)
try:
    address=bus.stdout.readline().strip()
    if not address:raise RuntimeError('Test D-Bus daemon could not start')
    env=os.environ.copy();env['DBUS_SESSION_BUS_ADDRESS']=address
    result=subprocess.run([sys.executable,str(Path(__file__).with_name('test_release.py'))],env=env)
finally:
    bus.terminate();bus.wait(timeout=5)
sys.exit(result.returncode)
