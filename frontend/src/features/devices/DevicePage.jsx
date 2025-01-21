import React from "react";
import { useLocation } from "react-router-dom";
import DeviceDetailPage from "./DeviceDetailPage";
import DeviceListPage from "./DeviceListPage";

const DevicePage = () => {
  const location = useLocation();
  const queryParams = new URLSearchParams(location.search);
  const deviceId = queryParams.get("deviceId");

  return deviceId ? <DeviceDetailPage deviceId={deviceId} /> : <DeviceListPage />;
};

export default DevicePage;