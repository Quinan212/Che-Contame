"""Gestos Android sobre el APK normal: reloj real y video del tutorial.

Requiere un emulador QA con el APK de lib/main.dart instalado y el tutorial
abierto en el paso 1. No borra datos ni instala el ejecutable de integración.
"""
from pathlib import Path
import argparse
import os
import re
import subprocess
import time
import xml.etree.ElementTree as ET

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--device', default='emulator-5556')
parser.add_argument('--output', type=Path, default=Path('qa/tutorial-guiado'))
options = parser.parse_args()
if options.device == 'emulator-5554':
    parser.error('Usar el emulador de QA separado, no el de Alan.')
root = Path(__file__).resolve().parents[1]
output = root / options.output
output.mkdir(parents=True, exist_ok=True)
adb_path = str(Path(os.environ['LOCALAPPDATA']) / 'Android/Sdk/platform-tools/adb.exe')
hidden = subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
events = []

def adb(*args):
    return subprocess.run([adb_path, '-s', options.device, *args],
        capture_output=True, check=True, creationflags=hidden).stdout

def bounds(node):
    return tuple(map(int, re.findall(r'\d+', node.get('bounds'))))

def snapshot(name):
    for attempt in range(3):
        try:
            adb('shell', 'uiautomator', 'dump', '/sdcard/tutorial-qa.xml')
            break
        except subprocess.CalledProcessError:
            if attempt == 2:
                raise
            events.append(f'Lectura de interfaz reintentada: {name}')
            time.sleep(.4)
    raw = adb('exec-out', 'cat', '/sdcard/tutorial-qa.xml')
    (output / f'{name}.xml').write_bytes(raw)
    (output / f'{name}.png').write_bytes(adb('exec-out', 'screencap', '-p'))
    nodes = list(ET.fromstring(raw).iter('node'))
    return {n.get('text') or n.get('content-desc'): n for n in nodes
        if n.get('text') or n.get('content-desc')}

def tap(nodes, label, pausa=.6):
    x0, y0, x1, y1 = bounds(nodes[label])
    events.append(f'{time.monotonic() - start:.3f}s toque {label}')
    adb('shell', 'input', 'tap', str((x0 + x1)//2), str((y0 + y1)//2))
    time.sleep(pausa)

def swipe(dx, duration):
    events.append(f'{time.monotonic() - start:.3f}s arrastre {dx}px / {duration}ms')
    adb('shell', 'input', 'swipe', str(cx), str(cy), str(cx + dx), str(cy), str(duration))
    time.sleep(.7)

start = time.monotonic()
nodes = snapshot('normal-inicial')
if '1 de 6' not in nodes:
    if 'Omitir' in nodes:
        tap(nodes, 'Omitir')
        nodes = snapshot('normal-inicio')
    tap(nodes, 'Ver tutorial')
    nodes = snapshot('normal-tutorial-01')
    # La capa de bienvenida puede seguir visible aunque Android ya publique
    # la semántica del inicio. Esperar y volver a intentar abrir, sin tocar datos.
    for _ in range(3):
        if '1 de 6' in nodes:
            break
        time.sleep(1)
        tap(nodes, 'Ver tutorial')
        nodes = snapshot('normal-tutorial-01')
assert '1 de 6' in nodes, 'Abrir el tutorial en el paso 1 antes de ejecutar.'
remote = f'/sdcard/tutorial-normal-{int(time.time())}.mp4'
recording = subprocess.Popen([adb_path, '-s', options.device, 'shell',
    'screenrecord', '--time-limit', '60', remote], stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL, creationflags=hidden)
start = time.monotonic()
try:
    tap(nodes, 'Siguiente')
    nodes = snapshot('normal-tutorial-02')
    assert '2 de 6' in nodes
    assert 'Una más' not in nodes and 'Esta la paso' not in nodes
    avance = bounds(nodes['Otra carta'])
    card_label = next(label for label in nodes if label.startswith('Tarjeta '))
    x0, y0, x1, y1 = bounds(nodes[card_label])
    cx, cy = (x0+x1)//2, (y0+y1)//2
    # Los tres toques ocurren en la misma explicación y durante una sola salida.
    for _ in range(3):
        tap(nodes, 'Otra carta', pausa=.02)
    time.sleep(1.6)
    nodes = snapshot('normal-tutorial-03')
    assert '3 de 6' in nodes and '2 de 3' in nodes
    assert 'CIERRE · EJEMPLO' not in nodes
    assert bounds(nodes['Otra carta']) == avance
    swipe(-100, 800) # Corto y lento: retorno físico.
    nodes = snapshot('normal-tutorial-03-retorno')
    assert '2 de 3' in nodes and '3 de 6' in nodes
    assert any('Así vuelve' in label for label in nodes)
    assert bounds(nodes['Otra carta']) == avance
    swipe(-450, 600)
    time.sleep(1.0)
    nodes = snapshot('normal-tutorial-04')
    assert '4 de 6' in nodes and '3 de 3' in nodes
    assert 'Otra carta' not in nodes and 'Esta la paso' not in nodes
    tap(nodes, 'Una más')
    time.sleep(1.0)
    nodes = snapshot('normal-tutorial-05')
    assert '5 de 6' in nodes
    assert any('reverso' in label for label in nodes)
    assert 'Otra carta' not in nodes and 'Una más' not in nodes
    tap(nodes, 'Esta la paso')
    time.sleep(1.0)
    nodes = snapshot('normal-tutorial-06')
    assert 'CIERRE · EJEMPLO' in nodes and '6 de 6' in nodes
    assert 'Donde más se quedaron' not in nodes and 'Tiempo activo' not in nodes
    tap(nodes, '¡A charlar!')
    nodes = snapshot('normal-tutorial-07-inicio')
    assert 'Hay mucho\npor contar.' in nodes or '¿Por dónde arrancamos?' in nodes
    events.append('Recorrido normal aprobado: tres toques producen una carta, retorno indica sin avanzar, gesto/giro/pasar continúan automáticamente y cierre compacto.')
finally:
    (output / 'tutorial-normal.log').write_text('\n'.join(events), encoding='utf-8')
    recording.wait(timeout=60)
    adb('pull', remote, str(output / 'tutorial-reloj-normal.mp4'))
print(events[-1])
