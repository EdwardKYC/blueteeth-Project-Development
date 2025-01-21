import { configureStore } from "@reduxjs/toolkit";
import userReducer from "../reducers/userSlice";
import deviceReducer from "../reducers/deviceSlice";
import raspReducer from "../reducers/raspSlice";
import bookReducer from "../reducers/bookSlice";
import historyReducer from "../reducers/historySlice";

const store = configureStore({
  reducer: {
    users: userReducer,
    devices: deviceReducer,
    rasps: raspReducer,
    books: bookReducer,
    history: historyReducer,
  },
});

export default store;