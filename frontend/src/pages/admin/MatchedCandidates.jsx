import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import CandidateCard from "../../components/CandidateCard";
import api from "../../api/api";
import toast from "react-hot-toast";

const MatchedCandidates = () => {
  const { jdId } = useParams();
  const navigate = useNavigate();

  const [candidates, setCandidates] = useState([]);
  const [jobTitle, setJobTitle] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchMatches();
  }, []);

  const fetchMatches = async () => {
    try {
      const matchRes = await api.get(`/admin/jd/${jdId}/matches`);
      const matchData = Array.isArray(matchRes.data) ? matchRes.data : [];
      setCandidates(matchData);

      const jobRes = await api.get(`/admin/jd/${jdId}`);
      setJobTitle(jobRes.data?.title || "");

    } catch (error) {
      console.error(error);
      toast.error("Failed to load matches");
    } finally {
      setLoading(false);
    }
  };

  const handleViewProfile = (candidateId) => {
    navigate(`/admin/candidate/${candidateId}`);
  };

  // ✅ EMAIL SEND WITH TOAST
  const handleSendEmail = async (candidate) => {
    try {
      await api.post("/admin/send-email", {
        email: candidate.email,
        name: candidate.name,
        job_title: jobTitle,
      });

      toast.success(`Email sent to ${candidate.name}`);

    } catch (error) {
      console.error(error);
      toast.error("Email failed to send");
    }
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