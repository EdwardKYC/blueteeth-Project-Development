import React, { useState } from "react";
import { useSelector } from "react-redux";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faChevronDown, faChevronRight, faArrowUp, faArrowDown, faArrowLeft, faArrowRight } from "@fortawesome/free-solid-svg-icons";
import "./RaspPage.css";

const directionIcons = {
  UP: faArrowUp,
  DOWN: faArrowDown,
  LEFT: faArrowLeft,
  RIGHT: faArrowRight,
};

const RaspPage = () => {
  const rasps = useSelector((state) => state.rasps.byId);
  const [expandedRasp, setExpandedRasp] = useState(null);

  const toggleExpand = (raspId) => {
    setExpandedRasp((prev) => (prev === raspId ? null : raspId));
  };

  return (
    <div className="rasp-page">
      {Object.keys(rasps).length === 0 ? (
        <h1>No Raspberries Available</h1>
      ) : (
        <>
          <h1>Raspberries</h1>
          <div className="rasp-list">
            {Object.values(rasps).map((rasp) => (
              <div key={rasp.id} className="rasp-card" onClick={() => toggleExpand(rasp.id)}>
                <div className="rasp-card-header">
                  <div className="rasp-card-profile">
                    <div className={`profile-circle ${rasp.facing?.charAt(0).toLowerCase()}`}>
                      {rasp.facing?.charAt(0)}
                    </div>
                    <div className="rasp-info">
                      <h2>{rasp.id}</h2>
                      <p>
                        at ({rasp.cords?.x || 0}, {rasp.cords?.y || 0})
                      </p>
                    </div>
                  </div>
                  <button className="expand-button">
                    <FontAwesomeIcon icon={expandedRasp === rasp.id ? faChevronDown : faChevronRight} />
                  </button>
                </div>
                {expandedRasp === rasp.id && (
                  <div className="rasp-card-body">
                    {rasp.users && rasp.users.length > 0 ? (
                      <ul className="user-list">
                        {rasp.users.map((user) => (
                          <li key={user.name} className="user-item">
                            <FontAwesomeIcon
                              className="user-direction"
                              icon={directionIcons[user.direction]}
                            />
                            <span className="user-name">{user.name}</span>
                          </li>
                        ))}
                      </ul>
                    ) : (
                      <p>No users linked to this Rasp</p>
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
};

export default RaspPage;