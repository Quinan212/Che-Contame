# Apertura con sonido sincronizado · versión 3

La animación conserva la secuencia aprobada y sus 4.600 ms. Esta edición acompaña la retirada del logo y el ascenso de Comenzar, y da una llegada propia al menú. La pausa central no contiene audio.

| Desde el toque | Imagen | Sonido |
|---|---|---|
| 0–550 ms | Se retiran logo y frase. | Inicio redondo y breve, con dos voces mezcladas. |
| 550–1.350 ms | Comenzar sube al centro. | Ascenso tonal ligado y moderado, sin escala de pitidos. |
| 1.350–1.700 ms | Desaparece el botón. | El ascenso se apaga progresivamente. |
| 1.700–3.700 ms | Pausa sobre el fondo. | Silencio completo. |
| 3.700–4.600 ms | El menú sube desde abajo. | Acorde abierto que se asienta suavemente. |

`comenzar.wav` dura 1.700 ms y contiene la primera etapa completa. `entradaInicio.wav` dura 900 ms. El segundo efecto se dispara desde el reloj de la animación al llegar a 3.700 ms, una sola vez; no usa una espera independiente. No cambia la señal de bienvenida al aparecer Comenzar, las variantes de las tarjetas ni los demás controles.

El diseño continúa la biblioteca alegre y cercana: cuerpo tonal cálido, ataques redondeados, articulación ligada. Sin ruido de fondo, percusión, voces ni reverberación. Se reutilizó el perfil armónico medido de una fuente Small-SFX previamente generada en CUDA; los nuevos arreglos usan resíntesis controlada y montaje/exportación en REAPER. No hubo nueva inferencia del modelo. La elección entre tres candidatos por etapa se basa en el contorno, los niveles y la continuidad; queda pendiente la valoración subjetiva de Alan al escucharlos.

La biblioteca activa tiene 31 señales y 43 WAV, con 1.874.378 bytes. Los 41 WAV previos ajenos a Comenzar permanecen idénticos. Formato PCM16, mono, 44.100 Hz; RMS activo −20 dBFS y picos −10,71 dBFS para Comenzar y −9,20 dBFS para la llegada. Los clips tienen fundidos breves y terminan en cero.

Silenciar interrumpe el audio activo y suprime las etapas pendientes. Reactivar no reproduce una etapa que ya pasó. Segundo plano detiene el audio y pausa la animación; al regresar, las etapas aún pendientes siguen el reloj reanudado sin repetir las anteriores. Movimiento reducido conserva dos segundos tras el toque y emite la llegada cuando aparece el menú. Sonido y vibración siguen siendo independientes; esta secuencia no agrega vibraciones. La guía de primera visita abre sin otra señal automática.

El proyecto editable y las fuentes están en `../../../sound-design/apertura-v3/TRANSICION_INICIO.rpp`. El respaldo de Comenzar anterior está fuera de los assets activos, en `../../../sound-design/apertura-v3/respaldo/`. Las semillas originales, recetas, candidatos y mediciones quedan en [catalogo.json](catalogo.json); el catálogo completo está en [catalogo-activo.json](catalogo-activo.json).

La vista previa con audio combina la grabación de pantalla de Android con los WAV exportados, sincronizados con las etapas. No representa una captura del audio del dispositivo: Android `screenrecord` genera video silencioso. La reproducción nativa se verifica por separado en Android y en las evidencias de AudioFlinger. Ver `../../qa/apertura-v3/QA.md`.
