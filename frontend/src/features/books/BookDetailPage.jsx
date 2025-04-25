import React, { useState } from "react";
import { useSelector } from "react-redux";
import "./BookDetailPage.css";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'; 
import { faArrowLeft, faClockRotateLeft, faTimes, faUser } from '@fortawesome/free-solid-svg-icons'; 
import { useNavigate } from "react-router-dom";

const BookDetailPage = ({ bookId }) => {
  const book = useSelector((state) => state.books.byId[bookId]);
  const navigate = useNavigate();
  const [showHistory, setShowHistory] = useState(false);

  const getColorPair = (color) => {
    const colorMap = {
      "#ed2939": { background: "#ffe5e7", foreground: "#db5c71" }, // 淡粉紅 / 深紅
      "#fb9417": { background: "#faeed4", foreground: "#fb9417" }, // 淡黃 / 橘黃
      "#0b6623": { background: "#e1f3e6", foreground: "#069910" }, // 淡綠 / 深綠
      "#1338be": { background: "#e3e9fb", foreground: "#0077e6" }, // 淡藍 / 深藍
      "#8a00c2": { background: "#f3e6fc", foreground: "#9725ba" }, // 淡紫 / 深紫
      "#18848e": { background: "#daf2f4", foreground: "#18848e" }, // 淺青 / 深青
    };
    return colorMap[color] || { background: "#eee", foreground: "#555" }; // fallback
  };

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
          <div className="book-detail-title-left">
            <h1>{book.name}</h1>
            <p className="book-id">ID: {bookId}</p>
          </div>
          <div className="book-detail-title-right">
            <button className="history-button" onClick={() => setShowHistory(true)}>
            <FontAwesomeIcon icon={faClockRotateLeft } />
          </button>
          </div>
        </div>
        {book.device && (
            <div className="device-detail-tag ">{book.device.id}</div>
        )}
        {book.description && <p className="book-detail-description">{book.description}</p>}
      </div>

      {showHistory && (
        <div className="modal-overlay" onClick={() => setShowHistory(false)}>
          <div className="modal-window" onClick={(e) => e.stopPropagation()}>
            <div className="borrow-history-header">
              <span>Navigation History</span>
              <FontAwesomeIcon icon={faTimes} className="modal-close-icon" onClick={() => setShowHistory(false)} />
            </div>
            <div className="borrow-history-body">
              {book.history.length === 0 ? (
                <p className="borrow-history-no-data">No history found.</p>
              ) : (
                  book.history.map((entry, index) => (
                    <div key={entry.id} className="borrow-history-block">
                      {(() => {
                        const { background, foreground } = getColorPair(entry.color);
                        return (
                          <FontAwesomeIcon
                            icon={faUser}
                            style={{
                              backgroundColor: background,
                              color: foreground,
                            }}
                            className="borrow-history-block-user"
                          />
                        );
                      })()}
                      <div className="borrow-history-block-right">
                        <div className="borrow-history-block-text">
                          <div className="borrow-history-block-text-name">
                            {entry.username}
                          </div>
                          <div className="borrow-history-block-text-time">
                            {new Date(entry.timestamp).toLocaleString()}
                          </div>
                        </div>
                        {index !== book.history.length - 1 && (
                          <div className="borrow-history-divider" />
                        )}
                      </div>
                      
                    </div>
                  ))
              )}
            </div>
          </div>
        </div>
      )}
      
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
