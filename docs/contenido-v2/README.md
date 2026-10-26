# Contame · edición de complicidad cotidiana

Edición 0.2 · 2 de octubre de 2026.

Se reemplazaron las 75 preguntas, las 75 repreguntas y las 15 consignas de la biblioteca anterior. También se adaptaron los seis ejemplos de tutorial y laboratorio, las descripciones de los niveles y la invitación de la ayuda. Se conserva la progresión Para arrancar → Se pone bueno → En confianza.

## Criterio editorial

La referencia es la [guía editorial de la investigación](../../../investigacion/conversaciones-argentinas-16-25/GUIA-EDITORIAL.md), basada en 41 fuentes y 85 unidades de análisis. Es investigación cualitativa exploratoria, con concentración geográfica en Paraná y La Plata; no una muestra representativa del público argentino de 16–25.

Las cartas proponen escenas que dan pie a contar algo: destrabar el plan de un chat, explicar una frase del grupo, mostrar un rincón del barrio, sumarse a una juntada, recomendar un gusto o acordarse de un detalle. La identidad argentina aparece en la situación y en el voseo, con modismos moderados. El nivel más cercano deja entrar afecto, autonomía y curiosidad sin convertir cada respuesta en una confesión. El coqueteo es opcional y las cartas funcionan entre amigos.

No se presupone una pareja, consumo de alcohol, contenido sexual, dinero para salir ni interés romántico. Las repreguntas siguen un detalle de la primera respuesta. Las consignas alternan creación, humor, planes y escucha, sin puntajes ni obligaciones de revelar información privada.

Los textos son escritura original. Las fuentes registran mecanismos y contextos que inspiraron la adaptación; no son citas ni certifican que cada escena ocurrió literalmente. Falta probar comprensión, naturalidad al leer en voz alta, variedad y disposición a responder con jugadores de 16–17 y 18–25 de las tres regiones.

## Archivos

- [BIBLIOTECA.md](BIBLIOTECA.md): lectura completa de las cartas con referencias.
- [redaccion.tsv](redaccion.tsv) y [consignas.tsv](consignas.tsv): originales editables de esta edición.
- [trazabilidad.json](trazabilidad.json): relación entre cada carta, las fuentes y los casos de investigación.
- [preguntas-v1-respaldo.json](preguntas-v1-respaldo.json): respaldo exacto de la biblioteca previa.
- `compilar_biblioteca.py`: genera el asset, la biblioteca y la trazabilidad; comprueba IDs, cantidades, cambios de texto, duplicados exactos, signos y Unicode.
- [QA.md](../../qa/contenido-v2/QA.md): verificación técnica y entrega Android.

## Integración y continuidad

El asset activo es `assets/contenido/preguntas-base.json`, versión `0.2-complicidad-cotidiana`. Se mantienen los 90 IDs, los niveles y cinco temas de cinco cartas por nivel, para conservar el orden determinista de rondas anteriores. Las rondas nuevas usan exclusivamente los textos nuevos.

La sesión sigue en formato v2. `textosCompartidos` guarda el título de cada carta completada. Para una sesión `0.1-borrador`, el catálogo contiene un mapa histórico explícito: se conservan orden, posición, tiempos y pasadas, y el resumen sigue mostrando los textos que ya se conversaron. Las próximas cartas de esa ronda muestran la edición nueva. Las revisiones desconocidas o los IDs incompatibles no se aceptan.

La carga no escribe preferencias. El guardado normal ocurre al jugar. El mapa histórico no pertenece al mazo activo. Los colores de tarjetas, animaciones y biblioteca sonora v3 se conservan.
