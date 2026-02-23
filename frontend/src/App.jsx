import { useState, useEffect } from "react";
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
  const API_BASE = "";
  const fetchUrls = async () => {
    try {
      // This works for both local and production automatically
      const res = await axios.get(`${API_BASE}/api/urls/`);
      await axios.post(`${API_BASE}/api/shorten/`, { long_url: longUrl });
      setUrls(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post(`${API_BASE}/api/shorten/`, { long_url: longUrl });
      setLongUrl("");
      fetchUrls();
    } catch (err) {
      console.error("Error shortening URL:", err);
    }
  };

  const copyToClipboard = (text, id) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  useEffect(() => {
    // Define the function inside the effect to keep it "contained"
    const loadData = async () => {
      try {
        const res = await axios.get("http://localhost:8000/api/urls/");
        setUrls(res.data);
      } catch (err) {
        console.error("Failed to fetch links:", err);
      }
    };

    loadData();
  }, []);

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
            <button className="bg-blue-600 text-white px-6 py-2 rounded-lg font-medium hover:bg-blue-700 transition">
              Shorten
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
              {urls.map((u, i) => (
                <tr key={i} className="hover:bg-slate-50 transition">
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-3">
                      <a
                        href={u.short_url}
                        target="_blank"
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
                    <p className="text-xs text-slate-400 truncate max-w-[200px]">
                      {u.long_url}
                    </p>
                  </td>
                  <td className="px-6 py-4">
                    <span className="flex items-center gap-1 text-sm font-medium text-slate-700">
                      <MousePointer2 className="w-4 h-4 text-blue-500" />{" "}
                      {u.clicks}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-sm text-slate-500">
                    <div className="flex items-center gap-1">
                      <Calendar className="w-4 h-4" /> {u.created_at}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
