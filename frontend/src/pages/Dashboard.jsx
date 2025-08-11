import { useEffect, useState } from "react";
import api from "../api/axios";
import { toast } from "react-toastify";

export default function Dashboard() {
  const [entries, setEntries] = useState([]);
  const [filterType, setFilterType] = useState("all"); // all, search, image
  const [keyword, setKeyword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // Fetch saved entries from backend dashboard
  async function fetchEntries() {
    setLoading(true);
    setError("");
    try {
      const res = await api.get("/dashboard");
      setEntries(res.data.entries || []);
    } catch (err) {
      setError(
        err.response?.data?.detail || "Failed to load saved entries."
      );
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    fetchEntries();
  }, []);

  // Filter entries based on filterType and keyword
  const filteredEntries = entries.filter((entry) => {
    if (filterType !== "all" && entry.type !== filterType) {
      return false;
    }
    if (
      keyword.trim() &&
      !(
        entry.content?.toLowerCase().includes(keyword.toLowerCase()) ||
        entry.type.toLowerCase().includes(keyword.toLowerCase())
      )
    ) {
      return false;
    }
    return true;
  });

  // Delete entry by id
  async function handleDelete(id) {
    if (!window.confirm("Are you sure you want to delete this entry?")) return;

    try {
      await api.delete(`/dashboard/${id}`);
      setEntries((prev) => prev.filter((e) => e.id !== id));
    } catch (err) {
      alert(
        err.response?.data?.detail || "Failed to delete. Try again later."
      );
    }
  }

  // Basic edit handler (inline editing content)
  async function handleEdit(id, newContent) {
    try {
      await api.put(`/dashboard/${id}`, { content: newContent });
      setEntries((prev) =>
        prev.map((e) => (e.id === id ? { ...e, content: newContent } : e))
      );
    } catch (err) {
      alert(
        err.response?.data?.detail || "Failed to update. Try again later."
      );
    }
  }

  return (
    <div className="max-w-6xl mx-auto p-6">
      <h1 className="text-4xl font-bold mb-6 text-center text-primary">Your Saved Items</h1>

      <div className="flex flex-col sm:flex-row sm:justify-between mb-6 gap-4 max-w-3xl mx-auto">
        <select
          className="border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary"
          value={filterType}
          onChange={(e) => setFilterType(e.target.value)}
        >
          <option value="all">All Types</option>
          <option value="search">Search Results</option>
          <option value="image">Images</option>
        </select>

        <input
          type="text"
          placeholder="Search by keyword"
          className="border border-gray-300 rounded px-3 py-2 flex-grow focus:outline-none focus:ring-2 focus:ring-primary"
          value={keyword}
          onChange={(e) => setKeyword(e.target.value)}
        />
      </div>

      {loading ? (
        <p className="text-center">Loading saved items...</p>
      ) : error ? (
        <p className="text-center text-red-600">{error}</p>
      ) : filteredEntries.length === 0 ? (
        <p className="text-center text-gray-500">No saved items found.</p>
      ) : (
        <ul className="space-y-6 max-w-4xl mx-auto">
          {filteredEntries.map((entry) => (
            <EntryItem
              key={entry.id}
              entry={entry}
              onDelete={handleDelete}
              onEdit={handleEdit}
            />
          ))}
        </ul>
      )}
    </div>
  );
}

// Component to display individual entry with edit/delete
function EntryItem({ entry, onDelete, onEdit }) {
  const { id, type, content, url, image_url, created_at } = entry;
  const [isEditing, setIsEditing] = useState(false);
  const [editContent, setEditContent] = useState(content);

  function handleSave() {
    if (editContent.trim() === "") {
      toast.error("Content cannot be empty.");
      return;
    }
    onEdit(id, editContent);
    setIsEditing(false);
  }

  return (
    <li className="bg-white p-4 rounded-lg shadow hover:shadow-lg transition">
      <div className="flex flex-col sm:flex-row sm:justify-between items-start sm:items-center gap-3">
        <div className="flex-grow">
          <p className="text-sm text-gray-500 mb-1">
            Type: <span className="capitalize">{type}</span> |{" "}
            <time dateTime={created_at}>
              {new Date(created_at).toLocaleString()}
            </time>
          </p>

          {type === "image" && image_url ? (
            <img
              src={image_url}
              alt={content}
              className="max-w-xs rounded mb-2"
            />
          ) : null}

          {isEditing ? (
            <textarea
              className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary"
              rows={3}
              value={editContent}
              onChange={(e) => setEditContent(e.target.value)}
            />
          ) : (
            <p className="whitespace-pre-wrap">{content}</p>
          )}

          {url && (
            <a
              href={url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-primary hover:underline break-words"
            >
              {url}
            </a>
          )}
        </div>

        <div className="flex gap-3 mt-3 sm:mt-0">
          {isEditing ? (
            <>
              <button
                onClick={handleSave}
                className="bg-primary text-white px-3 py-1 rounded hover:bg-indigo-700 transition"
              >
                Save
              </button>
              <button
                onClick={() => {
                  setIsEditing(false);
                  setEditContent(content);
                }}
                className="bg-gray-300 text-gray-700 px-3 py-1 rounded hover:bg-gray-400 transition"
              >
                Cancel
              </button>
            </>
          ) : (
            <>
              <button
                onClick={() => setIsEditing(true)}
                className="bg-yellow-400 text-white px-3 py-1 rounded hover:bg-yellow-500 transition"
              >
                Edit
              </button>
              <button
                onClick={() => onDelete(id)}
                className="bg-red-600 text-white px-3 py-1 rounded hover:bg-red-700 transition"
              >
                Delete
              </button>
            </>
          )}
        </div>
      </div>
    </li>
  );
}
