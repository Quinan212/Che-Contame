"""Comprueba y captura la app normal entregada, sin cambiar sesión ni preferencias."""
from pathlib import Path
import json,os,re,subprocess,time,xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'qa/audio-v3'
ADB=str(Path(os.environ['LOCALAPPDATA'])/'Android/Sdk/platform-tools/adb.exe')
DEVICE='emulator-5554';PACKAGE='ar.contame.contame_android'
def adb(*args):
    return subprocess.run([ADB,'-s',DEVICE,*args],check=True,capture_output=True,
        creationflags=subprocess.CREATE_NO_WINDOW,timeout=25).stdout

assert b'Recorridos_API_36' in adb('emu','avd','name')
for attempt in range(8):
    adb('shell','uiautomator','dump','/sdcard/entrega-v3.xml')
    raw=adb('exec-out','cat','/sdcard/entrega-v3.xml')
    nodes=list(ET.fromstring(raw).iter('node'))
    if b"System UI isn't responding" in raw:
        incident=OUT/'emulador-systemui';incident.mkdir(exist_ok=True)
        (incident/'entrega-usuario.xml').write_bytes(raw)
        (incident/'entrega-usuario.png').write_bytes(adb('exec-out','screencap','-p'))
        close=next(n for n in nodes if n.get('resource-id')=='android:id/aerr_close')
        x0,y0,x1,y1=map(int,re.findall(r'\d+',close.get('bounds')))
        adb('shell','input','tap',str((x0+x1)//2),str((y0+y1)//2))
        time.sleep(1)
        continue
    if any(n.get('package')==PACKAGE and n.get('content-desc')=='Che, preguntame' for n in nodes):
        break
    time.sleep(1)
else: raise RuntimeError('La app normal no publicó una pantalla accesible.')
activity=adb('shell','dumpsys','activity','activities')
assert re.search(rb'topResumedActivity=.*ar.contame.contame_android/\.MainActivity',activity)
(OUT/'entrega-emulador.xml').write_bytes(raw)
(OUT/'entrega-emulador.png').write_bytes(adb('exec-out','screencap','-p'))
logs=adb('logcat','-d','-v','threadtime','-s','flutter','AndroidRuntime')
(OUT/'logs-entrega.txt').write_bytes(logs)
assert b'FATAL EXCEPTION' not in logs and b'No se pudo preparar' not in logs
time.sleep(1.3)
idle=adb('shell','dumpsys','media.audio_flinger')
pid=adb('shell','pidof',PACKAGE).strip().split()[0]
assert not re.search(rb'S\s+\d+\s+yes\s+'+pid+rb'/',idle)
(OUT/'audioflinger-entrega-reposo.txt').write_bytes(idle)
devices=adb('devices')
assert b'emulator-5556' not in devices,'El AVD de QA sigue abierto.'
(OUT/'entrega-verificada.json').write_text(json.dumps(dict(passed=True,
    device=DEVICE,avd='Recorridos_API_36',normal_main=True,
    no_audio_when_idle=True,qa_closed=True),indent=2),encoding='utf-8')
print('Entrega verificada: app normal abierta, sin audio en reposo y QA cerrado.')
