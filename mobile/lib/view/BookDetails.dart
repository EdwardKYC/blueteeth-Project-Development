import 'package:flutter/material.dart';
import 'package:mobile/model/Book.dart';
import 'package:mobile/controller/BookController.dart';
import 'package:mobile/util.dart';
import 'package:mobile/router.dart';

class BookDetails extends StatelessWidget {
  const BookDetails({super.key});

  @override
  Widget build(BuildContext context) {
    final Map<String, dynamic> args = ModalRoute.of(context)!.settings.arguments as Map<String, dynamic>;
    final Book book = args['book'];
    final Color dynamicColor = Util.parseColor(args['color']);
    final BookController bookController = BookController();

    return PopScope<Object?>(
      canPop: true,
      onPopInvokedWithResult: (bool didPop, Object? result) async {
        await bookController.finish(context);
      },
      child: Scaffold(
        appBar: AppBar(
          title: Text(book.name),
        ),
        body: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                "Book Name: ${book.name}",
                style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 10),
              Text(
                "Description: ${book.description}",
                style: const TextStyle(fontSize: 18),
              ),
              const SizedBox(height: 30),
              Center(
                child: Container(
                  width: 80, // 圆圈的直径
                  height: 80,
                  decoration: BoxDecoration(
                    color: dynamicColor, // 圆圈颜色
                    shape: BoxShape.circle, // 圆形
                    border: Border.all(color: Colors.black, width: 2), // 可选的黑色边框
                  ),
                ),
              ),
              const SizedBox(height: 30),
              Center(
                child: ElevatedButton(
                  onPressed: () {
                    Navigator.popUntil(
                      context,
                      ModalRoute.withName(router.search),
                    );
                  },
                  style: ElevatedButton.styleFrom(
                    padding: const EdgeInsets.symmetric(horizontal: 50, vertical: 20),
                    textStyle: const TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  child: const Text('Finish'),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
