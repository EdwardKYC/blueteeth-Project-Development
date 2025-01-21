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
  },
});

export const { insertBook, addUserToBook, addDeviceToBook, removeUserFromBook } = bookSlice.actions;
export default bookSlice.reducer;