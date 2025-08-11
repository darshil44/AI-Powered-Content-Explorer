import { useAuth } from "../context/AuthContext";
import { Navigate } from "react-router-dom";

export default function PrivateRoute({ children }) {
  const { user, loading } = useAuth();

  if (loading) return <p className="text-center mt-20">Loading...</p>;

  if (!user) return <Navigate to="/login" replace />;

  return children;
}
