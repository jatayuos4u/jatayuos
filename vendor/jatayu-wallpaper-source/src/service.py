"""Per-user slideshow agent and launcher. SPDX-License-Identifier: GPL-3.0-or-later."""
import os
import re
import sys
import time
import subprocess
from pathlib import Path
from core import CONFIG, VERSION, settings, collection, next_image, wallpaper_script, read_json, write_json
from plasma import Plasma
from PyQt6.QtCore import QLockFile, QTimer

UNIT = 'jatayu-wallpaper.service'

def start_background():
    """Use a user service outside the GUI's desktop scope; detached fallback otherwise."""
    CONFIG.mkdir(parents=True, exist_ok=True)
    launch_lock=QLockFile(str(CONFIG/'launch.lock'))
    if not launch_lock.tryLock(0): return 0
    enabled=settings()['enabled']
    unit=Path('/usr/lib/systemd/user')/UNIT
    systemd=False
    if unit.exists():
        try:
            r=subprocess.run(['systemctl','--user','daemon-reload'],capture_output=True,timeout=5)
            if r.returncode==0:
                command='start' if enabled else 'stop'
                r=subprocess.run(['systemctl','--user',command,UNIT],capture_output=True,timeout=5)
                systemd=r.returncode==0
        except (OSError,subprocess.TimeoutExpired): pass
    if not enabled or systemd: return 0
    # A single lock inside the agent ensures repeated settings changes never create two rotators.
    log=CONFIG/'service.log'
    if log.exists() and log.stat().st_size>1024*1024: log.write_text('')
    try:
        with log.open('ab') as output:
            subprocess.Popen([sys.executable,str(Path(__file__).with_name('app.py')),'--service'],
                stdin=subprocess.DEVNULL,stdout=output,stderr=output,start_new_session=True,close_fds=True)
    except OSError as error:
        write_json(CONFIG/'service-status.json',dict(ok=False,state='error',message=str(error),time=time.time(),version=VERSION))
        return 1
    return 0

class RotationEngine:
    def __init__(self, backend, clock=time.monotonic, wall=time.time):
        self.backend=backend;self.clock=clock;self.wall=wall
        self.signature=None;self.next_due=None;self.cycles=0
        self.last_change=0;self.last_error='';self.last_path=''

    def report(self,state,message,ok=True):
        now=self.wall()
        write_json(CONFIG/'service-status.json',dict(ok=ok,state=state,message=message,time=now,
            version=VERSION,pid=os.getpid(),cycles=self.cycles,last_change=self.last_change,
            last=self.last_path,next_due=now+max(0,(self.next_due or self.clock())-self.clock())))

    def tick(self):
        c=settings();now=self.clock()
        if not c['enabled']:
            self.report('disabled','Automatic rotation is off.');return False
        signature=(c['interval'],c['screen'],c['layout'],c['favourites_only'],c['shuffle'],tuple(c['favourites']),tuple(c['folders']))
        if self.next_due is None:
            self.next_due=now if c['at_login'] else now+c['interval']
        elif signature!=self.signature:
            self.next_due=now+c['interval']
        self.signature=signature
        if now<self.next_due:
            self.report('waiting',self.last_error or 'Automatic rotation is running.',not bool(self.last_error));return True
        state=read_json(CONFIG/'rotation.json',{})
        chosen=next_image(collection(c),c,state.get('last',c.get('last','')))
        if not chosen:
            self.next_due=now+5
            reason='No available favourites. Add a favourite or turn off favourites-only rotation.' if c['favourites_only'] else 'No readable images are available. Add a wallpaper folder.'
            self.last_error=reason;self.report('paused',reason,False);return True
        try:
            ok,result=self.backend.sync(wallpaper_script(chosen,c['screen'],c['layout']))
            count=re.search(r'JATAYU_OK:(\d+)',result)
            ok=ok and bool(count) and int(count.group(1))>0
            if not ok and 'JATAYU_OK:0' in result:result='Selected screen is unavailable. Refresh screens and choose an active display.'
        except Exception as error:
            ok,result=False,str(error)
        if ok:
            write_json(CONFIG/'rotation.json',{'last':chosen})
            self.cycles+=1;self.last_change=self.wall();self.last_path=chosen;self.last_error=''
            self.next_due=self.clock()+c['interval']
            self.report('waiting','Automatic rotation is running.')
        else:
            self.next_due=self.clock()+5;self.last_error=result
            self.report('error',result,False)
        return True

def run_service(app):
    CONFIG.mkdir(parents=True,exist_ok=True)
    lock=QLockFile(str(CONFIG/'service.lock'))
    if not lock.tryLock(0): return 0
    backend=Plasma();engine=RotationEngine(backend)
    def tick():
        try:
            if not engine.tick():app.quit()
        except Exception as error:
            engine.report('error',str(error),False)
            print(str(error),file=sys.stderr,flush=True)
    timer=QTimer();timer.timeout.connect(tick);timer.start(2000)
    QTimer.singleShot(0,tick)
    try:return app.exec()
    finally:lock.unlock()
