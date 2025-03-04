import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  byName: {},
};

const userSlice = createSlice({
  name: "users",
  initialState,
  reducers: {
    insertUser(state, action) {
      const { userName } = action.payload;

      // 确保用户不重复插入
      if (state.byName[userName]) return;

      state.byName[userName] = {
        userName,
        device: null,
        rasps: [],
      };
    },
    addBookToUser(state, action) {
      const { userName, bookId, bookName } = action.payload;

      const user = state.byName[userName];
      if (user) {
        user.book = { id: bookId, name: bookName }; 
      }
    },
    addDeviceToUser(state, action) {
      const { deviceId, userName, color } = action.payload;

      const user = state.byName[userName];
      if (user) {
        user.device = { id: deviceId, color }; 
      }
    },
    addRaspToUser(state, action) {
      const { userName, raspId, direction } = action.payload;

      const user = state.byName[userName];
      if (user) {
        const raspExists = user.rasps.some((rasp) => rasp.id === raspId);
        if (!raspExists) {
          user.rasps.push({ id: raspId, direction });
        }
      }
    },
    clearUserNavigation(state, action) {
      const { userName } = action.payload;

      const user = state.byName[userName];
      if (user) {
        user.device = null; 
        user.rasps = [];
        user.book = null;
      }
    },
    removeUser(state, action) {
      const { userName } = action.payload;
      if (state.byName[userName]) {
        delete state.byName[userName];
      }
    },
  },
});

export const { insertUser, addBookToUser, addDeviceToUser, addRaspToUser, clearUserNavigation, removeUser } =
  userSlice.actions;

export default userSlice.reducer;