import React from "react";
import { useSelector } from "react-redux";
import "./BookListPage.css";
import { useNavigate } from "react-router-dom";

const BookListPage = () => {
  const books = useSelector((state) => state.books.byId);
const navigate = useNavigate();

  const handleBookClick = (id) => {
    navigate(`/books?bookId=${id}`);
  };

  return (
    <div className="book-page">
      <h1>Books</h1>
      <div className="book-list">
        {Object.values(books).length > 0 ? (
          Object.values(books).map((book) => (
            <div key={book.id} className="book-card" onClick={() => handleBookClick(book.id)}>
              <div className="book-card-top">
                <div className="book-header">
                  <h2>
                    {book.name}{" "}
                  </h2>
                  {book.device && (
                    <span className="device-tag">{book.device.id}</span>
                  )}
                </div>
                {book.description ? (
                  <p className="book-description">{book.description}</p>
                ) : (
                 <p className="book-description">此書暫無描述</p>
                )}
              </div>

              <div className="book-users">
                    {book.users && book.users.length > 0 ? (
                    <p>{book.users.length} users reading this book</p>
                    ) : (
                    <p>No users linked to this book</p>
                    )}
                </div>
            </div>
          ))
        ) : (
          <p>No books available</p>
        )}
      </div>
    </div>
  );
};

export default BookListPage;