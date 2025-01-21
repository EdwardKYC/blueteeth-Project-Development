import { BASE_URL } from '../config';

export const fetchDevices = async () => {
  const response = await fetch(`${BASE_URL}/api/v1/rasp/get-all-devices`);
  return await response.json();
};

export const fetchRasps = async () => {
  const response = await fetch(`${BASE_URL}/api/v1/rasp/get-all-rasps`);
  return await response.json();
};

export const fetchUsers = async () => {
  const response = await fetch(`${BASE_URL}/api/v1/users/get-all-users`);
  return await response.json();
};

export const fetchBooks = async () => {
  const response = await fetch(`${BASE_URL}/api/v1/books/get-all-books`);
  return await response.json();
};

export const fetchHistoryLogs = async () => {
  const response = await fetch(`${BASE_URL}/api/v1/history/get-all-history`);
  if (!response.ok) {
    throw new Error("Failed to fetch history logs");
  }
  return await response.json();
};

export const clearAllHistoryLogs = async () => {
  const response = await fetch(`${BASE_URL}/api/v1/history/clear-logs`, {
    method: "DELETE",
  });
  if (!response.ok) {
    throw new Error("Failed to clear history logs");
  }
  return { message: "All history logs cleared successfully." };
};