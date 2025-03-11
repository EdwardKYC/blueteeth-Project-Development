class Book{
  late int id;
  late String name;
  late String description;
  Book({required this.id ,required this.name, required this.description});
  factory Book.fromJson(Map<String, dynamic> json) {
    return Book(
      id: json['id'],
      name: json['name'],
      description: json['description'],
    );
  }
}