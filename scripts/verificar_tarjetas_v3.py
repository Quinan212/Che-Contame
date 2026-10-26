"""Colores y cuatro variantes con entradas reales sobre el APK normal, solo en QA."""
from pathlib import Path
import argparse,io,json,os,re,subprocess,time,xml.etree.ElementTree as ET
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output',default='qa/audio-v3/tarjetas-normal')
OUT=ROOT/parser.parse_args().output;OUT.mkdir(parents=True,exist_ok=True)
ADB=str(Path(os.environ['LOCALAPPDATA'])/'Android/Sdk/platform-tools/adb.exe')
DEVICE='emulator-5556';PACKAGE='ar.contame.contame_android'
palette=re.search(r'coloresCartas = \[(.*?)\];',
    (ROOT/'lib/tema/tema_contame.dart').read_text(encoding='utf-8'),re.S).group(1)
COLORS=[tuple(int(value[i:i+2],16) for i in (0,2,4))
    for value in re.findall(r'Color\(0xFF([0-9A-Fa-f]{6})\)',palette)]

def adb(*args):
    return subprocess.run([ADB,'-s',DEVICE,*args],check=True,capture_output=True,
                          creationflags=subprocess.CREATE_NO_WINDOW).stdout

def snapshot(name):
    for attempt in range(5):
        raw=adb('shell','uiautomator','dump','/sdcard/tarjetas-v3.xml')
        if b'dumped' in raw: break
        time.sleep(.5)
    xml=adb('exec-out','cat','/sdcard/tarjetas-v3.xml')
    png=adb('exec-out','screencap','-p')
    (OUT/f'{name}.xml').write_bytes(xml);(OUT/f'{name}.png').write_bytes(png)
    nodes={n.get('text') or n.get('content-desc'):n for n in ET.fromstring(xml).iter('node')
           if n.get('text') or n.get('content-desc')}
    return nodes,Image.open(io.BytesIO(png)).convert('RGB')

def bounds(node): return tuple(map(int,re.findall(r'\d+',node.get('bounds'))))
def tap(node):
    x0,y0,x1,y1=bounds(node);adb('shell','input','tap',str((x0+x1)//2),str((y0+y1)//2));time.sleep(.8)
def dominant(nodes,image):
    label=next(s for s in nodes if s.startswith('Tarjeta '))
    x0,y0,x1,y1=bounds(nodes[label])
    image=image.crop((x0+20,y0+20,x1-20,y1-20))
    return max(image.getcolors(image.width*image.height),key=lambda c:c[0])[1]

assert b'ChePreguntame_QA_API_36' in adb('emu','avd','name')
nodes,image=snapshot('00-inicio')
if 'Comenzar' in nodes:
    tap(nodes['Comenzar']);time.sleep(3);nodes,image=snapshot('00-menu')
if 'Activar sonidos' in nodes:
    tap(nodes['Activar sonidos']);nodes,image=snapshot('00-sonido')
for _ in range(6):
    if 'Otra carta' in nodes: break
    label=next((s for s in nodes if s in ('Dale, arranquemos','Seguir charlando')),None)
    if label: tap(nodes[label]);nodes,image=snapshot('01-partida');break
    adb('shell','input','swipe','540','1800','540','600','400')
    nodes,image=snapshot('00-inicio-desplazado')
assert 'Otra carta' in nodes
if 'Una más' in nodes:
    color=dominant(nodes,image)
    tap(nodes['Una más']);nodes,image=snapshot('02-reverso')
    assert dominant(nodes,image)==color
    tap(nodes['Volver a la carta']);nodes,image=snapshot('03-frente')
    assert dominant(nodes,image)==color
adb('logcat','-c')
seen=[]
for i in range(5):
    nodes,image=snapshot(f'carta-{i+1}')
    color=dominant(nodes,image);assert color in COLORS,color
    seen.append(color)
    tap(nodes['Otra carta'])
assert len(set(seen[:4]))==4 and seen[0]==seen[4],seen
raw=adb('logcat','-d','-v','threadtime','-s','flutter','AndroidRuntime')
(OUT/'logs-variantes.txt').write_bytes(raw)
variants=list(map(int,re.findall(rb'AUDIO-VARIANTE:carta:([1-4])',raw)))
assert len(variants)==5 and len(set(variants[:4]))==4 and variants[0]==variants[4],variants
assert all(a!=b for a,b in zip(variants,variants[1:]))
time.sleep(1.3)
silent=adb('shell','dumpsys','media.audio_flinger')
(OUT/'audioflinger-reposo.txt').write_bytes(silent)
pid=adb('shell','pidof',PACKAGE).strip().split()[0]
assert not re.search(rb'S\s+\d+\s+yes\s+'+pid+rb'/',silent)
(OUT/'resultado.json').write_text(json.dumps(dict(passed=True,colors=seen,variants=variants,
    no_audio_when_idle=True),indent=2),encoding='utf-8')
print('Tarjetas normales aprobadas: cuatro colores, cuatro variantes sin repetición y silencio en reposo.')
