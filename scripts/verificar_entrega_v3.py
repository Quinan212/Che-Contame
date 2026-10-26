"""Recorre el APK normal de v3 en QA y verifica sus 41 assets exportados."""
from pathlib import Path
import hashlib,json,os,re,subprocess,time,zipfile,xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'qa/audio-v3'
APK=OUT/'che-preguntame-debug.apk'
ADB=str(Path(os.environ['LOCALAPPDATA'])/'Android/Sdk/platform-tools/adb.exe')
DEVICE='emulator-5556';PACKAGE='ar.contame.contame_android'
HIDDEN=subprocess.CREATE_NO_WINDOW

def adb(*args):
    return subprocess.run([ADB,'-s',DEVICE,*args],check=True,capture_output=True,
                          creationflags=HIDDEN).stdout

def run(script,arguments,log):
    import sys
    with (OUT/log).open('w',encoding='utf-8') as output:
        result=subprocess.run([sys.executable,str(ROOT/'scripts'/script),*arguments],
            cwd=ROOT,stdout=output,stderr=subprocess.STDOUT,creationflags=HIDDEN)
    assert result.returncode==0,(script,(OUT/log).read_text(encoding='utf-8'))
    print((OUT/log).read_text(encoding='utf-8').strip(),flush=True)

with zipfile.ZipFile(APK) as archive:
    prefix='assets/flutter_assets/assets/sonidos/'
    names=[n for n in archive.namelist() if n.startswith(prefix) and n.endswith('.wav')]
    local=list((ROOT/'assets/sonidos').glob('*.wav'))
    assert len(names)==len(local)==41
    assert set(n[len(prefix):] for n in names)==set(p.name for p in local)
    for p in local:
        assert archive.read(prefix+p.name)==p.read_bytes(),p.name
(OUT/'assets-apk.json').write_text(json.dumps(dict(passed=True,count=41,
    sha256=hashlib.sha256(APK.read_bytes()).hexdigest()),indent=2),encoding='utf-8')
print('APK normal: 41 exportaciones exactas.',flush=True)

# La limpieza se limita a este AVD separado. Los datos de Alan se conservan.
assert b'ChePreguntame_QA_API_36' in adb('emu','avd','name')
adb('install','-r','-t',str(APK))
adb('shell','pm','clear',PACKAGE)
adb('logcat','-c')
adb('shell','am','start','-n',PACKAGE+'/.MainActivity')
time.sleep(3)
# Con pocos recursos el sistema del AVD puede demorarse al cambiar de APK.
# Guardar el incidente y recuperar exclusivamente su diálogo observado.
for attempt in range(12):
    adb('shell','uiautomator','dump','/sdcard/inicio-v3.xml')
    raw=adb('exec-out','cat','/sdcard/inicio-v3.xml')
    try:
        nodes=list(ET.fromstring(raw).iter('node'))
    except ET.ParseError:
        assert b'ChePreguntame_QA_API_36' in adb('emu','avd','name'), 'QA no está disponible.'
        time.sleep(1)
        continue
    if b"System UI isn't responding" in raw:
        incident=OUT/'emulador-systemui';incident.mkdir(exist_ok=True)
        (incident/f'inicio-{attempt}.xml').write_bytes(raw)
        (incident/f'inicio-{attempt}.png').write_bytes(adb('exec-out','screencap','-p'))
        close=next(n for n in nodes if n.get('resource-id')=='android:id/aerr_close')
        x0,y0,x1,y1=map(int,re.findall(r'\d+',close.get('bounds')))
        adb('shell','input','tap',str((x0+x1)//2),str((y0+y1)//2))
        print('Diálogo de System UI documentado y cerrado en QA.',flush=True)
    elif any(n.get('content-desc')=='1 de 6' or n.get('text')=='1 de 6'
             or n.get('content-desc')=='Ver tutorial' for n in nodes):
        break
    time.sleep(1)
else: raise RuntimeError('Android no publicó el tutorial ni el inicio normal.')
run('verificar_tutorial_normal.py',['--device',DEVICE,'--output','qa/audio-v3/normal-tutorial'],
    'normal-tutorial-ejecucion.log')
(OUT/'normal-tutorial/logs-normal-tutorial.txt').write_bytes(
    adb('logcat','-d','-v','threadtime','-s','flutter','AndroidRuntime'))
run('verificar_audio_normal.py',['--output','qa/audio-v3/normal-audio','--selecciones'],
    'normal-audio-ejecucion.log')
run('verificar_tarjetas_v3.py',['--output','qa/audio-v3/tarjetas-normal'],
    'tarjetas-normal-ejecucion.log')
print('Recorridos del APK normal completos.',flush=True)
