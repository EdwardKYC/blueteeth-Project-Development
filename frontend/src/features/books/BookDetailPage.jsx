import React from "react";
import { useSelector } from "react-redux";
import "./BookDetailPage.css";

const BookDetailPage = ({ bookId }) => {
  const book = useSelector((state) => state.books.byId[bookId]);

  if (!book) {
    return (
      <div className="book-detail-page">
        <h1>Book not found</h1>
      </div>
    );
  }

  return (
    <div className="book-detail-page">
      
      <div className="book-detail-info">
        <h1>{book.name}</h1>
        {book.device && (
            <div className="device-detail-tag ">{book.device.id}</div>
        )}
        {book.description && <p className="book-detail-description">{book.description}</p>}
      </div>
      
      <div className="book-detail-container">
        <div className="book-detail-card">
          <div className="book-detail-content-header">Users Reading This Book</div>
          <div className="book-detail-content">
            {book.users && book.users.length > 0 ? (
              book.users.map((user) => (
                <div key={user.name} className="book-detail-item">
                  <div className="book-detail-user-color-item">
                    <p className="book-detail-username">{user.name}</p>
                    <div
                      className="book-detail-user-color"
                      style={{ backgroundColor: user.color }}
                    />
                  </div>
                </div>
              ))
            ) : (
              <p className="book-no-data">No Users Linked</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default BookDetailPage;
