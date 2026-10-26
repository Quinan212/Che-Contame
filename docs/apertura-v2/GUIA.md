# Apertura por etapas · versión 2

Dirección de Alan del 2 de octubre de 2026: al tocar Comenzar, retirar primero el logo y los demás textos, subir el botón al centro y hacerlo desaparecer. Esperar unos dos segundos y traer la pantalla principal desde un lado, con un movimiento del mismo estilo.

La presentación conserva los dos segundos iniciales y la aparición de Comenzar. Después del toque, la secuencia dura 4.600 ms:

| Desde el toque | Movimiento |
|---|---|
| 0–550 ms | Logo y frase suben 56 dp y se retiran suavemente. |
| 550–1.350 ms | Comenzar sube desde su posición real hasta el centro de la pantalla. Conserva el naranja. |
| 1.350–1.700 ms | Comenzar desaparece en el centro. |
| 1.700–3.700 ms | Pausa de dos segundos sobre el mismo fondo. |
| 3.700–4.600 ms | La pantalla principal completa sube desde abajo y se asienta. No se desvanece. |

Las curvas usan `easeInOutCubic`. El centro se calcula con las dimensiones reales del botón y la pantalla; la posición no depende de una altura fija. El espacio inicial reservado mantiene quieto el logo al mostrar el botón. Durante la salida se bloquean nuevos toques y el desplazamiento de la portada. El menú queda fuera del lector de pantalla y de la interacción hasta terminar de entrar. El control de sonido permanece disponible.

Segundo plano pausa todas las etapas, incluida la espera; al regresar se continúa sin repetir el sonido ni la entrada. Movimiento reducido omite los desplazamientos y conserva una pausa de dos segundos después del toque. La primera visita sigue abriendo la guía una vez que termina esta entrada, sin duplicar la señal del toque.

El sonido y su volumen se conservan: bienvenida al presentar el botón y comenzar al confirmar el toque, sujetos a preferencias y sin vibración. Las 42 exportaciones permanecen idénticas a la versión 1. El catálogo, las mediciones y el proyecto editable del sonido están en [la guía anterior](../apertura-v1/GUIA.md).

Verificación y grabación del resultado en `../../qa/apertura-v2/QA.md`.
