import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import CandidateCard from "../../components/CandidateCard";
import api from "../../api/api";

const MatchedCandidates = () => {
  const { jdId } = useParams();
  const navigate = useNavigate();

  const [candidates, setCandidates] = useState([]);
  const [jobTitle, setJobTitle] = useState("");   // ✅ NEW
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchMatches();
  }, []);

const fetchMatches = async () => {
  try {
    // Matches
    const matchRes = await api.get(`/admin/jd/${jdId}/matches`);
    const matchData = Array.isArray(matchRes.data) ? matchRes.data : [];
    setCandidates(matchData);

    // Job details
    const jobRes = await api.get(`/admin/jd/${jdId}`);
    setJobTitle(jobRes.data?.title || "");

  } catch (error) {
    console.error(error);
  } finally {
    setLoading(false);
  }
};
  const handleViewProfile = (resumeId) => {
    navigate(`/admin/candidate/${resumeId}`);
  };

  const handleSendEmail = (email) => {
    alert(`Send email to: ${email}`);
  };

  // Stats
  const totalMatches = candidates.length;
  const topScore = candidates.length > 0 ? candidates[0]?.score || 0 : 0;

  const avgScore =
    candidates.length > 0
      ? (
          candidates.reduce((sum, c) => sum + (c.score || 0), 0) /
          candidates.length
        ).toFixed(1)
      : 0;

  return (
    <div className="min-h-screen bg-gray-100 p-6">

      {/* Header */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold">Matched Candidates</h1>

        <p className="text-gray-600 mt-1">
          Job Title:{" "}
          <span className="font-semibold">
            {jobTitle || "Loading..."}
          </span>
        </p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">

        <div className="bg-white rounded-lg p-4 shadow">
          <p className="text-gray-800 text-md">Total Matches</p>
          <h2 className="text-xl font-bold">{totalMatches}</h2>
        </div>

        <div className="bg-white rounded-lg p-4 shadow">
          <p className="text-gray-800 text-md">Top Score</p>
          <h2 className="text-xl font-bold">{topScore}%</h2>
        </div>

        <div className="bg-white rounded-lg p-4 shadow">
          <p className="text-gray-800 text-md">Average Score</p>
          <h2 className="text-xl font-bold">{avgScore}%</h2>
        </div>

        <div className="bg-white rounded-lg p-4 shadow">
          <p className="text-gray-800 text-md">Ranked</p>
          <h2 className="text-xl font-bold">{totalMatches}</h2>
        </div>

      </div>

      {/* Candidate Grid */}
      {loading ? (
        <p>Loading candidates...</p>
      ) : candidates.length === 0 ? (
        <p>No matched candidates found.</p>
      ) : (
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {candidates.map((candidate, index) => (
            <CandidateCard
              key={index}
              candidate={candidate}
              onViewProfile={handleViewProfile}
              onSendEmail={handleSendEmail}
            />
          ))}
        </div>
      )}

    </div>
  );
};

export default MatchedCandidates;