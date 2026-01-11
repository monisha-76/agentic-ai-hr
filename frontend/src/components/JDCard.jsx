const JDCard = ({ jd, isCandidate = false, onApply, onDelete }) => {
  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 flex justify-between items-start">
      {/* Left content */}
      <div className="max-w-3xl">
        <h2 className="text-xl font-semibold text-gray-900">
          {jd.title}
        </h2>

        <p className="mt-2 text-gray-600 text-sm leading-relaxed">
          {jd.description}
        </p>

        <p className="mt-3 text-sm text-gray-500">
          <span className="font-semibold text-gray-700">
            Total Candidates:
          </span>{" "}
          <span className="text-emerald-600 font-bold">
            {jd.total_candidates ?? 0}
          </span>
        </p>
      </div>

      {/* Right actions */}
      <div className="flex gap-3">
        {isCandidate ? (
          <button
            onClick={() => onApply(jd)}
            className="px-5 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition"
          >
            Apply Now
          </button>
        ) : (
          <>
            <button className="px-4 py-2 border border-blue-600 text-blue-600 rounded-lg hover:bg-blue-50">
              View Matches
            </button>

            <button
              onClick={() => onDelete(jd)}
              className="px-4 py-2 border border-red-600 text-red-600 rounded-lg hover:bg-red-50"
            >
              Delete
            </button>
          </>
        )}
      </div>
    </div>
  );
};

export default JDCard;