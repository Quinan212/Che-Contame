import 'dart:async';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../compartido/componentes/boton_principal.dart';
import '../../../compartido/componentes/boton_sonido.dart';
import '../../../compartido/componentes/entrada_inicio.dart';
import '../../../compartido/sonidos/respuesta_interfaz.dart';
import '../../../tema/tema_contame.dart';
import '../../ajustes/controladores/controlador_experiencia.dart';
import '../pantallas/pantalla_tutorial.dart';

class PuertaBienvenida extends ConsumerStatefulWidget {
  const PuertaBienvenida({super.key, required this.child});
  final Widget child;
  @override
  ConsumerState<PuertaBienvenida> createState() => _PuertaBienvenidaState();
}

class _PuertaBienvenidaState extends ConsumerState<PuertaBienvenida>
    with TickerProviderStateMixin, WidgetsBindingObserver {
  static const _salidaMs = 2750;
  static const _entradaMenuMs = 1850;
  static const _salidaReducida = Duration(milliseconds: 1700);
  late final _espera =
      AnimationController(
        vsync: this,
        duration: const Duration(seconds: 2),
        animationBehavior: AnimationBehavior.preserve,
      )..addStatusListener((estado) {
        if (estado == AnimationStatus.completed) unawaited(_mostrarBoton());
      });
  late final _logo = AnimationController(vsync: this);
  late final _boton = AnimationController(
    vsync: this,
    duration: const Duration(milliseconds: 550),
    animationBehavior: AnimationBehavior.preserve,
  );
  late final _salida =
      AnimationController(
          vsync: this,
          animationBehavior: AnimationBehavior.preserve,
        )
        ..addListener(_sonorizarEntrada)
        ..addStatusListener((estado) {
          if (estado == AnimationStatus.completed) unawaited(_seguir());
        });
  bool _preparada = false;
  bool _botonVisible = false;
  bool _entrando = false;
  bool _entradaLista = false;
  bool _primerPlano = true;
  bool _entradaSonoraEmitida = false;
  final _pantallaKey = GlobalKey();
  final _posicionBotonKey = GlobalKey();
  Offset _hastaCentro = Offset.zero;
  Animation<double>? _tutorial;

  void _enlazarTutorial(Animation<double>? animacion) {
    if (mounted) setState(() => _tutorial = animacion);
  }

  // Salida por etapas: identidad, botón, pausa y entrada del menú.
  double _tramo(int inicio, int fin) =>
      ((_salida.value * _salidaMs - inicio) / (fin - inicio)).clamp(0.0, 1.0);

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addObserver(this);
    final estado = WidgetsBinding.instance.lifecycleState;
    _primerPlano = estado == null || estado == AppLifecycleState.resumed;
    unawaited(_preparar());
  }

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    final reducido = MediaQuery.disableAnimationsOf(context);
    _logo.duration = reducido
        ? Duration.zero
        : const Duration(milliseconds: 420);
    _salida.duration = reducido
        ? _salidaReducida
        : const Duration(milliseconds: _salidaMs);
  }

  Future<void> _preparar() async {
    try {
      await ref.read(experienciaProvider.future);
      unawaited(
        prepararRespuesta(ref.read(respuestaInterfazProvider))
            .catchError((Object _) {}),
      );
    } on Object {
      // La portada sigue disponible aunque no se pueda preparar el audio.
    }
    if (!mounted) return;
    setState(() => _preparada = true);
    if (_primerPlano) _reanudar();
  }

  Future<void> _mostrarBoton() async {
    if (!mounted || !_primerPlano || _botonVisible) return;
    try {
      await prepararRespuestaApertura(ref.read(respuestaInterfazProvider));
    } on Object {
      // El acceso sigue disponible aunque un dispositivo no prepare el audio.
    }
    if (!mounted || !_primerPlano || _botonVisible) return;
    setState(() => _botonVisible = true);
    _boton.forward();
    _emitir(EfectoInterfaz.bienvenida);
  }

  void _emitir(EfectoInterfaz efecto) {
    if (ref.read(experienciaProvider).value?.sonidos ?? false) {
      ref.read(respuestaInterfazProvider).emitir(efecto);
    }
  }

  void _sonorizarEntrada() {
    if (!mounted || !_primerPlano || !_entrando || _entradaSonoraEmitida) {
      return;
    }
    // El mismo reloj que mueve el menú: la pausa en segundo plano conserva
    // la sincronía. Una etapa silenciada se consume y no se repite al reactivar.
    final umbral = _salida.duration == _salidaReducida
        ? 1.0
        : _entradaMenuMs / _salidaMs;
    if (_salida.value < umbral) return;
    _entradaSonoraEmitida = true;
    _emitir(EfectoInterfaz.entradaInicio);
  }

  void _entrar() {
    if (!_botonVisible || !_boton.isCompleted || _entrando || !_primerPlano) {
      return;
    }
    final pantalla = _pantallaKey.currentContext?.findRenderObject();
    final boton = _posicionBotonKey.currentContext?.findRenderObject();
    if (pantalla is RenderBox && boton is RenderBox) {
      final centroPantalla = pantalla.localToGlobal(
        pantalla.size.center(Offset.zero),
      );
      final centroBoton = boton.localToGlobal(boton.size.center(Offset.zero));
      _hastaCentro = centroPantalla - centroBoton;
    }
    _boton.stop();
    setState(() => _entrando = true);
    _emitir(EfectoInterfaz.comenzar);
    _salida.forward();
  }

  Future<void> _seguir() async {
    if (!mounted || _entradaLista) return;
    setState(() => _entradaLista = true);
    try {
      final preferencias = await ref.read(experienciaProvider.future);
      if (mounted && !preferencias.tutorialVisto) {
        await mostrarTutorial(
          context,
          conSonido: false,
          enlazarTransicion: _enlazarTutorial,
        );
      }
    } on Object {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('La bienvenida está disponible desde «Ver tutorial».'),
        ),
      );
    }
  }

  void _reanudar() {
    if (!_preparada || _entradaLista) return;
    if (_entrando) {
      _salida.forward();
    } else {
      if (!_logo.isCompleted) _logo.forward();
      if (!_espera.isCompleted) {
        _espera.forward();
      } else if (!_botonVisible) {
        unawaited(_mostrarBoton());
      }
      if (_botonVisible && !_boton.isCompleted) _boton.forward();
    }
  }

  @override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    _primerPlano = state == AppLifecycleState.resumed;
    if (_primerPlano) {
      _reanudar();
    } else {
      _espera.stop();
      _logo.stop();
      _boton.stop();
      _salida.stop();
      if (!_entradaLista) ref.read(respuestaInterfazProvider).silenciar();
    }
  }

  @override
  void dispose() {
    WidgetsBinding.instance.removeObserver(this);
    _espera.dispose();
    _logo.dispose();
    _boton.dispose();
    _salida.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) => ClipRect(
    key: _pantallaKey,
    child: AnimatedBuilder(
      animation: Listenable.merge([_salida, _boton, ?_tutorial]),
      builder: (context, _) {
        final reducido = MediaQuery.disableAnimationsOf(context);
        final retiroLogo = reducido && _entrando ? 1.0 : _tramo(0, 550);
        final subidaBoton = reducido
            ? 0.0
            : Curves.easeInOutCubic.transform(_tramo(550, 1350));
        final retiroBoton = reducido && _entrando ? 1.0 : _tramo(1350, 1700);
        final entradaMenu = _entradaLista
            ? 1.0
            : reducido
            ? 0.0
            : _tramo(_entradaMenuMs, _salidaMs);
        final tutorial = _tutorial?.value ?? 0.0;
        final menuVisible = entradaMenu * (1 - tutorial / .30).clamp(0.0, 1.0);
        return Stack(
          children: [
            Positioned.fill(child: FondoApertura(progreso: entradaMenu)),
            if (!_entradaLista)
              Positioned.fill(
                key: const ValueKey('cortina-inicial'),
                child: _portada(
                  retiroLogo,
                  subidaBoton,
                  retiroBoton,
                  entradaMenu,
                ),
              ),
            Positioned.fill(
              child: ExcludeSemantics(
                excluding: !_entradaLista || tutorial > 0,
                child: IgnorePointer(
                  ignoring: !_entradaLista || tutorial > 0,
                  child: EntradaInicio(
                    key: const ValueKey('entrada-pantalla-inicial'),
                    progreso: menuVisible,
                    enCurso: !_entradaLista || tutorial > 0,
                    ocultarSonido: !_entradaLista,
                    enlazarTutorial: _enlazarTutorial,
                    child: Offstage(
                      offstage: _entradaLista && menuVisible == 0,
                      child: widget.child,
                    ),
                  ),
                ),
              ),
            ),
          ],
        );
      },
    ),
  );

  Widget _portada(
    double retiroLogo,
    double subidaBoton,
    double retiroBoton,
    double entradaMenu,
  ) => Material(
    color: Colors.transparent,
    child: Stack(
      children: [
        Positioned.fill(
          child: SafeArea(
            minimum: const EdgeInsets.fromLTRB(32, 80, 32, 32),
            child: LayoutBuilder(
              builder: (context, limites) => SingleChildScrollView(
                physics: _entrando
                    ? const NeverScrollableScrollPhysics()
                    : null,
                child: ConstrainedBox(
                  constraints: BoxConstraints(minHeight: limites.maxHeight),
                  child: Center(
                    child: ConstrainedBox(
                      constraints: const BoxConstraints(maxWidth: 356),
                      child: Column(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          _identidad(retiroLogo),
                          const SizedBox(height: 36),
                          _comenzar(subidaBoton, retiroBoton),
                        ],
                      ),
                    ),
                  ),
                ),
              ),
            ),
          ),
        ),
        Positioned(
          top:
              16 -
              12 *
                  Curves.easeInOutCubic.transform(
                    (entradaMenu / .35).clamp(0.0, 1.0),
                  ),
          right:
              16 +
              (46 +
                      (MediaQuery.sizeOf(context).width - 560).clamp(
                            0.0,
                            double.infinity,
                          ) /
                          2) *
                  Curves.easeInOutCubic.transform(
                    (entradaMenu / .35).clamp(0.0, 1.0),
                  ),
          child: const SafeArea(child: BotonSonido()),
        ),
      ],
    ),
  );

  Widget _identidad(double retiro) => ExcludeSemantics(
    excluding: _entrando,
    child: Opacity(
      key: const ValueKey('identidad-bienvenida'),
      opacity: 1 - Curves.easeInOutCubic.transform(retiro),
      child: Transform.translate(
        offset: Offset(
          0,
          MediaQuery.disableAnimationsOf(context)
              ? 0
              : -56 * Curves.easeInOutCubic.transform(retiro),
        ),
        child: FadeTransition(
          opacity: _logo,
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              ColorFiltered(
                colorFilter: TemaContame.filtroLogo,
                child: Image.asset(
                  'assets/imagenes/che-preguntame-logo.png',
                  key: const ValueKey('logo-bienvenida'),
                  semanticLabel: 'Che, preguntame',
                  width: 340,
                  fit: BoxFit.contain,
                ),
              ),
              const SizedBox(height: 24),
              const Text(
                'Una carta. Muchas historias.',
                textAlign: TextAlign.center,
                style: TextStyle(color: TemaContame.tenue, fontSize: 16),
              ),
            ],
          ),
        ),
      ),
    ),
  );

  Widget _comenzar(double subida, double retiro) => ExcludeSemantics(
    excluding: !_botonVisible || !_boton.isCompleted || _entrando,
    child: IgnorePointer(
      ignoring: !_botonVisible || !_boton.isCompleted || _entrando,
      child: Transform.translate(
        offset: _hastaCentro * subida,
        child: Opacity(
          key: const ValueKey('retiro-comenzar'),
          opacity: 1 - Curves.easeInOutCubic.transform(retiro),
          child: FadeTransition(
            opacity: MediaQuery.disableAnimationsOf(context)
                ? AlwaysStoppedAnimation(_botonVisible ? 1.0 : 0.0)
                : _boton,
            child: SlideTransition(
              position: Tween(
                begin: MediaQuery.disableAnimationsOf(context)
                    ? Offset.zero
                    : const Offset(0, .18),
                end: Offset.zero,
              ).animate(_boton.drive(CurveTween(curve: Curves.easeOutCubic))),
              child: SizedBox(
                key: _posicionBotonKey,
                child: BotonPrincipal(
                  key: const ValueKey('comenzar-bienvenida'),
                  texto: 'Comenzar',
                  onPressed: _entrar,
                  feedbackExterno: true,
                ),
              ),
            ),
          ),
        ),
      ),
    ),
  );
}
