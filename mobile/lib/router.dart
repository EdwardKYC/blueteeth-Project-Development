import 'package:flutter/material.dart';
import 'package:mobile/view/LoginPage.dart';
import 'package:mobile/view/RegisterPage.dart';
import 'package:mobile/view/BookSearchPage.dart';
import 'package:mobile/view/ResultPage.dart';
import 'package:mobile/view/BookDetails.dart';

class router {
  static const String login = '/login';
  static const String register = '/register';
  static const String search = '/search';
  static const String result = '/result';
  static const String bookDetails = '/bookDetails';

  static Map<String, WidgetBuilder> getRoutes() {
    return {
      login: (context) => const Login(),
      register: (context) => const Register(),
      search: (context) => const Search(),
      result: (context) => const Result(),
      bookDetails: (context) => const BookDetails(),
    };
  }
}
