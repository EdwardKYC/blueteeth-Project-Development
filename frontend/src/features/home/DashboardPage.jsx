import React from "react";
import { useSelector } from "react-redux";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faLightbulb,
  faUsers,
  faBook,
  faDesktop,
} from "@fortawesome/free-solid-svg-icons";
import "./DashboardPage.css";
import CountUp from "react-countup";

const DashboardPage = () => {
  const devicesCount = useSelector((state) => Object.keys(state.devices.byId).length);
  const usersCount = useSelector((state) => Object.keys(state.users.byName).length);
  const booksCount = useSelector((state) => Object.keys(state.books.byId).length);
  const raspsCount = useSelector((state) => Object.keys(state.rasps.byId).length);

  const overviewData = [
    { icon: faLightbulb, label: "Devices", count: devicesCount, backgroundColor: "#fbe4e6",  foregroundColor: "#f49aa1"},
    { icon: faUsers, label: "Users", count: usersCount, backgroundColor: "#f5e7cb",  foregroundColor: "#e9a42c"},
    { icon: faBook, label: "Books", count: booksCount, backgroundColor: "#eaf4fb",  foregroundColor: "#5dade6" },
    { icon: faDesktop, label: "Rasps", count: raspsCount, backgroundColor: "#e8fbee",  foregroundColor: "#4ac06f" },
  ];

  return (
    <div className="dashboard-page">
      <h1>Dashboard Overview</h1>
      <div className="overview-grid">
        {overviewData.map((data, index) => (
          <div key={index} className="overview-card">
            <div 
              className="overview-icon"
              style={{
                backgroundColor: data.backgroundColor,
                color: data.foregroundColor
              }}
            >
              <FontAwesomeIcon
                icon={data.icon}
              />
            </div>
            
            <div className="overview-count">
              <CountUp
                start={0}
                end={data.count} 
                duration={1}
                separator=","
              />
            </div>
            <div className="overview-label">
              {data.label}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default DashboardPage;