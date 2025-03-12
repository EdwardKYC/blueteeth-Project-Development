import 'package:flutter/material.dart';
import 'package:mobile/router.dart';

void main() async {
  runApp(MaterialApp(
    initialRoute: router.register,
    routes: router.getRoutes(),
  ));
}