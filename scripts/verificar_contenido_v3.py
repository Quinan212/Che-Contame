"""Revisa el APK normal de la nueva biblioteca únicamente en el AVD de QA."""
from pathlib import Path
import hashlib
import json
import os
import re
import subprocess
import time
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'qa/contenido-v3'
APK = OUT / 'che-preguntame-debug.apk'
ADB = str(Path(os.environ['LOCALAPPDATA']) / 'Android/Sdk/platform-tools/adb.exe')
DEVICE = 'emulator-5556'
PACKAGE = 'ar.contame.contame_android'


def adb(*args):
    return subprocess.run([ADB, '-s', DEVICE, *args], check=True, capture_output=True,
                          creationflags=subprocess.CREATE_NO_WINDOW, timeout=45).stdout


def snapshot(name):
    for attempt in range(6):
        try:
            adb('shell', 'uiautomator', 'dump', '/sdcard/contenido-v3.xml')
            raw = adb('exec-out', 'cat', '/sdcard/contenido-v3.xml')
            nodes = list(ET.fromstring(raw).iter('node'))
            break
        except (ET.ParseError, subprocess.CalledProcessError):
            if attempt == 5:
                raise
            time.sleep(.5)
    (OUT / f'{name}.xml').write_bytes(raw)
    (OUT / f'{name}.png').write_bytes(adb('exec-out', 'screencap', '-p'))
    return nodes


def label(node):
    return node.get('text', '') or node.get('content-desc', '')


def tap_node(node):
    x0, y0, x1, y1 = map(int, re.findall(r'\d+', node.get('bounds')))
    adb('shell', 'input', 'tap', str((x0 + x1) // 2), str((y0 + y1) // 2))
    time.sleep(.8)


def tap_text(text, name):
    for attempt in range(5):
        nodes = snapshot(f'{name}-buscar-{attempt}')
        match = next((node for node in nodes if label(node) == text), None)
        if match is None:
            match = next((node for node in nodes if text in label(node)), None)
        if match is not None:
            tap_node(match)
            return
        adb('shell', 'input', 'swipe', str(int(width * .95)), str(int(height * .85)),
            str(int(width * .95)), str(int(height * .35)), '400')
    raise AssertionError(f'No aparece el control {text}')


assert b'ChePreguntame_QA_API_36' in adb('emu', 'avd', 'name')
with zipfile.ZipFile(APK) as archive:
    data = json.loads(archive.read('assets/flutter_assets/assets/contenido/preguntas-base.json'))
    assert data['version'] == '0.3-historias-y-codigos'
    assert len(data['preguntas']) == 144 and len(data['consignas']) == 15
    assert archive.read('assets/flutter_assets/kernel_blob.bin'), 'APK normal debug requerido.'
dimensions = list(map(int, re.findall(r'\d+', adb('shell', 'wm', 'size').decode())))
width, height = dimensions[-2:]
adb('install', '-r', '-t', str(APK))
adb('shell', 'am', 'force-stop', PACKAGE)
adb('shell', 'settings', 'put', 'system', 'font_scale', '1.0')
adb('logcat', '-c')
adb('shell', 'am', 'start', '-n', f'{PACKAGE}/.MainActivity')
time.sleep(4)
nodes = snapshot('normal-portada')
for attempt in range(12):
    if any(label(node) == 'Comenzar' or 'Para arrancar' in label(node) or
           label(node) == 'Omitir' for node in nodes):
        break
    time.sleep(.5)
    nodes = snapshot(f'normal-apertura-espera-{attempt}')
if any(label(node) == 'Comenzar' for node in nodes):
    tap_text('Comenzar', 'normal-comenzar')
    time.sleep(4)
nodes = snapshot('normal-menu-inicial')
if any(label(node) == 'Omitir' for node in nodes):
    tap_text('Omitir', 'normal-omitir')
    time.sleep(1)
results = []
try:
    for level in data['niveles']:
        tap_text(level['nombre'], f"normal-nivel-{level['id']}")
        nodes = snapshot(f"normal-seleccion-{level['id']}")
        new_round = next((node for node in nodes if label(node) == 'Empezar otra ronda'), None)
        if new_round is not None:
            tap_node(new_round)
        else:
            button = next((label(node) for node in nodes if label(node) in
                           ('Dale, arranquemos', 'Seguir charlando')), 'Dale, arranquemos')
            tap_text(button, f"normal-empezar-{level['id']}")
        nodes = snapshot(f"normal-frente-{level['id']}")
        all_labels = '\n'.join(label(node) for node in nodes)
        card = next((card for card in data['preguntas'] if card['nivel'] == level['id']
                     and card['pregunta'] in all_labels), None)
        assert card is not None, f"Texto del nivel {level['id']} no coincide con el asset."
        tap_text('Una más', f"normal-girar-{level['id']}")
        nodes = snapshot(f"normal-reverso-{level['id']}")
        assert card['repregunta'] in '\n'.join(label(node) for node in nodes)
        tap_text('Volver a la carta', f"normal-volver-{level['id']}")
        if level['id'] == 3:
            adb('shell', 'settings', 'put', 'system', 'font_scale', '2.0')
            time.sleep(1)
            nodes = snapshot('normal-letra-grande-antes')
            scroll = next(node for node in nodes if node.get('class') ==
                          'android.widget.ScrollView' and node.get('scrollable') == 'true')
            x0, y0, x1, y1 = map(int, re.findall(r'\d+', scroll.get('bounds')))
            adb('shell', 'input', 'swipe', str((x0 + x1) // 2),
                str(y0 + (y1 - y0) * 3 // 4), str((x0 + x1) // 2),
                str(y0 + (y1 - y0) // 4), '500')
            nodes = snapshot('normal-letra-grande-desplazada')
            assert card['pregunta'] in '\n'.join(label(node) for node in nodes)
            adb('shell', 'settings', 'put', 'system', 'font_scale', '1.0')
            time.sleep(.5)
        results.append({'nivel': level['id'], 'id': card['id'], 'formato': card['formato'],
                        'frente_y_continuacion': True})
        tap_text('Elegir nivel', f"normal-menu-{level['id']}")
    logs = adb('logcat', '-d', '-v', 'threadtime', '-s', 'flutter', 'AndroidRuntime')
    (OUT / 'normal-android.log').write_bytes(logs)
    assert not any(error in logs for error in
                   [b'FATAL EXCEPTION', b'RenderFlex overflowed', b'EXCEPTION CAUGHT'])
    result = {'passed': True, 'version': data['version'], 'cartas': 159,
              'apk_sha256': hashlib.sha256(APK.read_bytes()).hexdigest(),
              'niveles': results, 'letra_grande': True, 'device': DEVICE}
    (OUT / 'normal-resultado.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n',
                                             encoding='utf-8')
    print('APK normal aprobado: biblioteca nueva, tres niveles, ambas caras y letra grande.')
finally:
    adb('shell', 'settings', 'put', 'system', 'font_scale', '1.0')
