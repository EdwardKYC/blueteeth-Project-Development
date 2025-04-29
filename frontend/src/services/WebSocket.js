import { 
	handleAddDeviceColor,
	handleAddHistoryLog,
	handleAddRaspDirection,
	handleCancelNavigation,
	handleClearAllHistory,
	handleNavigateBook,
	handleRegisterBook,
	handleRegisterDevice,
	handleRegisterRasp,
	handleRegisterUser,
	handleUpdateDeviceBattery,
	handleRemoveUser,
	handleToggleDeviceStatus,
	handleToggleRaspStatus,
	handleAddBorrowHistory
} from "./helper";
import { WS_URL } from '../config';

let socket = null;
let reconnectInterval = 5000;

export const initializeWebSocket = () => {
	socket = new WebSocket(`${WS_URL}/api/v1/ws`);

	socket.onmessage = (event) => {
		const message = JSON.parse(event.data);
		handleWebSocketMessage(message);
	};

	socket.onopen = () => {
		console.log("WebSocket connection established");
	};

	socket.onerror = (error) => {
		console.error("WebSocket Error:", error);
	};

	socket.onclose = () => {
        console.log("WebSocket connection closed. Attempting to reconnect in 5 seconds...");
        setTimeout(() => {
            console.log("Reconnecting...");
            initializeWebSocket();
        }, reconnectInterval);
    };
};

const handleWebSocketMessage = (message) => {
	if (message.type == "add_device_color") {
		handleAddDeviceColor(message.payload);
	} else if (message.type == "cancel_navigation") {
		handleCancelNavigation(message.payload);
	} else if (message.type == "add_rasp_direction") {
		handleAddRaspDirection(message.payload);
	} else if (message.type == "navigate_book") {
		handleNavigateBook(message.payload);
	} else if (message.type === "add_history_log") {
		handleAddHistoryLog(message.payload);
	} else if (message.type === "clear_all_history") {
		handleClearAllHistory();
	} else if (message.type === "update_device_battery") {
		handleUpdateDeviceBattery(message.payload);
	} else if (message.type === "register_device") {
		handleRegisterDevice(message.payload);
	} else if (message.type === "register_book") {
		handleRegisterBook(message.payload);
	} else if (message.type === "register_rasp") {
		handleRegisterRasp(message.payload);
	} else if (message.type === "register_user") {
		handleRegisterUser(message.payload);
	} else if (message.type === "remove_user") {
		handleRemoveUser(message.payload);
	} else if (message.type === "toggle_rasp_status") {
		handleToggleRaspStatus(message.payload);
	} else if (message.type === "toggle_device_status") {
		handleToggleDeviceStatus(message.payload);
	} else if (message.type === "add_book_history") {
		handleAddBorrowHistory(message.payload);
	}
};
