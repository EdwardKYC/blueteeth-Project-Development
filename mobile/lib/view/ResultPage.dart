import 'package:flutter/material.dart';
import 'package:mobile/controller/BookController.dart';
import 'package:mobile/model/Book.dart';

class Result extends StatelessWidget {
  const Result({super.key});
  @override
  Widget build(BuildContext context) {
    final List<Book> books = ModalRoute.of(context)!.settings.arguments as List<Book>;
    final BookController bookController = BookController();
    return Scaffold(
      appBar: AppBar(
        title: const Text('Search Results'),
      ),
      body: ListView.builder(
        itemCount: books.length,
        itemBuilder: (context, index) {
          final book = books[index];
          return Card(
            margin: const EdgeInsets.all(8.0),
            child: ListTile(
              title: Text(
                  book.name,
                style: const TextStyle(
                  fontSize: 20.0,
                  fontFamily: 'NotoSans',
                ),
              ),
              subtitle: Text(
                  book.description,
                style: const TextStyle(
                  fontSize: 18.0,
                  fontFamily: 'NotoSans',
                ),
              ),
              onTap: () async {
                final color = await bookController.fetchBookColor(book.id, context);
                if (color != null) {
                  Navigator.pushNamed(
                    context,
                    '/bookDetails',
                    arguments: {
                      'book': book,
                      'color': color,
                    }
                  );
                }
              },
            ),
          );
        },
      ),
    );
  }
}


