import 'dart:math' as math;

import 'package:flutter/material.dart';

import '../../tema/tema_contame.dart';

/// Un solo reloj para el fondo y los elementos del menú; no se reinicia al
/// cargar datos, seleccionar un nivel ni volver de otra pantalla.
class EntradaInicio extends InheritedWidget {
  const EntradaInicio({
    super.key,
    required this.progreso,
    required this.enCurso,
    this.ocultarSonido = false,
    this.enlazarTutorial,
    required super.child,
  });
  final double progreso;
  final bool enCurso;
  final bool ocultarSonido;
  final ValueChanged<Animation<double>?>? enlazarTutorial;

  static EntradaInicio? of(BuildContext context) =>
      context.dependOnInheritedWidgetOfExactType<EntradaInicio>();

  @override
  bool updateShouldNotify(EntradaInicio oldWidget) =>
      progreso != oldWidget.progreso ||
      enCurso != oldWidget.enCurso ||
      ocultarSonido != oldWidget.ocultarSonido;
}

class RevelarInicio extends StatelessWidget {
  const RevelarInicio({
    super.key,
    required this.child,
    this.inicio = 0,
    this.fin = 1,
  });
  final Widget child;
  final double inicio;
  final double fin;

  @override
  Widget build(BuildContext context) {
    final reloj = EntradaInicio.of(context);
    if (reloj == null) return child;
    final valor = ((reloj.progreso - inicio) / (fin - inicio)).clamp(0.0, 1.0);
    final progreso = Curves.easeInOutCubic.transform(valor);
    return ExcludeSemantics(
      excluding: progreso < 1,
      child: ClipRect(
        clipper: _RevelacionVertical(progreso),
        child: Transform.translate(
          offset: Offset(0, -14 * (1 - progreso)),
          child: child,
        ),
      ),
    );
  }
}

class _RevelacionVertical extends CustomClipper<Rect> {
  const _RevelacionVertical(this.progreso);
  final double progreso;
  @override
  Rect getClip(Size size) =>
      Rect.fromLTWH(0, 0, size.width, size.height * progreso);
  @override
  bool shouldReclip(_RevelacionVertical oldClipper) =>
      oldClipper.progreso != progreso;
}

class ColumnaInicio extends StatelessWidget {
  const ColumnaInicio({
    super.key,
    required this.children,
    this.crossAxisAlignment = CrossAxisAlignment.center,
  });
  final List<Widget> children;
  final CrossAxisAlignment crossAxisAlignment;

  @override
  Widget build(BuildContext context) {
    final bloques = children.where((child) => child is! SizedBox).length;
    var indice = 0;
    return Column(
      crossAxisAlignment: crossAxisAlignment,
      children: [
        for (final child in children)
          if (child is SizedBox)
            child
          else
            RevelarInicio(
              inicio: .10 + .60 * indice / math.max(1, bloques - 1),
              fin: math.min(
                1.0,
                .44 + .60 * indice++ / math.max(1, bloques - 1),
              ),
              child: child,
            ),
      ],
    );
  }
}

class FondoApertura extends StatelessWidget {
  const FondoApertura({super.key, required this.progreso});
  final double progreso;

  @override
  Widget build(BuildContext context) => ExcludeSemantics(
    child: Stack(
      fit: StackFit.expand,
      children: [
        const ColoredBox(color: TemaContame.fondo),
        // Mostrar la región central libre de adornos del recurso original.
        // Es un encuadre de pintado, no otra imagen editada ni otra cortina.
        RepaintBoundary(
          key: const ValueKey('textura-apertura'),
          child: ClipRect(
            child: LayoutBuilder(
              builder: (context, limites) => OverflowBox(
                minWidth: limites.maxWidth * 3,
                maxWidth: limites.maxWidth * 3,
                minHeight: limites.maxHeight * 3,
                maxHeight: limites.maxHeight * 3,
                child: ColorFiltered(
                  colorFilter: TemaContame.filtroFondo,
                  child: Image.asset(
                    'assets/imagenes/conversation-background-v2.png',
                    fit: BoxFit.fill,
                    filterQuality: FilterQuality.high,
                  ),
                ),
              ),
            ),
          ),
        ),
        CustomPaint(
          key: const ValueKey('esquinas-inicio'),
          painter: _Esquinas(progreso),
        ),
      ],
    ),
  );
}

