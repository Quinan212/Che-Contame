import 'dart:async';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../funcionalidades/ajustes/controladores/controlador_experiencia.dart';
import '../../tema/iconos_contame.dart';
import '../movimiento/movimiento.dart';
import '../sonidos/respuesta_interfaz.dart';

class BotonSonido extends ConsumerWidget {
  const BotonSonido({super.key});
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final ajustes = ref.watch(experienciaProvider).value;
    final habilitado = ajustes?.sonidos ?? false;
    return ToqueConRebote(
      child: IconButton(
        key: const ValueKey('sonido'),
        tooltip: habilitado ? 'Silenciar sonidos' : 'Activar sonidos',
        isSelected: habilitado,
        icon: const Icon(IconosContame.silencio, size: 23),
        selectedIcon: const Icon(IconosContame.sonido, size: 23),
        onPressed: ajustes == null
            ? null
            : () {
                if (habilitado) ref.read(respuestaInterfazProvider).silenciar();
                unawaited(
                  ref.read(experienciaProvider.notifier).alternarSonidos().then(
                    (_) {
                      if (!context.mounted) return;
                      if (!habilitado) {
                        ref
                            .read(respuestaInterfazProvider)
                            .emitir(EfectoInterfaz.activarSonido);
                      }
                    },
                  ),
                );
              },
      ),
    );
  }
}
