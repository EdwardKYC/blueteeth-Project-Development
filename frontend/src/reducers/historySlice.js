import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  byId: {},
};

const historySlice = createSlice({
  name: "history",
  initialState,
  reducers: {
    insertHistory(state, action) {
      const { id, type, action: logAction, timestamp, details } = action.payload;

      if (state.byId[id]) return; 

      state.byId[id] = { id, type, action: logAction, timestamp, details };
    },
    clearHistory(state) {
      state.byId = {};
    },
  },
});

export const { insertHistory, clearHistory } = historySlice.actions;
export default historySlice.reducer;