import React, { createContext, useState, useEffect, useContext } from "react";
import api from "../api/axios";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // Check if user is logged in on mount
  useEffect(() => {
    async function checkAuth() {
      try {
        // Call a backend endpoint to get user info or verify token
        const res = await api.get("/auth/me");
        setUser(res.data);
      } catch {
        setUser(null);
      } finally {
        setLoading(false);
      }
    }
    checkAuth();
  }, []);

  const login = (userData) => setUser(userData);
  const logout = async () => {
    await api.post("/auth/logout"); // call backend logout
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
}

// Custom hook for easy access
export function useAuth() {
  return useContext(AuthContext);
}
