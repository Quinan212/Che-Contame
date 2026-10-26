# Apertura con Comenzar · versión 1

Dirección solicitada por Alan el 2 de octubre de 2026: mantener la presentación durante dos segundos, hacer aparecer un botón animado y entrar mediante un toque, con sonido adecuado a la app.

## Secuencia

1. Mostrar fondo, logo y «Una pregunta. Muchas historias.». Fundido del logo: 420 ms.
2. Mantener la portada durante 2 segundos de uso en primer plano. La preparación del sonido ocurre en paralelo y no retrasa la presentación.
3. Aparecer «Comenzar» en 450 ms con fundido y ascenso corto. El espacio ya está reservado: el logo no se desplaza. Emitir `bienvenida` una sola vez cuando comienza esta aparición, si Sonidos está activo.
4. Esperar indefinidamente el toque. El menú queda fuera del área táctil y del lector de pantalla mientras la portada lo cubre.
5. Al confirmar Comenzar, deshabilitar la acción, emitir `comenzar` una vez y fundir la portada en 320 ms. Ir al menú; conservar la guía de primera visita para quien todavía no la vio, sin añadir una segunda señal de apertura de tutorial.

Movimiento reducido mantiene los dos segundos, presenta el botón directamente y omite desplazamientos y el fundido de salida. Segundo plano suspende la espera y las animaciones y detiene el audio. Al volver se continúa donde se estaba, sin repetir la bienvenida. Silenciar actúa inmediatamente y conserva la preferencia; no hay vibración en esta entrada.

## Sonido

Se conserva la guía v3 alegre y coqueta, limpia y ligera. `bienvenida.wav` (950 ms) mantiene su exportación y pasa a acompañar la aparición del botón en cada apertura. `comenzar.wav` (520 ms) añade un acorde suave con una respuesta ascendente. No incluye percusión, barridos de ruido, fondo, voces ni reverberación.

El nuevo arreglo usa un perfil armónico medido de una fuente Small-SFX generada anteriormente en GPU. No se hizo otra inferencia ni se copió un efecto terminado. Se compararon tres arreglos de 480, 520 y 580 ms; se eligió el segundo por el acorde inicial y la respuesta breve. Fuentes, notas, tiempos, ganancias, perfil y semilla original están en `catalogo.json`.

`catalogo-activo.json` reúne las 42 exportaciones vigentes, incluyendo la base v3 y esta extensión; `catalogo.json` conserva las tres propuestas de Comenzar y su procedencia.

Proyecto editable con tres regiones y tres pistas: `../../../sound-design/apertura-v1/APERTURA.rpp`. Las rutas de fuentes del proyecto son relativas. La fuente IA original permanece en la biblioteca de producción v3.

| Exportación | Formato | RMS activo | Pico | Tamaño |
|---|---|---|---|---|
| comenzar.wav | PCM16, mono, 44.100 Hz, 520 ms | −20,00 dBFS | −9,99 dBFS | 45.908 bytes |

Se aplican fundidos de 5/35 ms y se conserva el volumen de reproducción 0,32. Biblioteca activa ampliada: 30 acciones, 42 WAV y 1.690.878 bytes. Los 41 WAV existentes se conservan byte por byte. La extensión se puede reconstruir con `producir_apertura.py prepare`, `renderizar_apertura.ps1` y `producir_apertura.py finish`; el render ocurre en REAPER en segundo plano.
