import React from "react";
import { useSelector } from "react-redux";
import "./BookPage.css";

const BookPage = () => {
  const books = useSelector((state) => state.books.byId);

  return (
    <div className="book-page">
      <h1>Books</h1>
      <div className="book-list">
        {Object.values(books).length > 0 ? (
          Object.values(books).map((book) => (
            <div key={book.id} className="book-card">
              <div className="book-card-top">
                <div className="book-header">
                  <h2>
                    {book.name}{" "}
                  </h2>
                  {book.device && (
                    <span className="device-tag">{book.device.id}</span>
                  )}
                </div>
                {book.description && (
                  <p className="book-description">{book.description}</p>
                )}

              </div>

              <div className="book-users">
                {book.users && book.users.length > 0 ? (
                  <p>{book.users.map((user) => user.name).join(", ")}</p>
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

export default BookPage;