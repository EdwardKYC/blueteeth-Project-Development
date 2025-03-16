import React, {useEffect, useRef} from "react";
import { useSelector } from "react-redux";
import { clearAllHistoryLogs } from "../../services/api";
import "./HistoryPage.css";

const HistoryPage = () => {
  const history = useSelector((state) => state.history);
  const consoleRef = useRef(null);
  const firstTime = useRef(0);

  useEffect(() => {
    if (consoleRef.current && (firstTime.current <= 1 || !document.hasFocus())) {
      consoleRef.current.scrollTop = consoleRef.current.scrollHeight;
      firstTime.current += 1;
    }
  }, [history.byId]);

  const handleClearAllHistory = async () => {
    try {
      await clearAllHistoryLogs(); 
    } catch (error) {
      console.error("Error clearing history logs:", error);
    }
  };

  return (
    <div className="history-page">
      <h1>History Logs</h1>
      <button className="clear-history-button" onClick={handleClearAllHistory}>
        Clear All History
      </button>
      <div className="console" ref={consoleRef}>
        {Object.values(history.byId).length > 0 ? (
          Object.values(history.byId).map((log) => (
            <div key={log.id} className="console-item">
              <span className="timestamp">
                {new Date(log.timestamp).toLocaleString()}
              </span>{" "}
              <span 
                className={`type ${
                  log.type === "warning"
                    ? "type-warning"
                    : log.type === "error"
                    ? "type-error"
                    : ""
                }`}
              >
                {log.type}
              </span>
              {" "}
              <span className="action">{log.action}</span> -{" "}
              <span className="details">
                {typeof log.details === "string"
                  ? log.details
                  : JSON.stringify(log.details, null, 2)}
              </span>
            </div>
          ))
        ) : (
          <p className="no-history">No history logs available</p>
        )}
      </div>
    </div>
  );
};

export default HistoryPage;