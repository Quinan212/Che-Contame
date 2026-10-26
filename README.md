# Che Contame

Proyecto Flutter local del juego de cartas de conversación, cuya interfaz conserva el nombre Che Preguntame. Gratuito y sin conexión, con tres niveles, rondas de 12 o 25 cartas, repreguntas, dinámicas, sonidos y progreso local.

## Desarrollo

Flutter 3.47.2, Dart 3.13.2, Java 17 y Android SDK 36. Paquete Android de publicación: ar.maillet.encuentroer. Versión de esta copia: 1.0.0+6.

```sh
flutter pub get
flutter run
```

Se conservan las fuentes, recursos, contenido, pruebas y herramientas de desarrollo. Las cachés, dependencias descargadas, APK, capturas y resultados de pruebas no se incluyen. Algunas herramientas de QA conservan rutas del entorno original de Windows y deben ajustarse en otra máquina.

## Firma

El archivo de firma que indicaba la configuración anterior no estaba disponible. Por indicación del propietario se creó una firma nueva exclusiva para Che Contame. Esto no recupera ni reemplaza la firma de publicaciones anteriores.

La firma y su configuración se incluyen en:

- android/firma-che-contame/che-contame-upload.jks
- android/firma-che-contame/che-contame-upload-certificate.pem
- android/firma-che-contame/credenciales.properties
- android/key.properties, con una ruta relativa válida desde android/app/.

```sh
flutter build apk --release
flutter build appbundle --release
```

El contenido de las cartas, las reglas, los sonidos y las animaciones del juego local no se modificaron para preparar esta publicación.
