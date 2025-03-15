import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  byId: {},
};

const raspSlice = createSlice({
  name: "rasps",
  initialState,
  reducers: {
    insertRasp(state, action) {
      const { id, status, cords, facing } = action.payload;

      if (state.byId[id]) return; 

      state.byId[id] = { id, status, cords, facing, users: [] };
    },
    removeUserFromRasp(state, action) {
      const { raspId, userName } = action.payload;

      const rasp = state.byId[raspId];
      if (!rasp) return;

      rasp.users = rasp.users.filter((user) => user.name !== userName);
    },
    addUserToRasp(state, action) {
      const { raspId, userName, direction, color } = action.payload;

      const rasp = state.byId[raspId] || { id: raspId, users: [] };

      const userExists = rasp.users.some((user) => user.name === userName);
      if (!userExists) {
        rasp.users.push({ name: userName, direction, color });
      }

      state.byId[raspId] = rasp; 
    },
    toggleRaspStatus(state, action) {
      const { raspId, status } = action.payload;

      const rasp = state.byId[raspId]
      if (!rasp) return

      rasp.status = status
    }
  },
});

export const { insertRasp, removeUserFromRasp, addUserToRasp, toggleRaspStatus } = raspSlice.actions;
export default raspSlice.reducer;