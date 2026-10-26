"""Prueba nativa aislada y evidencias reales mediante Flutter y el ADB del SDK."""
from pathlib import Path
import argparse
import os
import re
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]
SDK = Path(os.environ.get('ANDROID_HOME', Path(os.environ['LOCALAPPDATA']) / 'Android' / 'Sdk'))
ADB = str(SDK / 'platform-tools' / 'adb.exe')
FLUTTER = str(Path(os.environ['USERPROFILE']) / 'flutter' / 'bin' / 'flutter.bat')
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--device', default='emulator-5556', help='Emulador dedicado a QA. No usar el que está probando una persona.')
parser.add_argument('--output', type=Path, default=Path('qa/mazo'), help='Carpeta para las evidencias de este recorrido.')
parser.add_argument('--target', default='integration_test/experiencia_android_test.dart')
options = parser.parse_args()
DEVICE = options.device
if DEVICE == 'emulator-5554':
    parser.error('El emulador de Alan se reserva para la app normal; usar QA.')
OUTPUT = ROOT / options.output
OUTPUT.mkdir(parents=True, exist_ok=True)
hidden = subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0

def adb(*args):
    return subprocess.run([ADB, '-s', DEVICE, *args], capture_output=True, check=True, creationflags=hidden)

recording = None
captured = set()
audio_captured = False
stages_captured = set()
remote_video = f'/sdcard/che-mazo-{int(time.time())}.mp4'
command = [FLUTTER, 'drive', '--driver=test_driver/experiencia_android.dart',
           '--target='+options.target, '-d', DEVICE, '--debug']
process = subprocess.Popen(command, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                           encoding='utf-8', errors='replace', creationflags=hidden)
with (OUTPUT / 'integracion-android.log').open('w', encoding='utf-8') as log:
    for line in process.stdout:
        log.write(line)
        log.flush()
        if 'AUDIO-CONTAME:bienvenida' in line and not audio_captured:
            (OUTPUT / 'audioflinger-reproduccion.txt').write_bytes(
                adb('shell', 'dumpsys', 'media.audio_flinger').stdout)
            audio_captured = True
        for stage in ('comenzar', 'entradaInicio'):
            if f'AUDIO-CONTAME:{stage}' in line and stage not in stages_captured:
                (OUTPUT / f'audioflinger-{stage}.txt').write_bytes(
                    adb('shell', 'dumpsys', 'media.audio_flinger').stdout)
                stages_captured.add(stage)
        if 'QA-AUDIO-REPOSO' in line:
            silent = adb('shell', 'dumpsys', 'media.audio_flinger').stdout
            (OUTPUT / 'audioflinger-reposo.txt').write_bytes(silent)
            app_pid = adb('shell', 'pidof', 'ar.contame.contame_android').stdout.strip().split()[0]
            assert not re.search(rb'S\s+\d+\s+yes\s+'+app_pid+rb'/', silent), 'Quedó audio activo en reposo'
        match = re.search(r'QA-CAPTURA:([a-z0-9-]+)', line)
        if match:
            name = match.group(1)
            if name in captured:
                continue
            captured.add(name)
            if recording is None:
                recording = subprocess.Popen([ADB, '-s', DEVICE, 'shell', 'screenrecord', '--time-limit', '60', remote_video],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=hidden)
            png = adb('exec-out', 'screencap', '-p').stdout
            (OUTPUT / f'{name}.png').write_bytes(png)
            print(f'Captura Android: {name}', flush=True)
        if 'All tests passed' in line or 'Failure' in line or 'Exception' in line:
            print(line.strip(), flush=True)
code = process.wait()
(OUTPUT / 'logs-android.txt').write_bytes(
    adb('logcat', '-d', '-v', 'threadtime', '-s', 'flutter', 'AndroidRuntime', 'SoundPool').stdout)
if recording is not None:
    recording.wait(timeout=60)
    adb('pull', remote_video, str(OUTPUT / 'transiciones-android.mp4'))
print(f'Prueba Android: código {code}', flush=True)
raise SystemExit(code)
