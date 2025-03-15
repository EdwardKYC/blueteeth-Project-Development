import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  byId: {},
};

const deviceSlice = createSlice({
  name: "devices",
  initialState,
  reducers: {
    insertDevice(state, action) {
      const { id, status, battery, cords } = action.payload;

      if (state.byId[id]) return;

      state.byId[id] = { id, status, battery, cords, books: [], users: [] };
    },
    addBookToDevice(state, action) {
      const { deviceId, bookId, bookName } = action.payload;

      const device = state.byId[deviceId];
      if (device) {
        const bookExists = device.books.some((book) => book.id === bookId);

        if (!bookExists) {
          device.books.push({ id: bookId, name: bookName });
        }
      }
    },
    addRaspToDevice(state, action) {
      const { deviceId, raspId } = action.payload;

      const device = state.byId[deviceId];
      if (device) {
        device.rasp_id = raspId; 
      }
    },
    addUserToDevice(state, action) {
      const { deviceId, userName, color } = action.payload;

      const device = state.byId[deviceId];
      if (device) {
        const userExists = device.users.some((user) => user.name === userName);

        if (!userExists) {
          device.users.push({ name: userName, color });
        }
      }
    },
    removeUserFromDevice(state, action) {
      const { deviceId, userName } = action.payload;

      const device = state.byId[deviceId];
      if (device) {
        device.users = device.users.filter((user) => user.name !== userName);
      }
    },
    updateDeviceBattery(state, action) {
      const { deviceId, battery } = action.payload;

      const device = state.byId[deviceId];
      if (device) {
        device.battery = battery;
      }
    },
    toggleDeviceStatus(state, action) {
      const { deviceId, status } = action.payload;

      const device = state.byId[deviceId];
      if (device) {
        device.status = status;
      }
    }
  },
});

export const { insertDevice, addBookToDevice, addRaspToDevice, addUserToDevice, removeUserFromDevice, updateDeviceBattery, toggleDeviceStatus } = deviceSlice.actions;
export default deviceSlice.reducer;