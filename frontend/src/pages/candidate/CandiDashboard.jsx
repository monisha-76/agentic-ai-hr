import { useEffect, useState } from "react";
import StatCard from "../../components/StatCard";
import JDCard from "../../components/JDCard";
import api from "../../api/api";

const CandidateDashboard = () => {
  const [jds, setJDs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({
    total_jobs: 0,
    myApplications: 0,
    totalApplications: 0
  });

  const [modalOpen, setModalOpen] = useState(false);
  const [selectedJD, setSelectedJD] = useState(null);
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    resume: null
  });
  const [submitting, setSubmitting] = useState(false);


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

  const fetchStats = async () => {
    try {
      const res = await api.get("/candidate/stats");
      setStats(res.data);
    } catch (err) {
      console.error("Failed to fetch candidate stats", err);
    }
  };

  useEffect(() => {
    fetchJDs();
    fetchStats();
  }, []);

  const handleApplyClick = (jd) => {
    setSelectedJD(jd);
    setModalOpen(true);
    setFormData({
      name: "",
      email: "",
      resume: null
    });
  };

  const handleFileChange = (e) => {
    setFormData({ ...formData, resume: e.target.files[0] });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.name || !formData.email || !formData.resume) {
      alert("Please fill all fields and upload your resume!");
      return;
    }

   setSubmitting(true); 

     const data = new FormData();

  // ✅ EXACT KEYS REQUIRED BY BACKEND
  data.append("file", formData.resume);         // ✅ MUST be "file"
  data.append("name", formData.name);
  data.append("email", formData.email);
  data.append("jd_id", selectedJD._id);  
    try {
      await api.post("/upload-resume", data, {
        headers: { "Content-Type": "multipart/form-data" }
      });
      alert("Application submitted successfully!");
      setModalOpen(false);
      fetchStats(); // refresh stats
    } catch (err) {
      console.error("Failed to submit application", err);
      alert("Failed to submit application");
    }finally{
      setSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b px-8 py-4">
        <h1 className="text-2xl font-semibold text-gray-800">
          Candidate Dashboard
        </h1>
      </header>

      <div className="p-8 max-w-7xl mx-auto">
        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
          <StatCard
            title="Total Job Openings"
            value={jds.length}
            color="bg-gray-500"
          />
          <StatCard
            title="My Applications"
            value={stats.myApplications}
            color="bg-gray-500 text-black"
          />
          <StatCard
            title="Total Applications"
            value={stats.totalApplications}
            color="bg-gray-500 text-black"
          />
        </div>

        {/* Search */}
        <div className="mb-6">
          <input
            type="text"
            placeholder="Search jobs..."
            className="w-full bg-white border border-gray-300 rounded-xl px-5 py-3 shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>

        {/* Job Listings */}
        <h2 className="text-xl font-semibold text-gray-800 mb-4">
          Job Listings
        </h2>

        <div className="space-y-4">
          {loading && <p className="text-gray-500">Loading jobs...</p>}
          {!loading && jds.length === 0 && (
            <p className="text-gray-500">No job openings available</p>
          )}
          {!loading &&
            jds.map((jd) => (
              <JDCard
                key={jd._id}
                jd={jd}
                isCandidate={true}
                onApply={() => handleApplyClick(jd)}
              />
            ))}
        </div>
      </div>

      {/* Apply Modal */}
      {modalOpen && (
        <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
          <div className="bg-white rounded-xl shadow-lg w-96 p-6 relative">
            <button
              className="absolute top-3 right-3 text-gray-400 hover:text-gray-600"
              onClick={() => setModalOpen(false)}
            >
              ✕
            </button>
            <h2 className="text-lg font-semibold mb-2">Apply for Job</h2>
            <p className="text-gray-600 mb-4">
              Applying for: <strong>{selectedJD.title}</strong>
            </p>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-gray-700 mb-1">Full Name</label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  className="w-full border border-gray-300 rounded-xl px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>
              <div>
                <label className="block text-gray-700 mb-1">Email</label>
                <input
                  type="email"
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  className="w-full border border-gray-300 rounded-xl px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>
              <div>
                <label className="block text-gray-700 mb-1">Resume Upload (PDF)</label>
                <input
                  type="file"
                  accept=".pdf"
                  onChange={handleFileChange}
                  className="w-full"
                />
              </div>
            <button
            type="submit"
            disabled={submitting}
            className={`w-full rounded-xl py-2 transition 
              ${submitting
                ? "bg-gray-400 cursor-not-allowed"
                : "bg-indigo-600 hover:bg-indigo-700 text-white"
              }`}
          >
            {submitting ? "Submitting..." : "Submit Application"}
          </button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default CandidateDashboard;