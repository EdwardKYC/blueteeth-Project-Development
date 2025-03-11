import 'package:flutter/material.dart';

class Util{
  static void showSnackBar(BuildContext context, String message) {
    if (context.mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(message),
          backgroundColor: Colors.red,
        ),
      );
    }
  }
  static Color parseColor(String color) {
    color = color.trim().toLowerCase().replaceFirst('#', '').replaceFirst('0x', '');
    if (color.length == 6) color = 'FF$color';
    return Color(int.parse(color, radix: 16));
  }
}