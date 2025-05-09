import store from "../store/index";
import {
    insertDevice,
    addRaspToDevice,
    addUserToDevice,
    addBookToDevice,
    removeUserFromDevice,
    updateDeviceBattery,
    toggleDeviceStatus
} from "../reducers/deviceSlice";
import {
    insertRasp,
    addUserToRasp,
    removeUserFromRasp,
    toggleRaspStatus
} from "../reducers/raspSlice";
import {
    insertUser,
    addBookToUser,
    addDeviceToUser,
    addRaspToUser,
    clearUserNavigation,
	removeUser
} from "../reducers/userSlice";
import {
    insertBook,
    addDeviceToBook,
    addUserToBook,
    removeUserFromBook,
    addBorrowHistory
} from "../reducers/bookSlice";
import { insertHistory, clearHistory } from "../reducers/historySlice";

export const handleNavigateBook = ({ book_id, book_name, username }) => {
	// Dispatch actions to update User and Book in Redux
	store.dispatch(addBookToUser({ userName: username, bookId: book_id, bookName: book_name }));
	store.dispatch(addUserToBook({ userName: username, bookId: book_id }));
};

export const handleAddDeviceColor = ({ username, device_id, color }) => {
	// Dispatch actions to update User and Device in Redux
	store.dispatch(addDeviceToUser({ userName: username, deviceId: device_id, color: color }));
	store.dispatch(addUserToDevice({ userName: username, deviceId: device_id, color: color }));
};

export const handleAddRaspDirection = ({ rasp_id, username, direction, color }) => {
	// Dispatch actions to update User and Rasp in Redux
	store.dispatch(addRaspToUser({ userName: username, raspId: rasp_id, direction: direction, color: color }));
	store.dispatch(addUserToRasp({ userName: username, raspId: rasp_id, direction: direction, color: color }));
};

export const handleCancelNavigation = ({ username }) => {
	const state = store.getState();
	const user = state.users.byName[username];

	if (!user) return;

	const deviceId = user.device?.id;
	const bookId = user.book?.id;
	const rasps = user.rasps || [];

	// Dispatch 清除 User 的導航狀態
	store.dispatch(clearUserNavigation({ userName: username }));

	// Dispatch 移除 Book 中的 User
	if (bookId) {
		store.dispatch(removeUserFromBook({ bookId, userName: username }));
	}

	// Dispatch 移除 Device 中的 User
	if (deviceId) {
		store.dispatch(removeUserFromDevice({ deviceId: deviceId, userName: username }));
	}

	// Dispatch 移除 Rasp 中的 User
	rasps.forEach(({ id }) => {
		store.dispatch(removeUserFromRasp({ raspId: id, userName: username }));
	});
};

export const handleAddHistoryLog = ({ id, type, action, timestamp, details }) => {
	if (!id || !type || !action) {
		console.warn("Incomplete history log data", id, type, action);
		return;
	}
	store.dispatch(insertHistory({ id, type, action, timestamp, details }));
};

export const handleClearAllHistory = () => {
	store.dispatch(clearHistory());
};

export const handleRegisterDevice = ({ id, status, battery, cords, rasp_id }) => {
    if (!id || !status || !battery || !cords) {
        console.warn("Incomplete device data:", id, status, battery, cords, rasp_id);
        return;
    }
	store.dispatch(insertDevice({ id, status, battery, cords }));

	if (rasp_id) {
		store.dispatch(addRaspToDevice({ deviceId: id, raspId: rasp_id }))
	}
};

export const handleRegisterRasp = ({ id, status, cords, facing }) => {
    if (!id || !status || !cords || !facing) {
        console.warn("Incomplete rasp data:", id, status, cords, facing);
        return;
    }
	store.dispatch(insertRasp({ id, status, cords, facing }));
};

export const handleToggleRaspStatus = ({ id, status }) => {
    if (!id || !status) {
		console.warn("Incomplete rasp data:", id, status);
		return;
	}

	store.dispatch(toggleRaspStatus({ raspId: id, status }));
};

export const handleToggleDeviceStatus = ({ id, status }) => {
    if (!id || !status) {
		console.warn("Incomplete device data:", id, status);
		return;
	}

	store.dispatch(toggleDeviceStatus({ deviceId: id, status }));
};

export const handleRegisterBook = ({ id, name, description, device_id }) => {
	if (!id || !name) {
		console.warn("Incomplete book data:", id, name);
		return;
	}

	store.dispatch(insertBook({ id, name, description }));

	if (device_id) {
		store.dispatch(addDeviceToBook({ deviceId: device_id, bookId: id }));
        store.dispatch(addBookToDevice({ deviceId: device_id, bookName: name , bookId: id }));
	}
};

export const handleRegisterUser = ({ username, book, device, rasps = [] }) => {
    if (!username) {
        console.warn("Incomplete user data:", username);
        return;
    }

    store.dispatch(insertUser({ userName: username }));

    if (book && book.id && book.name) {
        store.dispatch(addBookToUser({ userName: username, bookId: book.id, bookName: book.name }));
        store.dispatch(addUserToBook({ userName: username, bookId: book.id }));
    }

    if (device && device.id && device.color) {
        store.dispatch(addDeviceToUser({ userName: username, deviceId: device.id, color: device.color }));
        store.dispatch(addUserToDevice({ userName: username, deviceId: device.id, color: device.color }));
    }

    rasps.forEach(({ id, direction, color }) => {
        if (!id || !direction || !color) {
            console.warn("Incomplete rasp link for user:", username, id, direction, color);
            return;
        }
        store.dispatch(addRaspToUser({ userName: username, raspId: id, direction }));
        store.dispatch(addUserToRasp({ raspId: id, userName: username, direction, color }));
    });
};

export const handleUpdateDeviceBattery = ({ device_id, battery }) => {
    if (!device_id || !battery) {
		console.warn("Incomplete device data:", device_id, battery);
		return;
	}

	store.dispatch(updateDeviceBattery({ deviceId: device_id, battery }));
};

export const handleRemoveUser = ({ username }) => {
    const state = store.getState();
    const user = state.users.byName[username];

    if (!user) return;

    const deviceId = user.device?.id;
    const bookId = user.book?.id;
    const rasps = user.rasps || [];

    store.dispatch(removeUser({ userName: username }));

    if (bookId) {
        store.dispatch(removeUserFromBook({ bookId, userName: username }));
    }

    if (deviceId) {
        store.dispatch(removeUserFromDevice({ deviceId, userName: username }));
    }

    rasps.forEach(({ id }) => {
        store.dispatch(removeUserFromRasp({ raspId: id, userName: username }));
    });
};

export const handleAddBorrowHistory = ({ id, book_id, username, timestamp, color }) => {
	if (!id || !book_id || !username || !timestamp || !color) {
		console.warn("Incomplete borrow history data", id, book_id, username, timestamp, color);
		return;
	}
	store.dispatch(addBorrowHistory({ id, bookId: book_id, userName: username, timestamp: timestamp, color }));
};