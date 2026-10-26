# Tutorial · transiciones por etapas · 2 de octubre de 2026

El tutorial adopta el lenguaje de la apertura v6: recorte vertical y desplazamiento corto desde arriba, sobre textura celeste estacionaria. Se elimina el fundido lateral de la ruta anterior.

- La transición dura 900 ms. El menú se retira durante los primeros 270 ms; desde los 216 ms se revelan encabezado, práctica y guía, en ese orden. El solapamiento breve evita una pantalla vacía.
- Al completar, omitir o usar Atrás, el mismo reloj recorre las etapas en sentido inverso. El menú vuelve por grupos. Sus selecciones y desplazamiento se conservan.
- El fondo y las esquinas pertenecen a la pantalla inicial y permanecen dibujados. La práctica no agrega otra textura ni vuelve a trazar las esquinas. Si se abre desde una pantalla sin ese fondo compartido, utiliza un fondo estacionario del mismo estilo.
- Los recortes conservan las medidas finales de la práctica y la burbuja; no cambian alturas, posiciones del mazo ni áreas de los controles. El foco difuminado y sus aberturas siguen las superficies reales.
- La práctica y los controles de navegación se habilitan al terminar la entrada. El sonido del encabezado conserva su posición y no requiere otro botón flotante.
- Cada acción aceptada emite su efecto existente una vez. El tutorial automático de primera visita conserva la excepción sin señal adicional. La continuación automática entre pasos sigue esperando un segundo de reposo y permanece silenciosa.
- Las transiciones de las cartas, el giro, el arrastre y el foco mantienen sus funciones. La pista pendiente y la continuación se cancelan al salir; no pueden sonar sobre la salida.
- Segundo plano suspende el reloj de la ruta. Al volver continúa desde el punto pausado. Movimiento reducido muestra los estados completos sin recorridos.

No se modifican imágenes, WAV, contenido, almacenamiento, sesión real ni preferencias. Catálogo sonoro vigente: `docs/apertura-v5/catalogo-activo.json`. Evidencias: `qa/tutorial-transiciones/`.
