// src/config.js
const BASE_URL = import.meta.env.VITE_BASE_URL || `${window.location.origin}`;
const WS_URL = BASE_URL.replace(/^http/, "ws").replace(/\/$/, ""); 

export { BASE_URL, WS_URL };