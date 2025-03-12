import 'package:mobile/model/User.dart';
import 'package:flutter/material.dart';
import 'package:mobile/controller/UserController.dart';

class Register extends StatefulWidget {
  const Register({super.key});

  @override
  State<Register> createState() => _RegisterState();
}

class _RegisterState extends State<Register> {
  final TextEditingController _emailController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();
  late UserController userController;
  @override
  void initState(){
    super.initState();
    userController = UserController();
  }
  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Sign Up'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            const SizedBox(height: 30,),
            TextField(
              controller: _emailController,
              decoration: const InputDecoration(labelText: 'Email'),
              keyboardType: TextInputType.emailAddress,
            ),
            TextField(
              controller: _passwordController,
              decoration: const InputDecoration(labelText: 'Password'),
              obscureText: true,
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: () async {
                await userController.signUp(
                    User(
                      email: _emailController.text,
                      password: _passwordController.text,
                    ),
                    context
                );
              },
              child: const Text('Sign Up'),
            ),
            const SizedBox(height: 20),
            TextButton(
                onPressed: (){
                  Navigator.pushReplacementNamed(context, '/login');
                },
                child: const Text("Sign in")
            ),
          ],
        ),
      ),
    );
  }
}
