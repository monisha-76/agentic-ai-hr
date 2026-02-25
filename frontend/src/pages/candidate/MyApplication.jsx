import { useEffect, useState } from "react";
import { FiSearch, FiCalendar } from "react-icons/fi";
import api from "../../api/api";
import CandidateHeader from "./CandidateHeader";


const MyApplication = () => {
  const [applications, setApplications] = useState([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);

  const fetchApplications = async () => {
    try {
      const res = await api.get("/candidate/applications");
      setApplications(res.data);
    } catch (err) {
      console.error("Failed to load applications", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchApplications();
  }, []);

  const filtered = applications.filter(app =>
    app.title.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-gray-50">

      {/* Header */}
<CandidateHeader title="My Applications" />


      <div className="max-w-5xl mx-auto px-8 py-8">

        {/* Search Bar */}
        <div className="relative mb-8">
          <FiSearch className="absolute left-4 top-3.5 text-gray-500" />
          <input
            type="text"
            placeholder="Search applied jobs..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full bg-white border border-gray-300 rounded-xl pl-12 pr-4 py-3 shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 transition"
          />
        </div>

        {/* Loading */}
        {loading && (
          <p className="text-gray-500">Loading applications...</p>
        )}

        {/* Empty State */}
        {!loading && filtered.length === 0 && (
          <div className="bg-white rounded-xl shadow-sm p-8 text-center text-gray-500">
            No applications found.
          </div>
        )}

        {/* Application Cards */}
        <div className="space-y-6">
          {!loading &&
            filtered.map(app => (
              <div
                key={app.resume_id}
                className="bg-white rounded-2xl shadow-md border border-gray-400 p-6 hover:shadow-lg transition"
              >
                {/* Top Row */}
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <h2 className="font-semibold text-lg text-gray-800">
                      {app.title}
                    </h2>

                    <div className="flex items-center text-sm text-gray-500 mt-2">
                      <FiCalendar className="mr-2" />
                      Applied on{" "}
                      {app.applied_at
                        ? new Date(app.applied_at).toLocaleDateString()
                        : "N/A"}
                    </div>
                  </div>

                  {/* Status Badge */}
                  <span className="bg-green-100 text-green-600 text-xs px-3 py-1 rounded-full font-medium">
                    Submitted
                  </span>
                </div>

                {/* Skills */}
                <div className="flex flex-wrap gap-2 mt-4">
                  {app.skills.slice(0, 6).map((skill, i) => (
                    <span
                      key={i}
                      className="bg-indigo-50 text-indigo-600 px-3 py-1 rounded-full text-xs font-medium"
                    >
                      {skill}
                    </span>
                  ))}
                </div>
              </div>
            ))}
        </div>
      </div>
    </div>
  );
};

export default MyApplication;
