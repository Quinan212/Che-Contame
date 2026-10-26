# Contame · Guía sonora v1 · Moderno suave

Referencia aprobada para la biblioteca actual y los sonidos que se agreguen después.
Fecha de entrega: 2 de octubre de 2026.

## Paleta

Usar tonos digitales redondos, clicks amortiguados y barridos breves filtrados.
ReaSynth aporta el motivo preciso; Small-SFX aporta una textura propia a cada acción.
Mantener ataques de 3–6 ms y colas de 25–45 ms, una base cercana a Re mayor y
matices cromáticos discretos en navegación. Evitar estridencia y resonancias largas.
No usar madera, papel realista, voces, música de fondo, retro, alarmas ni castigos.
Pasar es neutral: su gesto sonoro permite cambiar de tema con tranquilidad.

## Diferenciación

Una acción conserva siempre el mismo archivo en partida, tutorial y laboratorio.
Las acciones distintas tienen motivos, articulaciones, ritmo y textura propios.
No crear variaciones que cambien únicamente volumen o altura. Evaluar la forma de
onda, el espectro y la envolvente temporal; verificar también que la señal coincida
con su intención. La correlación espectral es un filtro técnico, no una prueba de
preferencia de escucha.

Ejemplos de identidad: bienvenida (apertura), carta (barrido y asentamiento), giro y
volverCarta (contornos opuestos), pasar (salida neutral), cierre (resolución breve).

## Niveles y formato

WAV PCM de 16 bits, mono, 44,1 kHz. RMS sobre la parte activa: −20 dBFS ±1,5 dB.
Pico máximo: −6 dBFS. La región activa corresponde a una envolvente de potencia de
5 ms superior a −35 dB respecto de su máximo. Quitar DC y silencio inicial innecesario;
aplicar fundidos de entrada de 2 ms y salida de 8 ms como mínimo. Conjunto menor a 2 MB.
En esta versión: 529.594 bytes; RMS entre −20,001 y −20,000; pico máximo −7,058 dBFS.
La app reproduce a 0,40 y la pista de arrastre a 0,32 para acompañar la conversación.

## Mapa de acciones

| Archivo | Acción | Carácter | Duración |
|---|---|---|---|
| bienvenida.wav | Primera entrada | Tres destellos redondos que abren espacio | 450 ms |
| cierre.wav | Cierre de ronda | Resolución descendente y cola suave | 600 ms |
| nivelSuave.wav | Nivel suave | Punto claro de ataque ligero | 120 ms |
| nivelMedio.wav | Nivel medio | Dos apoyos equilibrados | 150 ms |
| nivelProfundo.wav | Nivel profundo | Base grave con apoyo superior | 180 ms |
| rondaCorta.wav | Ronda de 12 | Dos pulsos compactos | 180 ms |
| rondaLarga.wav | Ronda de 25 | Tres pulsos con curva ascendente propia | 240 ms |
| iniciarRonda.wav | Iniciar | Apertura ascendente con notas superpuestas | 260 ms |
| retomarRonda.wav | Retomar | Dos notas que vuelven al centro | 180 ms |
| otraRonda.wav | Otra ronda | Giro tonal de reinicio | 220 ms |
| abrirConsignas.wav | Entrar a consignas | Acento curioso en dos notas | 160 ms |
| abrirTutorial.wav | Entrar al tutorial | Salto suave que invita a practicar | 180 ms |
| abrirLaboratorio.wav | Entrar al laboratorio | Tres notas exploratorias breves | 200 ms |
| carta.wav | Otra carta | Barrido digital y asentamiento tonal al final | 360 ms |
| giro.wav | Mostrar repregunta | Contorno ascendente de tres notas | 300 ms |
| volverCarta.wav | Volver al frente | Contorno descendente con otra articulación | 280 ms |
| pasar.wav | Pasar | Salida lateral neutral con dos apoyos del mismo registro | 260 ms |
| deslizamiento.wav | Pista del tutorial | Aire filtrado sin golpe final | 210 ms |
| abrirAyuda.wav | Abrir ayuda | Dos notas superpuestas que abren | 160 ms |
| cerrarAyuda.wav | Cerrar ayuda | Cierre pequeño y amortiguado | 120 ms |
| volverInicio.wav | Volver al inicio | Dos notas cortas de retorno | 140 ms |
| tutorialSiguiente.wav | Siguiente | Punto claro y compacto | 100 ms |
| tutorialAnterior.wav | Anterior | Punto bajo con ataque y textura distintos | 100 ms |
| tutorialOmitir.wav | Omitir | Salida discreta con cola más larga | 120 ms |
| tutorialCompletar.wav | Completar tutorial | Resolución ascendente de preparación | 280 ms |
| activarSonido.wav | Activar sonido | Destello redondo con apoyo superpuesto | 120 ms |
| activarVibracion.wav | Activar vibración | Dos pulsos de tacto suave | 100 ms |
| desactivarVibracion.wav | Desactivar vibración | Dos apoyos de descenso discreto | 100 ms |
| reintentar.wav | Reintentar | Doble pulso neutral de recuperación | 120 ms |

