import { useState, useEffect, useCallback } from "react";
import axios from "axios";
import {
  Link2,
  MousePointer2,
  Calendar,
  Copy,
  Check,
  ExternalLink,
} from "lucide-react";

export default function App() {
  const [longUrl, setLongUrl] = useState("");
  const [urls, setUrls] = useState([]);
  const [copiedId, setCopiedId] = useState(null);
  const [loading, setLoading] = useState(false);

  // Leave this as empty string for Vercel production
  const API_BASE = "";

  // Wrapped in useCallback so it can be used in useEffect safely
  const fetchUrls = useCallback(async () => {
    try {
      const res = await axios.get(`${API_BASE}/api/urls/`);
      setUrls(res.data);
    } catch (err) {
      console.error("Failed to fetch links:", err);
    }
  }, [API_BASE]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await axios.post(`${API_BASE}/api/shorten/`, { long_url: longUrl });
      setLongUrl("");
      // Refresh the list immediately after adding
      fetchUrls();
    } catch (err) {
      console.error("Error shortening URL:", err);
      alert("Failed to shorten URL. Check backend logs.");
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = (text, id) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  useEffect(() => {
    fetchUrls();
  }, [fetchUrls]);

  return (
    <div className="min-h-screen bg-slate-50 p-6">
      <div className="max-w-4xl mx-auto space-y-8">
        <header>
          <h1 className="text-3xl font-bold text-slate-900">Link Dashboard</h1>
          <p className="text-slate-500">Manage and track your shortened URLs</p>
        </header>

        {/* Create Form */}
        <section className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
          <form onSubmit={handleSubmit} className="flex gap-3">
            <div className="relative flex-1">
              <Link2 className="absolute left-3 top-3 text-slate-400 w-5 h-5" />
              <input
                type="url"
                className="w-full pl-10 pr-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                placeholder="Paste a long URL..."
                value={longUrl}
                onChange={(e) => setLongUrl(e.target.value)}
                required
              />
            </div>
            <button
              disabled={loading}
              className="bg-blue-600 text-white px-6 py-2 rounded-lg font-medium hover:bg-blue-700 transition disabled:bg-blue-400"
            >
              {loading ? "Working..." : "Shorten"}
            </button>
          </form>
        </section>

        {/* Analytics Table */}
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
          <table className="w-full text-left">
            <thead className="bg-slate-50 border-b border-slate-200">
              <tr>
                <th className="px-6 py-4 text-sm font-semibold text-slate-600">
                  Short Link
                </th>
                <th className="px-6 py-4 text-sm font-semibold text-slate-600">
                  Clicks
                </th>
                <th className="px-6 py-4 text-sm font-semibold text-slate-600">
                  Date
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {urls.length > 0 ? (
                urls.map((u, i) => (
                  <tr key={i} className="hover:bg-slate-50 transition">
                    <td className="px-6 py-4">
                      <div className="flex items-center gap-3">
                        <a
                          href={u.short_url}
                          target="_blank"
                          rel="noreferrer"
                          className="text-blue-600 font-medium hover:underline flex items-center gap-1"
                        >
                          {u.short_url} <ExternalLink className="w-3 h-3" />
                        </a>
                        <button
                          onClick={() => copyToClipboard(u.short_url, i)}
                          className="text-slate-400 hover:text-slate-600"
                        >
                          {copiedId === i ? (
                            <Check className="w-4 h-4 text-green-500" />
                          ) : (
                            <Copy className="w-4 h-4" />
                          )}
                        </button>
                      </div>
                      <p className="text-xs text-slate-400 truncate max-w-[250px]">
                        {u.long_url}
                      </p>
                    </td>
                    <td className="px-6 py-4 text-sm font-medium text-slate-700">
                      <div className="flex items-center gap-1">
                        <MousePointer2 className="w-4 h-4 text-blue-500" />{" "}
                        {u.clicks}
                      </div>
                    </td>
                    <td className="px-6 py-4 text-sm text-slate-500">
                      <div className="flex items-center gap-1">
                        <Calendar className="w-4 h-4" /> {u.created_at}
                      </div>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td
                    colSpan="3"
                    className="px-6 py-10 text-center text-slate-400"
                  >
                    No links found. Create your first one above!
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
