import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import api from "../api/axios";

export default function Register() {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    email: "",
    password: "",
    confirmPassword: "",
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  function handleChange(e) {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");

    if (formData.password !== formData.confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    setLoading(true);

    try {
      const res = await api.post("/auth/register", { email: formData.email, password: formData.password });

      if (res.status === 201) {
        // Registration successful, redirect to login page
        navigate("/login");
      }
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          "Registration failed. Please try again later."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary to-secondary px-4">
      <div className="bg-white rounded-lg shadow-lg p-8 max-w-md w-full">
        <h2 className="text-3xl font-bold mb-6 text-center text-gray-800">
          Register
        </h2>
        {error && (
          <div className="bg-red-100 text-red-700 p-3 mb-4 rounded">{error}</div>
        )}
        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label htmlFor="email" className="block text-gray-700 mb-2">
              Email Address
            </label>
            <input
              id="email"
              name="email"
              type="email"
              required
              value={formData.email}
              onChange={handleChange}
              className="w-full border border-gray-300 rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-primary"
              placeholder="you@example.com"
              autoComplete="email"
            />
          </div>
          <div>
            <label htmlFor="password" className="block text-gray-700 mb-2">
              Password
            </label>
            <input
              id="password"
              name="password"
              type="password"
              required
              minLength={6}
              value={formData.password}
              onChange={handleChange}
              className="w-full border border-gray-300 rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-primary"
              placeholder="Enter a strong password"
              autoComplete="new-password"
            />
          </div>
          <div>
            <label htmlFor="confirmPassword" className="block text-gray-700 mb-2">
              Confirm Password
            </label>
            <input
              id="confirmPassword"
              name="confirmPassword"
              type="password"
              required
              minLength={6}
              value={formData.confirmPassword}
              onChange={handleChange}
              className="w-full border border-gray-300 rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-primary"
              placeholder="Re-enter your password"
              autoComplete="new-password"
            />
          </div>
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-primary text-white py-3 rounded font-semibold hover:bg-indigo-700 transition"
          >
            {loading ? "Registering..." : "Register"}
          </button>
        </form>
        <p className="mt-5 text-center text-gray-600">
          Already have an account?{" "}
          <Link
            to="/login"
            className="text-secondary font-semibold hover:underline"
          >
            Login here
          </Link>
        </p>
      </div>
    </div>
  );
}