## Producción y continuidad

El lote usa Small-SFX con CUDA y media precisión, una carga del modelo, 87 candidatos
(tres por efecto), semillas fijas, dos segundos por fuente y ocho pasos. El modelo y
su repositorio están identificados en catalogo.json. La selección automática valora
un factor de cresta cercano a 3 y poca energía por encima de 4,5 kHz. seleccion.json
conserva los tres puntajes, la fuente, el punto de recorte y el candidato elegido.

CONTAME_AUDIO_v1.rpp es el maestro real de REAPER 7.81: cuatro pistas, motivos MIDI
editables con ReaSynth y 29 regiones nombradas. Las capas están en texturas/ con rutas
relativas. Se puede abrir y editar sin cargar el modelo. REAPER renderiza las regiones
en mono a 44,1 kHz y 24 bits; el acabado conserva RMS activo, fundidos y PCM16 final.
finales/ contiene las exportaciones que se usan en la app. originales/ conserva los
13 WAV anteriores y el generador histórico, fuera de los assets activos.

Para repetir el lote, usar produccion_v1.py por fases: init → generate → prepare.
Abrir Montar_REAPER.lua en REAPER y renderizar las 29 regiones del maestro; luego
ejecutar finish y auditar_v1.py. Cada fase conserva las fuentes y la selección.
El generador histórico de la app queda bloqueado. Una revisión de estilo futura
debe abrir otra versión, preservando este maestro y su catálogo.

## Comportamiento en la app

Emitir solo después de aceptar la acción, una vez. Botón y gesto equivalentes usan
el mismo evento. Una nueva señal reemplaza la anterior, sin detener los otros
reproductores precargados. Silenciar corta inmediatamente y queda en silencio.
Segundo plano suspende el audio; volver al primer plano no repite señales.

No emitir por scroll, gestos cancelados, controles bloqueados o avances automáticos
del tutorial. Bienvenida mantiene la condición de primera entrada. Sonido y vibración
siguen siendo preferencias independientes; los controles nuevos de navegación y
ajustes no agregan vibración. De ayuda al tutorial se oye una única apertura del
tutorial; cerrar ayuda por botón, arrastre o Atrás produce el mismo cierre.

## Evidencias

qa/audio-v1/mediciones.csv y mediciones.json contienen las medidas y huellas de cada
archivo. formas-de-onda.png, espectros.png y ritmos.png muestran las diferencias.
QA_AUDIO.md contiene la verificación funcional y Android. La escucha del anfitrión
se dejó desactivada en QA para permitir que Alan siga usando el equipo; se verificó
reproducción nativa con SoundPool y AudioFlinger. La evaluación subjetiva de timbre
puede hacerse con los WAV o con la app instalada.
