import sys, json
from PyQt6.QtCore import QCoreApplication,QObject,pyqtSlot,pyqtClassInfo
from PyQt6.QtDBus import QDBusConnection
from PyQt6.QtQml import QJSEngine
@pyqtClassInfo('D-Bus Interface','org.kde.PlasmaShell')
class Shell(QObject):
    @pyqtSlot(str,result=str)
    def evaluateScript(self,script):
        e=QJSEngine()
        e.evaluate('''var lines=[];var writes=[];
function print(x){lines.push(x);}function currentActivity(){return 'a';}
function desk(n){return {screen:n,wallpaperPlugin:'',currentConfigGroup:[],writeConfig:function(k,v){writes.push([n,k,v]);}};}
function desktopsForActivity(a){return [desk(0),desk(2),desk(-1)];}''')
        result=e.evaluate(script)
        if result.isError():return 'ERROR:'+result.toString()
        output=e.evaluate("lines.join('\\n')").toString()
        with open(sys.argv[1],'a') as f:f.write(e.evaluate('JSON.stringify(writes)').toString()+'\n')
        return output
app=QCoreApplication(sys.argv);shell=Shell();bus=QDBusConnection.sessionBus()
assert bus.registerService('org.kde.plasmashell')
assert bus.registerObject('/PlasmaShell',shell,QDBusConnection.RegisterOption.ExportAllSlots)
print('READY',flush=True);sys.exit(app.exec())
