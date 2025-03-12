import 'package:mobile/model/Book.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:mobile/config.dart';
import 'package:flutter/material.dart';
import 'package:mobile/util.dart';

class BookController{
  Future<List<Book>?> search(String keyword, BuildContext context) async {
    final url = Uri.parse('${GlobalSetting.URL}/api/v1/books/search_book');
    SharedPreferences prefs = await SharedPreferences.getInstance();
    String? token = prefs.getString('authToken');
    try {
      final response = await http.post(
        url,
        headers: {
          "Content-Type": "application/json",
          "Authorization": "Bearer $token"
        },
        body: jsonEncode({
          'search_term': keyword,
        }),
      );
      if (response.statusCode == 200) {
        final decodedBody = utf8.decode(response.bodyBytes);
        final dynamic data = jsonDecode(decodedBody);
        if(data is List){
          return data.map((book) => Book.fromJson(book)).toList();
        }
        else{
          Util.showSnackBar(context, data["detail"] ?? "No books found.");
          return null;
        }
      }
      else{
        throw Exception("Failed to search book: ${response.statusCode}");
      }
    } catch (e) {
      print("Error occurred during book search: $e");
      Util.showSnackBar(context, 'Error: $e');
      return null;
    }
  }

  Future<String?> fetchBookColor(int id, BuildContext context) async {
    final url = Uri.parse('${GlobalSetting.URL}/api/v1/books/navigate');
    SharedPreferences prefs = await SharedPreferences.getInstance();
    String? token = prefs.getString('authToken');
    try{
      final response = await http.post(
        url,
        headers: {
          "Content-Type": "application/json",
          "Authorization": "Bearer $token"
        },
        body: jsonEncode({
          'book_id': id,
        }),
      );
      if (response.statusCode == 200) {
        final Map<String, dynamic> data = jsonDecode(response.body);
        return data['displayed_color'];
      }
      else{
        throw Exception("Failed to fetch book color: ${response.statusCode}");
      }
    }
    catch(e){
      print("Error occurred during fetch book color: $e");
      Util.showSnackBar(context, 'Error: $e');
      return null;
    }
  }
  Future<void> finish(BuildContext context) async {
    final url = Uri.parse('${GlobalSetting.URL}/api/v1/books/cancel-navigation');
    SharedPreferences prefs = await SharedPreferences.getInstance();
    String? token = prefs.getString('authToken');
    try {
      final response = await http.post(
        url,
        headers: {
          "Authorization": "Bearer $token"
        },
      );
      if(response.statusCode == 200){
        print("Navigation canceled successfully.");
        Util.showSnackBar(context, "Navigation canceled successfully!");
      }
      else{
        throw Exception("Failed to cancel navigation: ${response.statusCode}");
      }
    }
    catch(e){
      print("Error canceling navigation: $e");
      Util.showSnackBar(context, 'Failed to cancel navigation');
    }
  }
}