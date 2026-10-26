# Contame · Guía sonora v3 · Alegre y coqueto

Esta guía documenta la base de 41 exportaciones. La apertura sincronizada añade
dos señales y dos exportaciones: biblioteca vigente de 31 señales, 43 WAV y
1.836.452 bytes. Ver [extensión de apertura](../apertura-v4/GUIA.md) y su catálogo activo.

Dirección elegida por Alan: más alegría y juego, sin el ruido de fondo ni los
ataques de cuerda que recordaban tambores en v2. Colores y variantes para tarjetas.

## Paleta

Resonancias redondas, pequeñas curvas melódicas y guiños armónicos, con entradas
suaves de 35–65 ms. No percusión, madera, cuerdas pulsadas, barridos de ruido,
aire de fondo, reverberación, voces, música de fondo, retro ni tonos telefónicos.
La alegría viene del contorno y ritmo, no de golpes fuertes o agudos punzantes.
Pasar sigue siendo neutral. Silencio real entre gestos; no hay una pista ambiental.

## Producción

Small-SFX produce tres perfiles por exportación con una carga de CUDA. Se analiza
una región activa y se elige el candidato con más cuerpo armónico útil. La señal
final se reconstruye con esos armónicos y envolventes controladas: no se copia el
residuo de ruido, las percusiones ni el fondo de las fuentes generadas. Las fuentes
originales y el perfil medido se conservan para reproducibilidad. REAPER compone
las voces en pistas editables, con 41 regiones nombradas. El generador histórico
de la app sigue retirado. La escucha de Alan define la preferencia artística.

## Variantes y comportamiento

29 acciones semánticas, 41 WAV. Otra carta, giro, volver al frente y pasar tienen
cuatro versiones propias cada uno; rotan 1→2→3→4 sin repetir seguidas. Solo avanza
la variante cuando se reproduce una acción aceptada; silenciar, gestos cancelados
y solicitudes sustituidas en la cola no consumen una variante. La misma familia
se usa en partida, tutorial y laboratorio. El resto conserva un efecto por acción.
Volumen de app 0,32; pista de movimiento 0,20. Sin vibraciones nuevas.

## Colores de las tarjetas

Rosa #FCEBF2, durazno #FFF0DF, lila #F0EBFF y celeste #E4F3FD, opacos. Alternan por
posición en el mazo; ambas caras y la instantánea saliente conservan el color de la
misma carta. Las cartas de atrás muestran el color que tendrán al pasar al frente.
Texto azul profundo; el color no transmite reglas ni sustituye etiquetas.

## Exportación y control

WAV PCM16 mono 44,1 kHz; RMS activo −20 dBFS ±1,5; pico ≤−6 dBFS; conjunto <2 MB.
Fundidos 5/35 ms. Sin valores inválidos, clipping, duplicados ni colas de ruido.
Regeneración: init → generate → prepare → REAPER → finish → install.
Conservar v1, v2 y las propuestas previas fuera de los assets activos.

## Resultado medido

41 WAV, 1,644,970 bytes; RMS activo −20 dBFS; pico máximo -8.866 dBFS.
76 pruebas e integración Android aprobadas; informe en qa/audio-v3/QA_AUDIO.md.
La rotación se reinicia al crear una nueva instancia del reproductor; no agrega preferencias persistentes.
