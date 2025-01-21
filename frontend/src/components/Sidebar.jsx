import React from 'react';
import { NavLink } from 'react-router-dom';
import { SidebarData } from '../routes/SidebarData'; 
import './Sidebar.css'; 

const Sidebar = ({ isExpanded, toggleSidebar }) => {

  // Handle item click and only toggle on small screens
  const handleItemClick = () => {
    if (window.innerWidth < 768) { // Only toggle on mobile/tablet screen sizes
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
            <li key={key} className="sidebar-item" onClick={handleItemClick}>
              <NavLink to={val.link} className={({ isActive }) => (isActive ? 'active' : '')}>
                <div className="icon">{val.icon}</div>
                {isExpanded && <div className="title">{val.title}</div>}
              </NavLink>
            </li>
          ))}
        </ul>
      </div>
    </>
  );
};

export default Sidebar;