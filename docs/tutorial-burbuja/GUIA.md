# Tutorial · burbuja anclada al objetivo · 2 de octubre de 2026

La explicación deja de ocupar un pie fijo. Flota en el espacio libre inmediatamente debajo de las superficies visibles que el usuario necesita, con margen para el puntero y sin cubrir el control activo.

- En niveles y resumen sube hasta el contenido; en las acciones de las cartas baja junto a sus controles.
- Al enseñar Una más y Pasar, se desplaza también hacia el lado del botón. El puntero se calcula desde su posición real, acompañando el desplazamiento de la burbuja.
- El movimiento dura 420 ms con `easeInOutCubic`. El texto nuevo se revela desde arriba durante los primeros 210 ms. Si dos pasos usan el mismo objetivo, cambia la explicación con ese revelado, sin inventar un desplazamiento innecesario.
- La posición se calcula a partir de las superficies medidas, el área visible de práctica, el tamaño de pantalla y el texto del sistema. Se limita a la pantalla y conserva lectura interna por desplazamiento.
- La práctica mantiene sus medidas. La burbuja queda quieta durante arrastre, rebote del botón, giro, resultado y espera de continuación; vuelve a calcular su destino al cambiar de paso. Las variaciones menores a 0,1 dp se descartan.
- Durante el recorrido se bloquean los toques sobre práctica y burbuja. La pista del deslizamiento espera a que la explicación termine de asentarse y conserva su demora de 900 ms. El avance automático continúa esperando un segundo de reposo y no añade sonido.
- Segundo plano suspende el movimiento y su lectura; movimiento reducido coloca la burbuja directamente en el destino y muestra el texto completo.

Se mantienen fondo, entrada/salida de la ruta, foco difuminado, tarjeta, sonidos y preferencias. Esta revisión reemplaza la posición fija de la explicación de las versiones anteriores. Evidencias: `qa/tutorial-burbuja/`.
