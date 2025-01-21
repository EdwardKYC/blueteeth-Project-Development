import { useState, useEffect } from 'react';

export const useSidebarState = () => {
  const [isSidebarExpanded, setIsSidebarExpanded] = useState(false);

  // Toggle Sidebar function
  const toggleSidebar = () => {
    setIsSidebarExpanded(!isSidebarExpanded);
  };

  // Effect to automatically collapse the sidebar when switching to mobile mode
  useEffect(() => {
    const mediaQuery = window.matchMedia('(max-width: 768px)');

    const handleMediaChange = (e) => {
      if (e.matches) {
        setIsSidebarExpanded(false); // Collapse the sidebar in mobile view
      } else {
        setIsSidebarExpanded(false);
      }
    };

    // Use addEventListener instead of addListener
    mediaQuery.addEventListener('change', handleMediaChange);

    // Initial check for when component mounts
    handleMediaChange(mediaQuery);

    // Cleanup the event listener on unmount
    return () => {
      mediaQuery.removeEventListener('change', handleMediaChange);
    };
  }, []);

  return { isSidebarExpanded, toggleSidebar };
};