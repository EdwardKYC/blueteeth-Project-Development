import React from "react";
import { useLocation } from "react-router-dom";
import BookDetailPage from "./BookDetailPage";
import BookListPage from "./BookListPage";

const BookPage = () => {
  const location = useLocation();
  const queryParams = new URLSearchParams(location.search);
  const bookId = queryParams.get("bookId");

  return bookId ? <BookDetailPage bookId={bookId} /> : <BookListPage />;
};

export default BookPage;