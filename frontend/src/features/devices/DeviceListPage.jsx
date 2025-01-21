import React from "react";
import { useSelector } from "react-redux";
import DeviceCard from "./DeviceCard";
import "./DeviceListPage.css";

const DevicePage = () => {
  const devices = useSelector((state) => state.devices.byId);

  return (
    <div className="device-page">
      {Object.keys(devices).length === 0 ? (
        <h1>No devices available</h1>
      ) : (
        <>
          <h1>Devices</h1>
          <div className="device-list">
            {Object.values(devices).map((device) => (
              <DeviceCard key={device.id} device={device} />
            ))}
          </div>
        </>
      )}
    </div>
  );
};

export default DevicePage;