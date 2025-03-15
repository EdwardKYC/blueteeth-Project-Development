import React from "react";
import { CircularProgressbar, buildStyles } from "react-circular-progressbar";
import "react-circular-progressbar/dist/styles.css";
import { useNavigate } from "react-router-dom";

const DeviceCard = ({ device }) => {
  const navigate = useNavigate();

  const handleCardClick = () => {
    navigate(`/devices?deviceId=${device.id}`);
  };

  const getBatteryColor = (battery) => {
    if (battery <= 20) {
      return "#ff1c3e";
    } else if (battery <= 50) {
      return "#fadb14";
    } else if (battery <= 80) {
      return "#52c41a"; 
    } else {
      return "#64edd2";
    }
  }
  const batteryColor = getBatteryColor(device.battery);

  return (
    <div className="device-card" onClick={handleCardClick}>
      <div className="device-card-left">
        <h2>{device.id}</h2>
        <p>Coordanates: ({device.cords.x}, {device.cords.y})</p>
        <div className="device-status-bar">
          <span className="device-rasp">{device.rasp_id || "No Rasp Linked"}</span>
          <div className="device-status">
              <span className={`device-status-text ${device.status}`}>{device.status}</span>
          </div>
        </div>
        
      </div>
      <div className="device-card-right">
        <div
          className="circular-progress-container"
        >
          <CircularProgressbar
            className="circular-progressbar"
            value={device.battery}
            text={`${device.battery}%`}
            styles={buildStyles({
              textColor: batteryColor, 
              pathColor: batteryColor,
              trailColor: "#ddd",
            })}
          />
        </div>
      </div>
    </div>
  );
};

export default DeviceCard;