"""Pops y deslizamiento originales: síntesis FM y ruido filtrado, sin samples."""
raise SystemExit(
    'Generador histórico retirado: no debe sobrescribir la biblioteca moderna. '
    'Usar sound-design/produccion_v1.py y el proyecto CONTAME_AUDIO_v1.rpp.'
)
import math
import random
from pathlib import Path
import struct
import wave

RATE = 44100
ROOT = Path(__file__).resolve().parents[1] / 'assets' / 'sonidos'
ROOT.mkdir(parents=True, exist_ok=True)


def pop(t, duration, frequency, end, elastic=0.18):
    if t < 0 or t >= duration:
        return 0.0
    u = t / duration
    # Ataque redondo, descenso elástico de tono y cola sin discontinuidad.
    attack = min(1.0, t / 0.005)
    tail = math.cos(u * math.pi / 2) ** 2
    envelope = attack * tail * math.exp(-2.2 * u)
    phase = 2 * math.pi * (end * t + (frequency - end) * duration * (1 - math.exp(-5 * u)) / 5)
    bend = elastic * math.sin(2 * math.pi * 3 * u) * math.exp(-5 * u)
    fm = 0.55 * math.sin(phase * 2) * math.exp(-8 * u)
    return envelope * (math.sin(phase + fm + bend) + 0.12 * math.sin(phase / 2))


sounds = {
    'toque': (0.060, [(0, 620, 440, 0.12)]),
    'seleccion': (0.100, [(0, 540, 650, 0.15)]),
    # Los niveles bajan de registro con la profundidad. Las rondas responden
    # con dos / tres notas: se distinguen también por ritmo, no solo por tono.
    'nivelSuave': (0.100, [(0, 880, 740, 0.12)]),
    'nivelMedio': (0.110, [(0, 660, 550, 0.18)]),
    'nivelProfundo': (0.130, [(0, 440, 330, 0.24)]),
    'rondaCorta': (0.150, [(0, 660, 700, 0.12), (0.065, 880, 920, 0.12)]),
    'rondaLarga': (0.200, [(0, 440, 480, 0.12), (0.065, 660, 700, 0.12), (0.130, 880, 920, 0.12)]),
    'carta': (0.160, [(0, 350, 570, 0.30)]),
    'giro': (0.180, [(0, 480, 260, 0.22), (0.065, 310, 580, 0.20)]),
    'pasar': (0.140, [(0, 490, 290, 0.14)]),
    'bienvenida': (0.400, [(0, 330, 360, 0.18), (0.100, 440, 480, 0.18), (0.220, 660, 700, 0.18)]),
    'cierre': (0.600, [(0, 392, 415, 0.16), (0.100, 494, 520, 0.16), (0.220, 587, 620, 0.16), (0.340, 784, 810, 0.16)]),
}


def guardar(name, samples):
    peak = max(abs(s) for s in samples) or 1
    pcm = b''.join(struct.pack('<h', round(s / peak * 0.72 * 32767)) for s in samples)
    with wave.open(str(ROOT / (name + '.wav')), 'wb') as output:
        output.setnchannels(1)
        output.setsampwidth(2)
        output.setframerate(RATE)
        output.writeframes(pcm)
    print(f'{name}: {round(len(samples) / RATE * 1000)} ms')


for name, (duration, voices) in sounds.items():
    samples = []
    for i in range(round(duration * RATE)):
        t = i / RATE
        value = sum(pop(t - start, min(duration - start, 0.26), f, end, elastic)
                    for start, f, end, elastic in voices)
        value *= min(1, (duration - t) / 0.008)
        samples.append(value)
    guardar(name, samples)

# Swish corto, sin golpe ni siseo agudo sostenido. El ruido de banda limitada
# recorre el mismo gesto que el tono redondo de la familia de pops.
duration = .210
noise = random.Random(20261001)
fast = slow = 0.0
samples = []
for i in range(round(duration * RATE)):
    t = i / RATE
    u = t / duration
    white = noise.uniform(-1, 1)
    cutoff = 850 + 1900 * math.sin(math.pi * u)
    fast += (1 - math.exp(-2 * math.pi * cutoff / RATE)) * (white - fast)
    slow += (1 - math.exp(-2 * math.pi * 280 / RATE)) * (white - slow)
    envelope = math.sin(math.pi * u) ** 2
    samples.append(.85 * envelope * (fast - slow)
                   + .08 * pop(t, duration, 420, 280, .12))
guardar('deslizamiento', samples)
