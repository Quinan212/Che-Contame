# Paleta verde y naranja · 2 de octubre de 2026

> Referencia histórica. La paleta actual compartida con el video está documentada en [paleta-estilo-video-v11](../paleta-estilo-video-v11/GUIA.md).

Dirección solicitada por Alan: sustituir celeste y azul por una familia verde con naranja. Mantener la cercanía y la identidad de Che, preguntame.

| Uso | Color |
|---|---|
| Textos, iconos, burbuja y adornos oscuros | Bosque #16392A |
| Texto secundario | Verde apagado #52684D |
| Acciones principales y marcas | Naranja luminoso #F5660A |
| Enlaces y texto naranja pequeño | Naranja de lectura #9E3D06 |
| Selección | Salvia #CDDFBF |
| Fondo base | Salvia muy clara #E9F2DF |
| Paneles y ayuda | Crema verde #F5F8ED |
| Bordes | Verde #A8BE9B |
| Cartas, ciclo de cuatro | #EDF2D9, #FFEAD2, #DBEACF, #FFF4DE |

Las esquinas usan un gradiente salvia #D7E4CE → #C5D6B8 → #BED0B2. El logo conserva su forma, con bosque y el mismo naranja luminoso. El fondo conserva su textura: ambos se colorean al pintar en Flutter, sin modificar los archivos originales. Las marcas naranjas usan el color central de acciones. La apertura Android usa salvia y un símbolo bosque de un solo color, con los originales raster conservados.

Revisión de Alan: naranja más claro, intenso y luminoso, manteniendo los verdes aprobados. Las acciones grandes conservan letras blancas (3,09:1 con etiquetas de 24–25 dp); las etiquetas pequeñas sobre naranja usan verde oscuro #0E2D20 (4,80:1). El tutorial y el aviso Pasada usan ese contraste oscuro; los switches conservan el pulgar blanco. Los enlaces pequeños usan un naranja de lectura más oscuro (4,77:1 sobre selección salvia). Referencia vigente: `qa/naranja-luminoso/contraste.json`; las mediciones anteriores quedan en `qa/paleta-verde-naranja/`.

Usar los nombres semánticos de `TemaContame`; no introducir celeste, azul, rosa o violeta en nuevas superficies. Los errores pueden conservar su significado específico. No alterar las transiciones, los cuatro colores de cartas en rotación, el contenido ni el audio para aplicar la paleta.

Ajuste posterior solicitado por Alan: el botón principal del menú, «Dale, arranquemos» / «Seguir charlando», conserva letras y flecha blancas. Su etiqueta de 23 dp usa peso 700 para contraste de texto grande sobre el naranja luminoso; no cambia el tamaño, la posición ni el tiempo de las animaciones. Evidencia: `qa/naranja-luminoso-v2/`.
