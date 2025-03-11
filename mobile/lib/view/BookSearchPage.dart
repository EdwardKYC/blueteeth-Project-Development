import 'package:flutter/material.dart';
import 'package:mobile/controller/BookController.dart';
import 'package:mobile/controller/UserController.dart';

class Search extends StatefulWidget {
  const Search({super.key});

  @override
  State<Search> createState() => _SearchState();
}

class _SearchState extends State<Search> {
  final TextEditingController _bookNameController = TextEditingController();
  late BookController bookController;
  late UserController userController;

  @override
  void initState(){
    super.initState();
    bookController = BookController();
    userController = UserController();
  }
  @override
  void dispose() {
    _bookNameController.dispose();
    super.dispose();
  }
  @override
  Widget build(BuildContext context) {
    final String UserName = ModalRoute.of(context)!.settings.arguments as String;
    return Scaffold(
      appBar: AppBar(
        title: const Text('Search Books'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              UserName,
              style: const TextStyle(
                fontSize: 30,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 10),
            Align(
              alignment: Alignment.centerLeft,
              child: ElevatedButton(
                onPressed: () async {
                  await userController.signOut(UserName, context);
                },
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.red,
                  foregroundColor: Colors.white,
                ),
                child: const Text("Logout"),
              ),
            ),
            const SizedBox(height: 30,),
            TextField(
              controller: _bookNameController,
              decoration: const InputDecoration(labelText: 'Book name'),
              keyboardType: TextInputType.text,
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: () async {
                final books = await bookController.search(
                    _bookNameController.text,
                    context,
                );
                if (books != null && books.isNotEmpty) {
                  Navigator.pushNamed(
                    context,
                    '/result',
                    arguments: books,
                  );
                } else {
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(
                      content: Text("No books found."),
                      backgroundColor: Colors.red,
                    ),
                  );
                }
              },
              child: const Text('Search'),
            ),
            const SizedBox(height: 50),
          ],
        ),
      ),
    );
  }
}
