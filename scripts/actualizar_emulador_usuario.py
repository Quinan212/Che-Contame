"""Instala el APK normal preservando byte por byte el almacén local existente."""
from pathlib import Path
import argparse
import hashlib
import os
import subprocess
import time

root = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--output', default='qa/tutorial-guiado')
output = root / parser.parse_args().output
apk = output / 'che-preguntame-debug.apk'
assert apk.is_file()
adb_path = str(Path(os.environ['LOCALAPPDATA']) / 'Android/Sdk/platform-tools/adb.exe')
device = 'emulator-5554'
package = 'ar.contame.contame_android'
store = 'files/datastore/FlutterSharedPreferences.preferences_pb'


def adb(*args):
    return subprocess.run([adb_path, '-s', device, *args], check=True,
        capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW).stdout


assert b'Recorridos_API_36' in adb('emu', 'avd', 'name'), 'AVD de Alan no coincide; no instalar.'
adb('shell', 'input', 'keyevent', 'KEYCODE_HOME')
time.sleep(1)
adb('shell', 'am', 'force-stop', package)
before = adb('exec-out', 'run-as', package, 'cat', store)
assert before, 'No se pudo leer el almacén existente; no instalar.'
(output / 'preferencias-antes.pb').write_bytes(before)
adb('install', '-r', '-t', str(apk))
after = adb('exec-out', 'run-as', package, 'cat', store)
(output / 'preferencias-despues.pb').write_bytes(after)
assert before == after, 'El almacén cambió al instalar; revisar el respaldo antes de iniciar.'
adb('shell', 'am', 'start', '-n', f'{package}/.MainActivity')
message = ('APK normal de lib/main.dart instalado en emulator-5554.\n'
    'Almacén local conservado byte por byte; sesión y preferencias preservadas.\n'
    f'APK SHA256: {hashlib.sha256(apk.read_bytes()).hexdigest()}\n'
    f'Almacén SHA256: {hashlib.sha256(after).hexdigest()}\n')
(output / 'actualizacion-emulador.log').write_text(message, encoding='utf-8')
print('Versión normal instalada; datos existentes preservados.')
