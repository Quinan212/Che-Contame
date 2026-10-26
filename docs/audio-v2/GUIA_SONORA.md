# Contame · Guía sonora v2 · Cálido social, íntimo y relajado

Revisión a partir de la escucha de Alan: la v1 resultaba corta, robótica y telefónica.
La nueva dirección busca cercanía, curiosidad y una invitación tranquila a conversar.
Alan eligió “Más íntimos y relajados” al escuchar las cuatro muestras iniciales:
menos rebote y brillo, pausas naturales y resonancias más apagadas.
La intención emocional es una hipótesis creativa que se comprueba escuchando en la app.

## Materiales y articulación

Resonancias suaves de cuerda pulsada y amortiguada, cuerpo elástico redondo y gestos
de aire cepillado. Ataques de tacto, pequeñas irregularidades naturales y colas
suaves que respiran. Sin pitidos de oscilador, llamadas, alarmas, tonos de teléfono,
voces, risas grabadas, público, madera/papel realista, música de fondo ni estética retro.
La textura generada es el cuerpo principal; no se oculta debajo de un tono digital.

Bienvenida, inicio y cierre usan pequeños gestos espaciados de pregunta y respuesta. Los
controles frecuentes son breves pero tienen cuerpo; las cartas dejan una resonancia
más larga. Pasar sigue siendo neutral. Evitar fanfarrias, premios y castigos.

## Duración y funcionamiento

Bienvenida 1,10 s; cierre 1,35 s; cartas 0,43–0,58 s; inicio 0,72 s; completar 0,82 s.
Los controles menores duran 0,21–0,39 s. No estirar los archivos v1: se generan nuevas
fuentes. Las colas no cambian las animaciones ni bloquean el siguiente gesto. Una
nueva acción reemplaza el audio anterior; silenciar y segundo plano lo detienen.
Un archivo fijo por acción, compartido entre partida, tutorial y laboratorio.

## Producción y nivel

Tres candidatos Small-SFX en GPU por efecto, una carga por lote, semillas fijas.
Prioridad baja de CPU y pausas entre candidatos para compartir el equipo.
Seleccionar textura con cuerpo medio, armónicos y poco brillo agudo; el puntaje
automático penaliza señales casi sinusoidales, pero no sustituye la preferencia humana.
REAPER monta cuerpo y aire con pulsos, alturas, volúmenes y fundidos editables.
Las selecciones de ronda aíslan granos de 180 ms, con dos/tres apoyos y sin capa
de aire para no agregar ataques accidentales de la fuente generada.
Normalizar WAV PCM16 mono 44,1 kHz a −20 dBFS RMS activo ±1,5 dB; pico ≤−6 dBFS.
Fundidos de entrada de 5 ms y salida de 35 ms; inicio audible antes de 25 ms.
Mantener los 29 assets por debajo de 2 MB. Conservar v1 y fuentes v2 fuera de assets.

## Catálogo

| Acción | Duración | Intención |
|---|---|---|
| bienvenida | 1100 ms | Una invitación que recibe y deja espacio |
| cierre | 1350 ms | Un cierre agradecido y tranquilo |
| nivelSuave | 240 ms | Un toque liviano y cercano |
| nivelMedio | 290 ms | Dos apoyos relajados |
| nivelProfundo | 360 ms | Un apoyo más asentado |
| rondaCorta | 360 ms | Dos pulsos que invitan a empezar |
| rondaLarga | 490 ms | Tres pulsos con espacio entre ellos |
| iniciarRonda | 720 ms | Abrir la conversación con calma |
| retomarRonda | 550 ms | Reencontrarse con la charla |
| otraRonda | 660 ms | Dar continuidad al encuentro |
| abrirConsignas | 460 ms | Un pequeño gesto de curiosidad |
| abrirTutorial | 560 ms | Invitar a probar con confianza |
| abrirLaboratorio | 590 ms | Un gesto tranquilo de exploración |
| carta | 580 ms | Un movimiento que abre otro tema |
| giro | 500 ms | Un giro curioso que invita a profundizar |
| volverCarta | 460 ms | Un regreso relajado al tema |
| pasar | 430 ms | Dejar ir el tema con naturalidad |
| deslizamiento | 330 ms | Una sugerencia ligera de movimiento |
| abrirAyuda | 390 ms | Abrir un espacio de acompañamiento |
| cerrarAyuda | 220 ms | Un cierre pequeño y amable |
| volverInicio | 340 ms | Un retorno familiar |
| tutorialSiguiente | 210 ms | Un avance liviano |
| tutorialAnterior | 230 ms | Un paso atrás sin reproche |
| tutorialOmitir | 280 ms | Una salida sin presión |
| tutorialCompletar | 820 ms | Quedar listos para conversar |
| activarSonido | 340 ms | Una confirmación que se abre |
| activarVibracion | 230 ms | Dos pequeños apoyos de tacto |
| desactivarVibracion | 250 ms | Un apoyo que se apaga |
| reintentar | 310 ms | Dar otra oportunidad con calma |

Regeneración: init → generate → prepare → render en REAPER → finish → install. La fase install es explícita; generar o revisar muestras no sobrescribe la app.

## Resultado medido

29 WAV, 1,205,206 bytes; RMS activo −20 dBFS; pico máximo -6.339 dBFS.
QA técnica en qa/audio-v2/QA_AUDIO.md. La valoración del carácter requiere escucha.
