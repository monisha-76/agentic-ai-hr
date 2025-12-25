import { useEffect, useState } from "react";
import StatCard from "../../components/StatCard";
import JDCard from "../../components/JDCard";
import ConfirmModal from "../../components/ConfirmModal";
import api from "../../api/api";

const AdminDashboard = () => {
  const [jds, setJDs] = useState([]);
  const [stats, setStats] = useState({
    total_resumes: 0,
    total_jds: 0,
    matched_profiles: 0,
  });
  const [selectedJD, setSelectedJD] = useState(null);
  const [loading, setLoading] = useState(true);

  // ✅ Fetch Admin Stats
  const fetchStats = async () => {
    try {
      const res = await api.get("/admin/stats");
      setStats(res.data);
    } catch (err) {
      console.error("Failed to fetch admin stats", err);
    }
  };

  // ✅ Fetch JDs
  const fetchJDs = async () => {
    try {
      const res = await api.get("/jd/all");
      setJDs(res.data);
    } catch (err) {
      console.error("Failed to fetch JDs", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStats();
    fetchJDs();
  }, []);

  // ✅ Delete JD
  const handleDelete = async () => {
    try {
      await api.delete(`/jd/delete/${selectedJD._id}`);
      setJDs(jds.filter((jd) => jd._id !== selectedJD._id));
      setSelectedJD(null);

      // refresh stats after delete
      fetchStats();
    } catch (err) {
      console.error("Delete failed", err);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-gradient-to-r from-slate-800 to-slate-600 text-white px-8 py-4 flex justify-between items-center">
        <h1 className="text-2xl font-semibold">Admin Dashboard</h1>
        <button className="border px-4 py-2 rounded-lg hover:bg-white/10">
          Logout
        </button>
      </header>

      <div className="p-8">
        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <StatCard
            title="Total Resumes"
            value={stats.total_resumes}
            color="from-blue-500 to-blue-700"
          />
          <StatCard
            title="Total Job Descriptions"
            value={stats.total_jds}
            color="from-green-500 to-green-700"
          />
          <StatCard
            title="Matched Profiles"
            value={stats.matched_profiles}
            color="from-orange-500 to-orange-700"
          />
        </div>

        {/* JD Header */}
        <div className="flex justify-between items-center mt-10">
          <h2 className="text-xl font-semibold">Job Descriptions</h2>
          <button className="bg-blue-600 text-white px-4 py-2 rounded-lg">
            + Upload JD
          </button>
        </div>

        {/* JD List */}
        <div className="mt-6 space-y-4">
          {loading && <p>Loading JDs...</p>}

          {!loading && jds.length === 0 && (
            <p className="text-gray-500">No Job Descriptions found</p>
          )}

          {jds.map((jd) => (
            <JDCard
              key={jd._id}
              jd={{
                title: jd.title,
                skills: jd.skills,
                matches: jd.matched_profiles || 0,
              }}
              onDelete={() => setSelectedJD(jd)}
            />
          ))}
        </div>
      </div>

      {/* Confirm Delete */}
      <ConfirmModal
        open={!!selectedJD}
        title={selectedJD?.title}
        onClose={() => setSelectedJD(null)}
        onConfirm={handleDelete}
      />
    </div>
  );
};

export default AdminDashboard;    