import { BrowserRouter as Router } from "react-router-dom";
import { Provider } from "react-redux";
import store from './store/index';
import { initializeStore } from './services/storeInitializer';
import { useEffect } from "react";
import { initializeWebSocket } from "./services/WebSocket";
import { useSidebarState } from "./routes/SidebarState"

import AppRoutes from "./routes/AppRoutes";
import Sidebar from "./components/Sidebar";
import AppBar from "./components/AppBar";
import "./App.css"

function App() {
  useEffect(() => {
    initializeWebSocket();
    initializeStore();
  }, []);

  const { isSidebarExpanded, toggleSidebar } = useSidebarState();

  return (
    <Provider store={store}>
      <Router>
        <div className="app-container">
          <AppBar toggleSidebar={toggleSidebar} />
          <div className="content-wrapper">
            <Sidebar isExpanded={isSidebarExpanded} toggleSidebar={toggleSidebar} /> 
            <div className="content">
              <AppRoutes />
            </div>
          </div>
        </div>
      </Router>
    </Provider>
  );
}

export default App
