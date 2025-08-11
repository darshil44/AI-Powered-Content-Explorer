import { useState } from "react";
import api from "../api/axios";
import { toast } from "react-toastify";

export default function Search() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSearch(e) {
    e.preventDefault();
    setError("");
    if (!query.trim()) return;

    setLoading(true);
    setResults([]);

    try {
      const res = await api.post("/search", { query });
      setResults(res.data.results || []); // adapt based on your backend response shape
    } catch (err) {
      setError(
        err.response?.data?.detail || "Failed to fetch search results. Try again."
      );
    } finally {
      setLoading(false);
    }
  }

  // Added function to save a search result to backend
  const saveResult = async (item) => {
    try {
      const payload = {
        type: "search",
        content: item.summary || item.title || item.url || "No content",
        url: item.url,
      };

      await api.post("/dashboard", payload);
      toast.success("Saved successfully!");
    } catch (error) {
      alert(
        error.response?.data?.detail ||
          "Failed to save. Please try again later."
      );
    }
  };

  return (
    <div className="max-w-5xl mx-auto p-6">
      <h1 className="text-4xl font-bold mb-6 text-center text-primary">
        AI Content Explorer - Search
      </h1>

      <form onSubmit={handleSearch} className="flex max-w-md mx-auto mb-8">
        <input
          type="text"
          placeholder="Search topics, questions..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="flex-grow px-4 py-3 rounded-l-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary"
        />
        <button
          type="submit"
          disabled={loading}
          className="bg-primary text-white px-6 rounded-r-lg font-semibold hover:bg-indigo-700 transition"
        >
          {loading ? "Searching..." : "Search"}
        </button>
      </form>

      {error && (
        <p className="max-w-md mx-auto mb-6 text-red-600 text-center">{error}</p>
      )}

      <ul className="space-y-6 max-w-3xl mx-auto">
        {results.length === 0 && !loading && (
          <p className="text-center text-gray-500">No results yet. Try searching!</p>
        )}

        {results.map((item, idx) => (
          <li
            key={idx}
            className="bg-white p-4 rounded-lg shadow hover:shadow-lg transition flex flex-col"
          >
            <a
              href={item.url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-lg font-semibold text-primary hover:underline break-words"
            >
              {item.title || item.url}
            </a>
            <p className="mt-1 text-gray-700 whitespace-pre-wrap">
              {item.summary || item.description || "No description available."}
            </p>
            <p className="mt-2 text-sm text-gray-400">{item.domain || item.source}</p>

            <button
              className="mt-4 self-start bg-green-600 text-white px-3 py-1 rounded hover:bg-green-700 transition"
              onClick={() => saveResult(item)}
            >
              Save
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
