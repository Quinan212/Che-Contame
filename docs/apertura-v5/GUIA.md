# Apertura cálida · versión 5

Pedido de Alan: dos bienvenidas de la misma familia, con tonos diferentes. La señal al tocar Comenzar debe recordar una apertura de sistema cuidada, conservando la calidez social de la app. El ascenso continuo anterior se percibía como caricatura.

Esta edición cambia solamente `bienvenida.wav` y `comenzar.wav`. No modifica la animación, el catálogo de cartas ni el comportamiento del reproductor. La bienvenida termina antes de habilitar Comenzar. La señal de llegada del menú se conserva.

| Señal | Arreglo | Duración |
|---|---|---|
| Aparición de Comenzar | Firma luminosa, con F4 y entrada solapada de C5/A4. Ataques de 50 ms, sin golpes ni pitidos separados. | 520 ms |
| Toque en Comenzar | Apertura más asentada: base F3/C4, G4 breve y resolución suave hacia A4/F4. Ataques de 100 ms y colas amortiguadas. | 1.700 ms |
| Llegada del menú | La firma cálida existente, sin cambios de archivo. | 900 ms |

Cada voz mantiene una frecuencia fija. La evolución proviene de la entrada y salida de notas distintas, no de deslizar su afinación. Las dos firmas comparten la familia tonal de Fa y el perfil armónico cálido, pero difieren en registro, ritmo, voicing y envolvente. La referencia a un sistema operativo describe el carácter; no se copia ninguna firma comercial.

Sin fuentes de ruido, percusión, reverberación, vibrato o cambios continuos de tono. Los parciales superiores de la firma larga se atenúan más para obtener una apertura menos brillante y más asentada. La valoración auditiva final corresponde a Alan; las mediciones comprueban formato, nivel y diferencias entre archivos.

La portada mantiene al menos dos segundos en primer plano. El botón aparece durante 550 ms y después admite el toque. Desde ese toque: logo/frase se retiran en 550 ms, el botón sube hasta el centro entre 550 y 1.350 ms y desaparece hasta 1.700 ms. Hay 150 ms de silencio; el menú opaco sube desde abajo entre 1.850 y 2.750 ms, acompañado por su llegada existente. Movimiento reducido conserva las funciones y presenta el menú a los 1.700 ms, sin traslados.

Se mantienen precarga prioritaria de cuatro fuentes, una emisión por etapa, independencia de sonido y vibración, detención al silenciar y suspensión en segundo plano. No se repiten etapas consumidas ni se añade otra señal al tutorial de primera visita.

PCM16, mono, 44.100 Hz; RMS activo −20 dBFS. Picos seleccionados: bienvenida −11,87 dBFS; Comenzar −9,39 dBFS, por debajo del límite de −6 dBFS. Fundidos breves, extremos en cero. Catálogo completo: 31 señales y 43 WAV únicos, 1.836.452 bytes. Los otros 41 WAV mantienen sus hashes.

Tres candidatos por efecto, cinco pistas y siete regiones editables, incluida la llegada conservada. Fuentes relativas y respaldo de ambos WAV de la versión 4 en `../../../sound-design/apertura-v5/`. Proyecto: `TRANSICION_INICIO.rpp`. Se reutiliza el perfil armónico de una fuente Small-SFX producida previamente en CUDA; esta edición usa resíntesis y arreglos nuevos en REAPER, sin nueva inferencia. Semilla, perfil, recetas y mediciones en [catalogo.json](catalogo.json); biblioteca completa en [catalogo-activo.json](catalogo-activo.json).

Los productores históricos quedan protegidos contra la sobrescritura de esta edición. Para regenerar la v5: `crear_apertura_sobria.py prepare`, `renderizar_apertura_sobria.ps1` y `crear_apertura_sobria.py finish`. REAPER se ejecuta con configuración separada y en segundo plano.

La vista previa une pantalla real de Android con WAV exportados; la grabación de pantalla original no recoge audio. La reproducción nativa se verifica aparte. Evidencias: [QA](../../qa/apertura-v5/QA.md).
