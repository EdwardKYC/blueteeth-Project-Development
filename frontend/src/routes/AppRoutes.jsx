import { Routes, Route } from "react-router-dom";
import RaspPage from "../features/rasps/RaspPage";
import UserPage from "../features/users/UserPage";
import DevicePage from "../features/devices/DevicePage";
import BookPage from "../features/books/BookPage";
import HistoryPage from "../features/history/HistoryPage";
import DashboardPage from "../features/home/DashboardPage";
import NotFoundPage from "../features/NotFoundPage";

const AppRoutes = () => {
  return (
    <Routes>
      <Route path="/" element={<DashboardPage />} />
      <Route path="/rasps" element={<RaspPage />} />
      <Route path="/books" element={<BookPage />} />
      <Route path="/users" element={<UserPage />} />
      <Route path="/devices" element={<DevicePage />} />
      <Route path="/history" element={<HistoryPage />} />
      <Route path="*" element={<NotFoundPage />} />
    </Routes>
  );
};

export default AppRoutes;