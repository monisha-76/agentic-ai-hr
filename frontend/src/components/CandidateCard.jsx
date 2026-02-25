import { useState } from "react";
import { Mail, User } from "lucide-react";

const CandidateCard = ({ candidate, onViewProfile, onSendEmail }) => {

  const [showMore, setShowMore] = useState(false);

  const visibleSkills = showMore
    ? candidate.extra_skills
    : candidate.extra_skills?.slice(0, 6);

  return (
    <div className="bg-white rounded-xl shadow-md p-5 border hover:shadow-lg transition relative">

      {/* Rank */}
      <div className="absolute top-3 left-3 bg-yellow-400 text-white text-xs px-2 py-1 rounded">
        #{candidate.rank}
      </div>

      {/* Header */}
      <div className="flex items-center gap-3 mb-3">
        <div className="w-12 h-12 rounded-full bg-gray-200 flex items-center justify-center">
          <User size={22} />
        </div>

        <div>
          <h2 className="font-semibold text-lg">{candidate.name}</h2>
          <p className="text-gray-500 text-sm">{candidate.email}</p>
        </div>

        <div className="ml-auto">
          <span className="bg-green-100 text-green-700 text-sm px-2 py-1 rounded">
            {candidate.score}% Match
          </span>
        </div>
      </div>

      {/* Matched Skills */}
      <div className="mb-3">
        <p className="text-sm font-medium text-gray-700">Matched Skills</p>
        <div className="flex flex-wrap gap-2 mt-1">
          {candidate.matched_skills?.map((skill, i) => (
            <span
              key={i}
              className="bg-blue-200 text-blue-700 text-xs px-2 py-1 rounded"
            >
              {skill}
            </span>
          ))}
        </div>
      </div>

      {/* Extra Skills */}
      <div className="mb-4">
        <p className="text-sm font-medium text-gray-700">Extra Skills</p>
        <div className="flex flex-wrap gap-2 mt-1">
          {visibleSkills?.map((skill, i) => (
            <span
              key={i}
              className="bg-blue-100 text-gray-800 text-xs px-2 py-1 rounded"
            >
              {skill}
            </span>
          ))}
        </div>

        {candidate.extra_skills?.length > 6 && (
          <button
            onClick={() => setShowMore(!showMore)}
            className="text-blue-900 text-sm mt-2"
          >
            {showMore ? "View Less" : "View More"}
          </button>
        )}
      </div>

      {/* Buttons */}
      <div className="flex gap-3">
        <button
          onClick={() => onViewProfile(candidate.resume_id)}
          className="flex-1 border border-gray-300 rounded-lg py-2 text-sm hover:bg-gray-100"
        >
          View Profile
        </button>

        <button
          onClick={() => onSendEmail(candidate.email)}
          className="flex-1 bg-blue-600 text-white rounded-lg py-2 text-sm hover:bg-blue-700 flex items-center justify-center gap-2"
        >
          <Mail size={16} />
          Send Email
        </button>
      </div>
    </div>
  );
};

export default CandidateCard;