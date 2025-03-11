import 'package:mobile/model/User.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:crypto/crypto.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:mobile/config.dart';
import 'package:flutter/material.dart';
import 'package:mobile/util.dart';

class UserController{
  String hashPassword(String password) {
    final bytes = utf8.encode(password);
    final digest = sha256.convert(bytes);
    return digest.toString();
  }
  Future<void> signUp(User user, BuildContext context) async {
    final url = Uri.parse('${GlobalSetting.URL}/api/v1/users/register');
    try {
      final response = await http.post(
        url,
        headers: {"Content-Type": "application/json"},
        body: jsonEncode({
          'username': user.email,
          'password': hashPassword(user.password),
        }),
      );
      if (response.statusCode == 200) {
        final Map<String, dynamic> data = jsonDecode(response.body);
        if(data['message'] == 'User registered successfully.'){
          print("Sign up completed.");
          Util.showSnackBar(context, "Sign up completed successfully!");
        }
        else {
          print("Sign up failed with status: ${data['message']}");
          Util.showSnackBar(context, "Sign up failed with status: ${data['message']}");
        }
      }
      else {
        throw Exception("Failed to sign up: ${response.statusCode}");
      }
    }
    catch (e) {
      print("Error occurred during sign up: $e");
      Util.showSnackBar(context, "Sign up failed: $e");
    }
  }

  Future<void> signIn(User user, BuildContext context) async {
    final url = Uri.parse('${GlobalSetting.URL}/api/v1/users/login');
    try{
      final response = await http.post(
        url,
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: "username=${Uri.encodeQueryComponent(user.email)}&password=${Uri.encodeQueryComponent(hashPassword(user.password))}",
      );
      if(response.statusCode == 200) {
        final Map<String, dynamic> data = jsonDecode(response.body);
        if(data['message'] == 'Logged in successfully.'){
          print("Sign in completed.");
          Util.showSnackBar(context, "Sign in completed successfully!");
          SharedPreferences prefs = await SharedPreferences.getInstance();
          await prefs.setString('authToken', data['access_token']);
          Navigator.pushReplacementNamed(
              context,
              '/search',
              arguments: user.email,
          );
        }
        else{
          print("Sign in failed with status: ${data['message']}");
          Util.showSnackBar(context, "Sign in failed with status: ${data['message']}");
        }
      }
      else{
        throw Exception("Failed to sign in: ${response.statusCode}");
      }
    }
    catch (e){
      print("Error occurred during sign in: $e");
      Util.showSnackBar(context, "Sign in failed: $e");
    }
  }
  Future<void> signOut(String userEmail, BuildContext context) async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    await prefs.remove('authToken');
    Navigator.pushReplacementNamed(context, '/login');
  }
}