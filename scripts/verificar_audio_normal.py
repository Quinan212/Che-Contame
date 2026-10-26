"""Mute, regreso del segundo plano y movimiento reducido en el APK normal QA."""
from pathlib import Path
import argparse, os, re, subprocess, time, xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output',default='qa/audio-v1/normal-audio')
parser.add_argument('--selecciones',action='store_true',help='Comprobar las dos duraciones de ronda en el inicio.')
options=parser.parse_args()
OUT=ROOT/options.output
OUT.mkdir(parents=True,exist_ok=True)
ADB=str(Path(os.environ['LOCALAPPDATA'])/'Android/Sdk/platform-tools/adb.exe')
DEVICE='emulator-5556'
PACKAGE='ar.contame.contame_android'
HIDDEN=subprocess.CREATE_NO_WINDOW
events=[]
def adb(*args):
    return subprocess.run([ADB,'-s',DEVICE,*args],capture_output=True,check=True,
        creationflags=HIDDEN).stdout
def snapshot(name):
    for attempt in range(5):
        result=adb('shell','uiautomator','dump','/sdcard/audio-normal.xml')
        if b'dumped' in result: break
        time.sleep(.5)
    else: raise RuntimeError('Android no publicó la interfaz')
    raw=adb('exec-out','cat','/sdcard/audio-normal.xml')
    (OUT/f'{name}.xml').write_bytes(raw)
    (OUT/f'{name}.png').write_bytes(adb('exec-out','screencap','-p'))
    nodes={n.get('text') or n.get('content-desc'): n for n in ET.fromstring(raw).iter('node')
           if n.get('text') or n.get('content-desc')}
    return nodes
def point(node):
    x0,y0,x1,y1=map(int,re.findall(r'\d+',node.get('bounds')))
    return str((x0+x1)//2),str((y0+y1)//2)
def tap(node,wait=.6):
    adb('shell','input','tap',*point(node));time.sleep(wait)
def audio_log():
    raw=adb('logcat','-d','-v','threadtime','-s','flutter','AndroidRuntime')
    return raw.decode('utf-8',errors='replace')
def start_round(nodes):
    if 'Otra carta' in nodes and 'Una más' in nodes:
        return snapshot('02-partida')
    for _ in range(5):
        label=next((s for s in nodes if s in ('Dale, arranquemos','Seguir charlando')),None)
        if label: tap(nodes[label]);return snapshot('02-partida')
        scroll=next(n for n in nodes.values() if n.get('scrollable')=='true') if any(n.get('scrollable')=='true' for n in nodes.values()) else None
        if scroll:
            x0,y0,x1,y1=map(int,re.findall(r'\d+',scroll.get('bounds')))
        else: x0,y0,x1,y1=0,300,1080,2100
        adb('shell','input','swipe',str((x0+x1)//2),str(y1-100),str((x0+x1)//2),str(y0+100),'400')
        nodes=snapshot('01-inicio-desplazado')
    raise RuntimeError('No apareció el botón de inicio')

initial_scale=adb('shell','settings','get','global','animator_duration_scale').decode().strip()
try:
    nodes=snapshot('00-inicio')
    if 'Activar sonidos' in nodes:
        tap(nodes['Activar sonidos']);nodes=snapshot('01-sonido-activo')
    if options.selecciones:
        for _ in range(5):
            if '12 cartas' in nodes and '25 cartas' in nodes: break
            adb('shell','input','swipe','540','500','540','1700','450')
            nodes=snapshot('01-selecciones-visibles')
        assert '12 cartas' in nodes and '25 cartas' in nodes
        adb('logcat','-c')
        for label in ['25 cartas','12 cartas']:
            tap(nodes[label],wait=.75)
            nodes=snapshot('01-ronda-'+label.split()[0])
        log=audio_log()
        assert log.count('AUDIO-CONTAME:rondaCorta')==1
        assert log.count('AUDIO-CONTAME:rondaLarga')==1
        (OUT/'logs-selecciones.txt').write_text(log,encoding='utf-8')
        events.append('APK normal actualizado: ronda corta y larga se reproducen una vez cada una.')
    nodes=start_round(nodes)
    assert 'Una más' in nodes and 'Silenciar sonidos' in nodes
    adb('logcat','-c')
    # Coordenadas observadas: el encabezado permanece fijo mientras gira la carta.
    tap(nodes['Una más'],wait=0)
    tap(nodes['Silenciar sonidos'],wait=.1)
    muted=snapshot('03-silenciado')
    assert 'Activar sonidos' in muted
    adb('logcat','-c')
    tap(muted['Otra carta'])
    assert 'AUDIO-CONTAME:' not in audio_log(), 'Una acción emitió audio estando silenciada'
    events.append('Silenciar durante giro y avanzar silenciado: ningún audio posterior.')
    (OUT/'audioflinger-silencio.txt').write_bytes(adb('shell','dumpsys','media.audio_flinger'))
    nodes=snapshot('04-carta-silenciosa')
    tap(nodes['Activar sonidos'])
    assert audio_log().count('AUDIO-CONTAME:activarSonido')==1
    nodes=snapshot('05-reactivado')
    adb('logcat','-c')
    tap(nodes['Otra carta'],wait=0)
    adb('shell','input','keyevent','KEYCODE_HOME')
    time.sleep(.2)
    (OUT/'audioflinger-segundo-plano.txt').write_bytes(adb('shell','dumpsys','media.audio_flinger'))
    snapshot('06-segundo-plano')
    # Esperar el cambio de foco Android antes de evaluar pistas activas.
    settled=adb('shell','dumpsys','media.audio_flinger')
    (OUT/'audioflinger-segundo-plano-estable.txt').write_bytes(settled)
    process=adb('shell','pidof',PACKAGE).strip().split()[0]
    assert not re.search(rb'S\s+\d+\s+yes\s+'+process+rb'/',settled)
    adb('logcat','-c')
    adb('shell','am','start','-n',PACKAGE+'/.MainActivity')
    time.sleep(.6)
    assert 'AUDIO-CONTAME:' not in audio_log(), 'Volver al primer plano repitió un audio'
    events.append('Segundo plano durante cambio de carta: el audio se suspende y no se repite al volver.')
    nodes=snapshot('07-regreso')
    assert any(s.startswith('Tarjeta ') and 'reverso' not in s for s in nodes)
    adb('shell','settings','put','global','animator_duration_scale','0')
    time.sleep(.5)
    adb('logcat','-c')
    tap(nodes['Una más'])
    nodes=snapshot('08-reducido-reverso')
    assert 'Volver a la carta' in nodes
    tap(nodes['Volver a la carta'])
    nodes=snapshot('09-reducido-frente')
    assert 'Una más' in nodes
    log=audio_log()
    assert log.count('AUDIO-CONTAME:giro')==1 and log.count('AUDIO-CONTAME:volverCarta')==1
    events.append('Movimiento reducido: ambas caras funcionan y cada giro emite exactamente su efecto.')
    (OUT/'logs-normal-audio.txt').write_text(log,encoding='utf-8')
finally:
    adb('shell','settings','put','global','animator_duration_scale',initial_scale)
    (OUT/'recorrido.log').write_text('\n'.join(events)+'\n',encoding='utf-8')
print('Recorrido de audio normal aprobado.')
