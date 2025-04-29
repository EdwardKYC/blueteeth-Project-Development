import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  byId: {}, 
};

const bookSlice = createSlice({
  name: "books",
  initialState,
  reducers: {
    insertBook(state, action) {
      const { id, name, description } = action.payload;

      if (state.byId[id]) return;

      state.byId[id] = {
        id,
        name,
        description: description || "",
        history: [],
        users: [], 
        device: null, 
      };
    },
    addUserToBook(state, action) {
      const { userName, bookId } = action.payload;

      const book = state.byId[bookId];
      if (book) {
        const userExists = book.users.some((user) => user.name === userName);
        if (!userExists) {
          book.users.push({ name: userName });
        }
      }
    },
    addDeviceToBook(state, action) {
      const { deviceId, bookId } = action.payload;

      const book = state.byId[bookId];
      if (book) {
        book.device = { id: deviceId };
      }
    },
    removeUserFromBook(state, action) {
      const { userName, bookId } = action.payload;

      const book = state.byId[bookId];
      if (book) {
        book.users = book.users.filter((user) => user.name !== userName);
      }
    },
    addBorrowHistory(state, action) {
      const { id, bookId, userName, timestamp, color } = action.payload;

      const book = state.byId[bookId];
      if (book) {
        const historyExists = book.history.some((history) => history.id === id);
        if (!historyExists) {
          book.history.push({ id, username: userName, timestamp, color });
        }
      }
    },
  },
});

export const { insertBook, addUserToBook, addDeviceToBook, removeUserFromBook, addBorrowHistory } = bookSlice.actions;
export default bookSlice.reducer;