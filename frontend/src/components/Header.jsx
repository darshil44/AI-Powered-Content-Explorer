import { NavLink, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Header() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  async function handleLogout() {
    await logout();
    navigate("/login");
  }

  return (
    <header className="bg-primary text-white shadow">
      <nav className="max-w-7xl mx-auto flex items-center justify-between px-6 py-4">
        <div className="text-2xl font-bold cursor-pointer select-none" onClick={() => navigate("/dashboard")}>
          AI Explorer
        </div>

        {user && (
          <ul className="flex space-x-6 items-center">
            <li>
              <NavLink
                to="/search"
                className={({ isActive }) =>
                  isActive ? "underline font-semibold" : "hover:underline"
                }
              >
                Search
              </NavLink>
            </li>
            <li>
              <NavLink
                to="/imagegen"
                className={({ isActive }) =>
                  isActive ? "underline font-semibold" : "hover:underline"
                }
              >
                ImageGen
              </NavLink>
            </li>
            <li>
              <NavLink
                to="/dashboard"
                className={({ isActive }) =>
                  isActive ? "underline font-semibold" : "hover:underline"
                }
              >
                Dashboard
              </NavLink>
            </li>
            <li>
              <button
                onClick={handleLogout}
                className="bg-red-600 hover:bg-red-700 px-3 py-1 rounded text-sm font-semibold transition"
              >
                Logout
              </button>
            </li>
          </ul>
        )}
      </nav>
    </header>
  );
}
