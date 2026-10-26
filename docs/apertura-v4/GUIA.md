# Apertura fluida · versión 4

Corrección pedida por Alan: acortar el fondo vacío después de desaparecer Comenzar y separar el motivo breve «titití» del ascenso «uuu». El guiño acompaña la aparición del botón; al tocarlo suena únicamente el ascenso ligado.

La portada conserva los dos segundos iniciales. `bienvenida.wav` contiene el motivo breve de 520 ms, trasladado desde el comienzo del arreglo anterior. El botón aparece durante 550 ms y después acepta el toque: el motivo ya terminó. Con movimiento reducido se muestra directamente, conservando esa breve protección antes de admitir el toque. Sonido y segundo plano siguen sujetos a las preferencias.

La precarga prepara primero bienvenida, comenzar, llegada y activar sonido. El resto continúa en lotes de cuatro, sin bloquear estos efectos. La aparición espera únicamente esas fuentes iniciales si Android todavía las está preparando; el reproductor de cada acción espera su propia fuente, no toda la biblioteca. Así se evita que una bienvenida demorada quede en la cola y se corte al tocar Comenzar. La espera inicial sigue siendo de al menos dos segundos en primer plano.

| Desde el toque | Imagen | Sonido |
|---|---|---|
| 0–550 ms | Logo y frase se retiran. | Arranca el ascenso ligado, sin el motivo breve anterior. |
| 550–1.350 ms | Comenzar sube al centro. | Continúa la misma curva tonal. |
| 1.350–1.700 ms | Desaparece el botón. | Se apaga suavemente el ascenso. |
| 1.700–1.850 ms | Respiro breve sobre el fondo. | Silencio, 150 ms. |
| 1.850–2.750 ms | El menú sube y se asienta. | Llegada cálida existente, 900 ms. |

La secuencia tras el toque pasa de 4.600 a 2.750 ms. Se mantienen las curvas, la subida al centro real y la entrada opaca del menú desde abajo. La pausa vacía baja de dos segundos a 150 ms. Movimiento reducido muestra el menú después del ascenso sonoro de 1.700 ms, sin desplazamientos.

`comenzar.wav` conserva una duración de 1.700 ms, ahora con dos voces ligadas desde el comienzo y sin el motivo de aparición. `entradaInicio.wav` permanece idéntico; su disparo pasa a 1.850 ms y usa el mismo reloj visual. Una etapa silenciada no se repite al reactivar; segundo plano pausa el reloj y detiene el reproductor. No se añaden vibraciones ni señales extra al abrir la guía de primera visita.

Los botones principales que emiten un efecto propio o reciben feedback externo omiten el clic automático de Android. Comenzar produce su ascenso sonoro una vez por toque aceptado.

La biblioteca conserva 31 señales y 43 WAV: 1.836.452 bytes. Se actualizan solamente bienvenida y comenzar; los otros 41 archivos conservan sus hashes. PCM16 mono 44.100 Hz, RMS activo −20 dBFS. Picos: bienvenida −11,85 dBFS y comenzar −10,94 dBFS. Sin fuentes de ruido, percusión ni reverberación. No se generó material nuevo con el modelo: el perfil armónico Small-SFX previamente obtenido en CUDA se reutiliza en los nuevos arreglos de REAPER.

Tres candidatos por efecto, siete regiones editables incluyendo la llegada conservada, fuentes relativas y respaldo de los dos WAV anteriores en `../../../sound-design/apertura-v4/`. Proyecto: `TRANSICION_INICIO.rpp`. Recetas, semillas de origen y mediciones en [catalogo.json](catalogo.json); biblioteca completa en [catalogo-activo.json](catalogo-activo.json). Los generadores históricos no pueden sobrescribir esta biblioteca.

La vista previa muestra la apertura completa, incluyendo el motivo de aparición antes del clic. Combina pantalla real de Android con WAV exportados; la grabación de pantalla original no recoge audio. La reproducción nativa se comprueba aparte. Evidencias en `../../qa/apertura-v4/QA.md`.
