import { fetchUsers, fetchDevices, fetchRasps, fetchBooks, fetchHistoryLogs, fetchBorrowHistory } from "./api";
import { handleAddHistoryLog, handleRegisterBook, handleRegisterDevice, handleRegisterRasp, handleRegisterUser, handleAddBorrowHistory } from "./helper";

export const initializeStore = async () => {
    try {
        // Fetch and dispatch devices
        const devicesData = await fetchDevices();
        devicesData.forEach((device) => {
            handleRegisterDevice(device);
        });

        // Fetch and dispatch rasps
        const raspsData = await fetchRasps();
        raspsData.forEach((rasp) => {
            handleRegisterRasp(rasp);
        });

        const booksData = await fetchBooks();
        booksData.forEach((book) => {
            handleRegisterBook(book);
        });

        // Fetch and dispatch users
        const usersData = await fetchUsers();
        usersData.forEach((user) => {
            handleRegisterUser(user);
        });

        // Fetch and dispatch history logs
        const historyData = await fetchHistoryLogs();
        historyData.forEach((log) => {
            handleAddHistoryLog(log);
        });

        const borrowHistoryData = await fetchBorrowHistory();
        borrowHistoryData.forEach((history) => {
            handleAddBorrowHistory(history);
        });
    } catch (error) {
        console.error("Error initializing store:", error);
    }
};