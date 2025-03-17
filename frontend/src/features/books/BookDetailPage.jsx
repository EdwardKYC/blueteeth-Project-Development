import React from "react";
import { useSelector } from "react-redux";
import "./BookDetailPage.css";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'; 
import { faArrowLeft } from '@fortawesome/free-solid-svg-icons'; 
import { useNavigate } from "react-router-dom";

const BookDetailPage = ({ bookId }) => {
  const book = useSelector((state) => state.books.byId[bookId]);
  const navigate = useNavigate();

  if (!book) {
    return (
      <div className="book-detail-page">
        <h1>Book not found</h1>
      </div>
    );
  }

  const hasShortDescription = !book.description || book.description.length < 20;

  return (
    <div className={`book-detail-page ${hasShortDescription ? "column-layout" : ""}`}>
      <div className="book-detail-info">
        <button className="book-detail-back-button" onClick={() => navigate(-1)}>
          <FontAwesomeIcon icon={faArrowLeft} className="book-detail-back-icon"/> Back
        </button>
        <div className="book-detail-title">
          <h1>{book.name}</h1>
          <p className="book-id">ID: {bookId}</p>
        </div>
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
