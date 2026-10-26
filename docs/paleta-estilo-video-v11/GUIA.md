# Colores compartidos con el video v11

Alan pidió trasladar únicamente los colores de la presentación a la app. El video permanece en v11. La app conserva la geometría del logo, sus recursos originales, textura, Outfit, tamaños, posiciones, botones, gestos, transiciones, sonido, contenido y persistencia.

| Uso | Color |
|---|---|
| Fondo | Crema #F5F2E8 |
| Texto, iconos y ayuda | Verde #2A6047 |
| Texto secundario y etiquetas de cartas | Verde #385447 |
| Selección | Salvia #D9E7D6 |
| Paneles | Crema #FFF9EE |
| Acciones y marcas | Naranja #EE6B26 |
| Letras del logo y símbolo Android | Verde #2D6B4D |
| Burbuja naranja del logo | Naranja #FF7900 |
| Tarjetas en rotación | #D7E8B1, #FFE0B2, #CDE9D8, #FCE7AF |

Los gradientes de las esquinas usan #E4EDDE → #D9E7D6 → #CDDCC8; los bordes, #ADC4AB. Los colores de fondo, texto, selección, naranja y tarjetas provienen directamente de la composición del video. Los otros tonos son variantes para los roles de interfaz existentes.

El fondo y el logo se colorean al pintar en Flutter, conservando byte por byte los PNG originales. La matriz del fondo sitúa el tono central de la textura en crema; la del logo transforma las tintas originales a los colores de la marca del video y preserva blanco y transparencia. La apertura nativa Android recibe los mismos colores de fondo y símbolo a través de sus recursos XML.

La pregunta conserva al menos 5,61:1 en las cuatro cartas; sus etiquetas, al menos 6,35:1. Los textos pequeños sobre naranja conservan #0E2D20 y los enlaces pequeños, #9E3D06. El botón principal conserva letras blancas, peso 700 y su tamaño grande, con 3,10:1. La ayuda blanca sobre verde tiene 7,34:1. Mediciones completas en `qa/estilo-video-v11/contraste.json`.

Verificación: análisis sin incidencias, 102 pruebas aprobadas y APK normal de `lib/main.dart`. El control existente de las esquinas ahora compara los tres canales de color para detectar correctamente las superficies suaves sobre crema; mantiene las comprobaciones de permanencia de textura, posiciones y momento de aparición. El recorrido Android usa un AVD de QA separado y registra la rotación de las cartas, sus caras, variantes sonoras y reposo.

La actualización normal se instaló en Recorridos_API_36. La sesión y las preferencias se preservaron byte por byte; registros y capturas en `qa/estilo-video-v11`. `alcance.json` confirma que solamente cambiaron los dos archivos de color de producción.


### Figuras de fondo uniformes · 2 de octubre de 2026

Se corrige el filtro compartido del fondo para transformar las figuras originales a verde salvia #D9E7D6, conservando el crema #F5F2E8, las marcas verdes, blancos, transparencia y textura. La transformación anterior por luminancia dejaba las figuras grisáceas; ahora se anclan los colores originales de fondo, figura, marca y blanco. Solo cambia `lib/tema/tema_contame.dart`; no cambian recursos, medidas, movimiento ni sonido.

Formato, análisis, 102 pruebas y APK normal aprobados. Revisión visual en Android QA y actualización del emulador de Alan preservando byte por byte preferencias y sesión. Evidencia: `qa/fondo-salvia-uniforme`. El primer recorrido automático alcanzó el resumen porque el AVD conservaba una ronda con dos cartas restantes; se volvió al menú y se repitió con una ronda nueva.


## Ícono Android multicolor · 2 de octubre de 2026

Se corrige el ícono de instalación y apertura: el tinte monocromo de Android borraba letras y burbuja naranja. Recurso derivado con ImageGen de la imagen original, dos burbujas verdes/naranjas y letras claras, con transparencia real. Se guarda como che-simbolo-v11.png en Flutter y che_simbolo_v11.png en Android; originales conservados. Los drawables adaptativo y anterior a API 26 usan el recurso multicolor sin tinte. Los seis glifos Phosphor internos ya heredan la paleta vigente y mantienen su forma.

Versión 0.1.1+2. Análisis limpio, 102 pruebas, APK debug/release, firma y modo no depurable comprobados. Launcher Android: ícono legible completo sobre crema. Apertura y menú release aprobados, sin errores fatales ni desbordes. Al primer intento el launcher todavía se estaba asentando; se repitió el gesto y la captura correctamente. Emulador normal actualizado con datos conservados byte por byte. Release sustituye el archivo anterior en Drive, conservando ID y enlace; metadata y tamaño verificados. Firma de desarrollo actual; firma definitiva Play pendiente. Evidencias: qa/icono-v11.