class _Esquinas extends CustomPainter {
  const _Esquinas(this.progreso);
  final double progreso;
  double tramo(double inicio, double fin) => Curves.easeInOutCubic.transform(
    ((progreso - inicio) / (fin - inicio)).clamp(0.0, 1.0),
  );

  @override
  void paint(Canvas canvas, Size size) {
    final w = size.width;
    final h = size.height;
    final superior = tramo(0, .70);
    final inferior = tramo(.24, 1);
    final arriba = Path()
      ..moveTo(w * .496, 0)
      ..cubicTo(w * .516, h * .057, w * .573, h * .104, w * .744, h * .149)
      ..cubicTo(w * .876, h * .179, w * .956, h * .212, w, h * .249)
      ..lineTo(w, 0)
      ..close();
    if (superior > 0) {
      // El frente curvo baja siguiendo el contorno, como una pincelada.
      final frente = h * .27 * superior;
      canvas.save();
      canvas.clipPath(
        Path()
          ..lineTo(w, 0)
          ..lineTo(w, frente)
          ..quadraticBezierTo(
            w * .7,
            frente - h * .035 * math.sin(math.pi * superior),
            0,
            frente,
          )
          ..close(),
      );
      canvas.drawPath(
        arriba,
        Paint()
          ..shader = const LinearGradient(
            colors: [TemaContame.salviaClara, TemaContame.salviaMedia],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ).createShader(Rect.fromLTWH(w * .49, 0, w * .51, h * .26)),
      );
      canvas.restore();
    }
    final abajo = Path()
      ..moveTo(0, h * .821)
      ..cubicTo(w * .13, h * .837, w * .118, h * .895, w * .158, h * .916)
      ..cubicTo(w * .218, h * .959, w * .31, h * .94, w * .392, h * .952)
      ..cubicTo(w * .46, h * .964, w * .48, h * .978, w * .504, h)
      ..lineTo(0, h)
      ..close();
    if (inferior > 0) {
      final frente = w * .53 * inferior;
      canvas.save();
      canvas.clipPath(
        Path()
          ..moveTo(0, h * .80)
          ..lineTo(frente, h * .80)
          ..quadraticBezierTo(
            frente - w * .025 * math.sin(math.pi * inferior),
            h * .91,
            frente,
            h,
          )
          ..lineTo(0, h)
          ..close(),
      );
      canvas.drawPath(
        abajo,
        Paint()
          ..shader = const LinearGradient(
            colors: [TemaContame.salviaMedia, TemaContame.salviaOscura],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ).createShader(Rect.fromLTWH(0, h * .82, w * .51, h * .18)),
      );
      canvas.restore();
    }
    final marcas = [
      Path()
        ..moveTo(w * .180, h * .898)
        ..lineTo(w * .192, h * .874),
      Path()
        ..moveTo(w * .211, h * .910)
        ..lineTo(w * .244, h * .896),
      Path()
        ..moveTo(w * .233, h * .922)
        ..lineTo(w * .268, h * .918),
    ];
    final tinta = Paint()
      ..color = TemaContame.tinta
      ..style = PaintingStyle.stroke
      ..strokeWidth = w * .016
      ..strokeCap = StrokeCap.round;
    for (var i = 0; i < marcas.length; i++) {
      final valor = tramo(.45 + i * .10, .78 + i * .10);
      if (valor == 0) continue;
      final metrica = marcas[i].computeMetrics().first;
      canvas.drawPath(metrica.extractPath(0, metrica.length * valor), tinta);
    }
  }

  @override
  bool shouldRepaint(_Esquinas oldDelegate) => progreso != oldDelegate.progreso;
}
