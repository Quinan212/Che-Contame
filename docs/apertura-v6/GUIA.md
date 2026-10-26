# Apertura con revelación progresiva · versión 6

Pedido de Alan: quitar las formas de las esquinas de la portada y hacer que ingresen al menú como si se dibujaran. La interfaz debe aparecer de arriba hacia abajo, con el mismo movimiento suave, evitando que el fondo vuelva a entrar junto con toda la pantalla.

La textura celeste ocupa una sola capa persistente desde la portada hasta el menú. Se muestra la región central libre de adornos del recurso existente, mediante un encuadre de pintado; el archivo original no se edita. Las dos formas curvas y sus tres marcas se trazan por separado en Flutter, siguiendo el contorno y la paleta anteriores. La portada contiene únicamente textura, logo, frase, Comenzar y el control de sonido.

La salida del logo y el recorrido de Comenzar al centro mantienen sus tiempos. Después de los 150 ms de respiro, el menú se revela por grupos sobre esa misma textura: encabezado, título y descripción, niveles, duración, botón principal y accesos inferiores. Cada grupo conserva su espacio de layout, se descubre con un recorte vertical y recorre 14 dp desde arriba; no hay otro fondo que suba por detrás ni un fundido de pantalla completa.

| Desde el toque | Presentación |
|---|---|
| 0–550 ms | Retirada del logo y la frase. |
| 550–1.350 ms | Comenzar sube al centro real. |
| 1.350–1.700 ms | Desaparece Comenzar. |
| 1.700–1.850 ms | Respiro de 150 ms sobre la textura limpia. |
| 1.850–2.750 ms | Revelación de arriba hacia abajo de la interfaz y dibujo progresivo de las esquinas. |

Dentro de los 900 ms finales, el encabezado termina en 423 ms. Los grupos del cuerpo entran de manera escalonada, desde 90 ms hasta completar los accesos inferiores a los 900 ms. La forma superior termina en 630 ms; la inferior recorre de izquierda a derecha entre 216 y 900 ms. Las tres marcas se trazan con punta redonda entre 405 y 882 ms.

El control de sonido de la portada se desplaza suavemente a su posición final del encabezado durante los primeros 315 ms de la revelación y sigue disponible durante toda la transición. Ayuda se revela después, entre 315 y 585 ms, evitando cruzarse con ese recorrido. El control equivalente del menú conserva su espacio, oculto hasta el relevo final, evitando dos íconos simultáneos. Los demás controles, el scroll y la semántica del menú se habilitan al finalizar. Los estados de carga y error también se revelan, evitando filtrar contenido del menú en la portada.

Un solo reloj coordina sonido, fondo y grupos. Se pausa en segundo plano y no se reinicia al elegir nivel, volver de una partida ni terminar de cargar datos. Movimiento reducido presenta el menú completo al concluir los 1.700 ms de Comenzar, sin recorridos ni trazado gradual. La guía automática conserva su condición de primera visita y no añade otro efecto.

Los 43 WAV y el contenido de las cartas permanecen idénticos a la entrega anterior. Se mantienen las dos firmas distintas de [apertura v5](../apertura-v5/GUIA.md), los niveles normalizados y la llegada de 900 ms al comenzar la revelación. No hay producción musical ni generación de audio en esta revisión.

Pruebas, video de la app normal, vista previa con WAV exportados, mediciones y entrega en [QA](../../qa/apertura-v6/QA.md).
