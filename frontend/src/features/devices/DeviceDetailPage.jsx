import React from "react";
import { useSelector } from "react-redux";
import "./DeviceDetailPage.css";

const DeviceDetailPage = ({ deviceId }) => {
  const device = useSelector((state) => state.devices.byId[deviceId]);

  if (!device) {
    return (
      <div className="device-detail-page">
        <h1>
        Device not found
        </h1>
      </div>
    );
  }

  return (
    <div className="device-detail-page">
      <h1>Details of {device.id}</h1>
      <div className="detail-container">
        <div className="detail-card">
          <div className="detail-content-header">
            Users
          </div>
          <div className="detail-content">
            {device.users && device.users.length > 0 ? (
              device.users.map((user) => (
                <div
                  key={user.name}
                  className="detail-item"
                >
                  <div className="detail-user-color-item">
                    <p className="detail-username">
                      {user.name}
                    </p>
                    <div 
                      className="detail-user-color" 
                      style={{
                        backgroundColor: user.color
                      }}
                    />
                  </div>
                </div>
              ))
            ) : (
              <p className="no-data">No Users Linked</p>
            )}
          </div>
        </div>
        <div className="detail-card">
          <div className="detail-content-header">
            Books
          </div>
          <div className="detail-content">
            {device.books && device.books.length > 0 ? (
              device.books.map((book) => (
                <div key={book.id} className="detail-item">
                  {book.name}
                </div>
              ))
            ) : (
              <p className="no-data">No Books Found</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default DeviceDetailPage;