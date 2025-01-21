import React from 'react';
import './AppBar.css'; 
import { useNavigate } from 'react-router-dom';

const AppBar = ({ toggleSidebar }) => {
  const navigate = useNavigate();

  const handleClick = () => {
    navigate('/');
    toggleSidebar();
  };

  return (
    <div className="app-bar">
      <button className="hamburger" onClick={toggleSidebar}>
        <div className="hamburger-line"></div>
        <div className="hamburger-line"></div>
        <div className="hamburger-line"></div>
      </button>
      <span className="app-bar-title" onClick={handleClick}>
        BLE Dashboard
      </span>
    </div>
  );
};

export default AppBar;