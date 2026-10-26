import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'funcionalidades/inicio/pantallas/pantalla_inicio.dart';
import 'funcionalidades/bienvenida/componentes/puerta_bienvenida.dart';
import 'compartido/movimiento/movimiento.dart';
import 'tema/tema_contame.dart';

class ContameApp extends ConsumerWidget {
  const ContameApp({super.key});
  @override
  Widget build(BuildContext context, WidgetRef ref) => MaterialApp(
    title: 'Che, preguntame',
    debugShowCheckedModeBanner: false,
    theme: TemaContame.claro,
    locale: const Locale('es', 'AR'),
    supportedLocales: const [Locale('es', 'AR')],
    localizationsDelegates: GlobalMaterialLocalizations.delegates,
    navigatorObservers: [observadorPaginas],
    builder: (context, child) => MediaQuery(
      data: MediaQuery.of(context).copyWith(
        disableAnimations:
            MediaQuery.disableAnimationsOf(context) ||
            !ref.watch(permitirMovimientoProvider),
      ),
      child: child!,
    ),
    home: const PuertaBienvenida(child: PantallaInicio()),
  );
}
