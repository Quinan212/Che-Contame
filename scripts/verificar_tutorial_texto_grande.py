"""Recorrido manual nativo 320×640 dp, texto 2: navegación y objetivo accesibles.

Ejecutar después del recorrido normal, con el APK normal en el emulador QA.
Restaura tamaño, densidad y escala del emulador al terminar; no borra datos.
"""
from pathlib import Path
import os
import re
import subprocess
import time
import xml.etree.ElementTree as ET

device = 'emulator-5556'
root = Path(__file__).resolve().parents[1]
output = root / 'qa/tutorial-guiado/texto-grande'
output.mkdir(parents=True, exist_ok=True)
adb_path = str(Path(os.environ['LOCALAPPDATA']) / 'Android/Sdk/platform-tools/adb.exe')
hidden = subprocess.CREATE_NO_WINDOW


def adb(*args):
    return subprocess.run([adb_path, '-s', device, *args], check=True,
        capture_output=True, creationflags=hidden).stdout


def snapshot(name):
    adb('shell', 'uiautomator', 'dump', '/sdcard/tutorial-grande.xml')
    raw = adb('exec-out', 'cat', '/sdcard/tutorial-grande.xml')
    (output / f'{name}.xml').write_bytes(raw)
    (output / f'{name}.png').write_bytes(adb('exec-out', 'screencap', '-p'))
    return {n.get('text') or n.get('content-desc'): n
        for n in ET.fromstring(raw).iter('node')
        if n.get('text') or n.get('content-desc')}


def area(node):
    return tuple(map(int, re.findall(r'\d+', node.get('bounds'))))


def tap(nodes, label, alto=1680):
    x0, y0, x1, y1 = area(nodes[label])
    assert 0 <= y0 < y1 <= alto, (label, nodes[label].get('bounds'))
    adb('shell', 'input', 'tap', str((x0+x1)//2), str((y0+y1)//2))
    time.sleep(.8)


try:
    # Abrir antes de reducir la pantalla: el acceso de inicio tiene scroll.
    nodes = snapshot('inicio')
    for _ in range(4):
        if 'Ver tutorial' in nodes or '1 de 6' in nodes:
            break
        time.sleep(1)
        nodes = snapshot('inicio')
    if '1 de 6' not in nodes:
        tap(nodes, 'Ver tutorial', alto=2400)
    adb('shell', 'wm', 'size', '840x1680')
    adb('shell', 'wm', 'density', '420')
    adb('shell', 'settings', 'put', 'system', 'font_scale', '2.0')
    time.sleep(1.0)
    for paso in range(1, 7):
        nodes = snapshot(f'paso-{paso}')
        assert f'{paso} de 6' in nodes
        siguiente = '¡A charlar!' if paso == 6 else 'Siguiente'
        assert siguiente in nodes and 'Omitir' in nodes
        if paso in (2, 3, 4, 5):
            accion = 'Otra carta' if paso < 4 else 'Una más' if paso == 4 else 'Esta la paso'
            assert accion in nodes
            _, _, _, y1 = area(nodes[accion])
            _, yguia, _, _ = area(nodes['Paso anterior'])
            assert y1 < yguia, (accion, y1, yguia)
        if paso == 4:
            # Leer la explicación por su scroll propio sin mover la navegación.
            antes = area(nodes['Siguiente'])
            adb('shell', 'input', 'swipe', '420', '1260', '420', '1100', '550')
            time.sleep(.6)
            nodes = snapshot('paso-4-lectura')
            assert area(nodes['Siguiente']) == antes
        if paso == 6:
            for _ in range(6):
                if ('Compartidas' in nodes and 'Pasadas' in nodes
                        and area(nodes['Compartidas'])[0] == area(nodes['Pasadas'])[0]):
                    break
                adb('shell', 'input', 'swipe', '420', '760', '420', '350', '550')
                time.sleep(.5)
                nodes = snapshot('paso-6-conteos')
            assert 'Compartidas' in nodes and 'Pasadas' in nodes
            assert area(nodes['Compartidas'])[0] == area(nodes['Pasadas'])[0], 'Con texto grande, los conteos deben apilarse.'
        tap(nodes, siguiente)
    (output / 'resultado.log').write_text(
        'Recorrido 320×640 dp / texto 2 aprobado: seis pasos, acción accesible y navegación separada.\n',
        encoding='utf-8')
    print('Texto grande: recorrido aprobado.')
finally:
    adb('shell', 'settings', 'put', 'system', 'font_scale', '1.0')
    adb('shell', 'wm', 'size', 'reset')
    adb('shell', 'wm', 'density', 'reset')
