import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Search from "./pages/Search";
import ImageGen from "./pages/ImageGen";
import Dashboard from "./pages/Dashboard";
import { AuthProvider } from "./context/AuthContext";
import ProtectedRoute from "./components/ProtectedRoute";
import PrivateRoute from "./components/PrivateRoute";

export default function App() {
  return (
    <AuthProvider>
      <Router>
            <Header />
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />

          {/* Protected routes */}
          <Route
            path="/search"
            element={
              <ProtectedRoute>
                <Search />
              </ProtectedRoute>
            }
          />
          <Route
            path="/imagegen"
            element={
              <ProtectedRoute>
                <ImageGen />
              </ProtectedRoute>
            }
          />
          <Route
  path="/dashboard"
  element={
    <PrivateRoute>
      <Dashboard />
    </PrivateRoute>
  }
/>


          {/* Redirect all other routes */}
          <Route path="*" element={<Navigate to="/login" replace />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}
