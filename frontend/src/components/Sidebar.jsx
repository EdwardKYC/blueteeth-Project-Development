import React, { useState } from 'react';
import { NavLink } from 'react-router-dom';
import { SidebarData } from '../routes/SidebarData'; 
import './Sidebar.css'; 

const Sidebar = ({ isExpanded, toggleSidebar }) => {
  const [hoveredItem, setHoveredItem] = useState(null);
  const [showTooltip, setShowTooltip] = useState(false);
  let hoverTimeout = null; 

  const handleMouseEnter = (key) => {
    if (!isExpanded) {
      hoverTimeout = setTimeout(() => {
        setHoveredItem(key);
        setShowTooltip(true);
      }, 500); 
    }
  };

  const handleMouseLeave = () => {
    clearTimeout(hoverTimeout);
    setShowTooltip(false);
    setHoveredItem(null);
  };

  const handleItemClick = () => {
    if (window.innerWidth < 768) { 
      toggleSidebar();
    }
  };

  return (
    <>
      {/* Overlay, only visible on mobile when sidebar is expanded */}
      {isExpanded && window.innerWidth < 768 && <div className="overlay" onClick={toggleSidebar}></div>}

      <div className={`sidebar ${isExpanded ? 'expanded' : 'collapsed'}`}>
        <ul className="sidebar-list">
          {SidebarData.map((val, key) => (
            <li 
              key={key} 
              className="sidebar-item" 
              onMouseEnter={() => handleMouseEnter(key)} 
              onMouseLeave={handleMouseLeave}
              onClick={() => {
                handleItemClick();
              }}
            >
              <NavLink to={val.link} className={({ isActive }) => (isActive ? 'active' : '')}>
                <div className="icon">{val.icon}</div>
                {isExpanded && <div className="title">{val.title}</div>}
                {!isExpanded && showTooltip && hoveredItem === key && (
                  <div className="tooltip">{val.title}</div>
                )}
              </NavLink>
            </li>
          ))}
        </ul>
      </div>
    </>
  );
};

export default Sidebar;