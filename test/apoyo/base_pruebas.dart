import 'dart:convert';
import 'dart:io';

import 'package:contame_android/compartido/almacenamiento/almacen_preferencias.dart';
import 'package:contame_android/funcionalidades/partida/datos/repositorio_preguntas.dart';
import 'package:contame_android/funcionalidades/partida/modelos/catalogo_preguntas.dart';

class AlmacenMemoria implements AlmacenPreferencias {
  final datos = <String, String>{};
  bool fallar = false;
  int escrituras = 0;
  Duration demora = Duration.zero;
  @override
  Future<String?> leer(String clave) async => datos[clave];
  @override
  Future<void> escribir(String clave, String valor) async {
    if (demora != Duration.zero) await Future<void>.delayed(demora);
    if (fallar) throw const FileSystemException('Fallo simulado.');
    escrituras++;
    datos[clave] = valor;
  }
}

CatalogoPreguntas catalogoReal() => RepositorioPreguntas.decodificar(
  File('assets/contenido/preguntas-base.json').readAsStringSync(encoding: utf8),
);

class PreguntasFijas extends RepositorioPreguntas {
  PreguntasFijas(this.catalogo);
  final CatalogoPreguntas catalogo;
  @override
  Future<CatalogoPreguntas> cargar() async => catalogo;
}
