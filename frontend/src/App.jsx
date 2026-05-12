import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import PrivateRoute from './components/PrivateRoute';
import LoginPage from './pages/LoginPage';
import WelcomePage from './pages/WelcomePage';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route
          path="/welcome"
          element={
            <PrivateRoute>
              <WelcomePage />
            </PrivateRoute>
          }
        />
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
