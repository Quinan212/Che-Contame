import 'package:flutter/material.dart';

abstract final class TemaContame {
  static const tinta = Color(0xFF2A6047);
  static const tenue = Color(0xFF385447);
  static const naranja = Color(0xFFEE6B26);
  static const sobreNaranja = Color(0xFF0E2D20);
  static const naranjaTexto = Color(0xFF9E3D06);
  static const salvia = Color(0xFFD9E7D6);
  static const fondo = Color(0xFFF5F2E8);
  static const hoja = Color(0xFFFFF9EE);
  static const borde = Color(0xFFADC4AB);
  static const salviaClara = Color(0xFFE4EDDE);
  static const salviaMedia = Color(0xFFD9E7D6);
  static const salviaOscura = Color(0xFFCDDCC8);

  // Recolorear al pintar preserva el original, su textura y su transparencia.
  // Fondo crema, figuras salvia y marcas verdes; conserva textura y alfa.
  static const filtroFondo = ColorFilter.matrix([
    -0.938451974,
    3.019987566,
    -1.515542431,
    0.000000000,
    110.671743861,
    0.885296860,
    -1.350885919,
    1.392601803,
    0.000000000,
    18.611750078,
    1.715573516,
    -2.730245570,
    2.193036991,
    0.000000000,
    -45.483058750,
    0.000000000,
    0.000000000,
    0.000000000,
    1.000000000,
    0.000000000,
  ]);
  // Colores del logo del video; forma, textura y alfa originales.
  static const filtroLogo = ColorFilter.matrix([
    2.353728489,
    -3.284894837,
    1.931166348,
    0.000000000,
    0.000000000,
    2.442957298,
    -5.239643085,
    3.796685787,
    0.000000000,
    0.000000000,
    0.386233270,
    -1.332695985,
    1.946462715,
    0.000000000,
    0.000000000,
    0.000000000,
    0.000000000,
    0.000000000,
    1.000000000,
    0.000000000,
  ]);
  static const coloresCartas = [
    Color(0xFFD7E8B1),
    Color(0xFFFFE0B2),
    Color(0xFFCDE9D8),
    Color(0xFFFCE7AF),
  ];
  static Color colorCarta(int indice) =>
      coloresCartas[indice % coloresCartas.length];
  static final claro = ThemeData(
    useMaterial3: true,
    fontFamily: 'Outfit',
    scaffoldBackgroundColor: fondo,
    colorScheme: ColorScheme.fromSeed(seedColor: naranja).copyWith(
      primary: naranjaTexto,
      onPrimary: Colors.white,
      primaryContainer: coloresCartas[1],
      onPrimaryContainer: tinta,
      secondary: tenue,
      onSecondary: Colors.white,
      secondaryContainer: salvia,
      onSecondaryContainer: tinta,
      tertiary: tinta,
      onTertiary: Colors.white,
      tertiaryContainer: salviaClara,
      onTertiaryContainer: tinta,
      surface: hoja,
      onSurface: tinta,
      onSurfaceVariant: tenue,
      surfaceContainerLowest: hoja,
      surfaceContainerLow: fondo,
      surfaceContainer: fondo,
      surfaceContainerHigh: salviaClara,
      surfaceContainerHighest: salvia,
      outline: tenue,
      outlineVariant: borde,
      inverseSurface: tinta,
      onInverseSurface: hoja,
      inversePrimary: coloresCartas[1],
      shadow: tinta,
      scrim: tinta,
    ),
    textTheme: const TextTheme(
      bodyMedium: TextStyle(color: tinta, fontSize: 16),
      bodySmall: TextStyle(color: tenue, fontSize: 13),
    ),
    iconTheme: const IconThemeData(color: tinta),
    filledButtonTheme: FilledButtonThemeData(
      style: FilledButton.styleFrom(
        backgroundColor: naranja,
        foregroundColor: sobreNaranja,
      ),
    ),
    switchTheme: SwitchThemeData(
      trackColor: WidgetStateProperty.resolveWith(
        (states) => states.contains(WidgetState.selected) ? naranja : null,
      ),
      thumbColor: WidgetStateProperty.resolveWith(
        (states) => states.contains(WidgetState.selected) ? Colors.white : null,
      ),
    ),
    bottomSheetTheme: const BottomSheetThemeData(
      backgroundColor: hoja,
      showDragHandle: true,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(28)),
      ),
    ),
    snackBarTheme: const SnackBarThemeData(
      behavior: SnackBarBehavior.floating,
      backgroundColor: tinta,
    ),
  );
}
