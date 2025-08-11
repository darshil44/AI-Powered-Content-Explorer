import axios from "axios";

// Create an Axios instance with default config
const api = axios.create({
  baseURL: "http://localhost:8000/api/v1", // backend FastAPI URL - change if different
  withCredentials: true, // allow sending/receiving HTTP-only cookies
  headers: {
    "Content-Type": "application/json",
  },
});

// You can add interceptors here if needed (e.g., refresh token, error handling)

export default api;
