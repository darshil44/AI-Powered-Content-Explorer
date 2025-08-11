import { useState } from "react";
import api from "../api/axios";
import { toast } from "react-toastify";

export default function ImageGen() {
  const [prompt, setPrompt] = useState("");
  const [images, setImages] = useState([]); // array of image URLs/base64 strings
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleGenerate(e) {
    e.preventDefault();
    setError("");
    if (!prompt.trim()) return;

    setLoading(true);
    setImages([]);

    try {
      const res = await api.post("/image", { prompt });
      setImages(res.data.images || []); // adapt based on your backend response
    } catch (err) {
      setError(
        err.response?.data?.detail || "Failed to generate images. Try again."
      );
    } finally {
      setLoading(false);
    }
  }

  // Save generated image to backend dashboard
  const saveImage = async (imgSrc) => {
    try {
      const payload = {
        type: "image",
        content: prompt,
        image_url: imgSrc,
      };

      await api.post("/dashboard", payload);
      toast.success("Image saved successfully!");
    } catch (error) {
      alert(
        error.response?.data?.detail ||
          "Failed to save image. Please try again later."
      );
    }
  };

  return (
    <div className="max-w-5xl mx-auto p-6">
      <h1 className="text-4xl font-bold mb-6 text-center text-primary">
        AI Content Explorer - Image Generator
      </h1>

      <form onSubmit={handleGenerate} className="flex max-w-md mx-auto mb-8">
        <input
          type="text"
          placeholder="Enter image description..."
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          className="flex-grow px-4 py-3 rounded-l-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary"
        />
        <button
          type="submit"
          disabled={loading}
          className="bg-primary text-white px-6 rounded-r-lg font-semibold hover:bg-indigo-700 transition"
        >
          {loading ? "Generating..." : "Generate"}
        </button>
      </form>

      {error && (
        <p className="max-w-md mx-auto mb-6 text-red-600 text-center">{error}</p>
      )}

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6 max-w-4xl mx-auto">
        {images.length === 0 && !loading && (
          <p className="text-center text-gray-500">No images generated yet.</p>
        )}

        {images.map((imgSrc, idx) => (
          <div
            key={idx}
            className="rounded-lg overflow-hidden shadow hover:shadow-lg transition flex flex-col"
          >
            <img
              src={imgSrc}
              alt={`Generated for: ${prompt}`}
              className="w-full h-auto object-cover"
            />
            <button
              className="mt-2 bg-green-600 text-white px-3 py-1 rounded hover:bg-green-700 transition self-center"
              onClick={() => saveImage(imgSrc)}
            >
              Save
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
