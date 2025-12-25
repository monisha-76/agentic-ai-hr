const JDCard = ({ jd, onDelete }) => {
  return (
    <div className="bg-white rounded-xl shadow-sm p-6 flex justify-between items-start">
      <div>
        <h2 className="text-xl font-semibold text-gray-800">
          {jd.title}
        </h2>

        <p className="mt-2 text-gray-600">
          <span className="font-semibold">Skills:</span>{" "}
          {jd.skills.join(", ")}
        </p>

        <p className="mt-1 text-gray-500">
          Matched Profiles:{" "}
          <span className="font-semibold">{jd.matches}</span>
        </p>
      </div>

      <div className="flex gap-3">
        <button className="px-4 py-2 border border-blue-600 text-blue-600 rounded-lg hover:bg-blue-50">
          View Matches
        </button>

        <button
          onClick={() => onDelete(jd)}
          className="px-4 py-2 border border-red-600 text-red-600 rounded-lg hover:bg-red-50"
        >
          Delete
        </button>
      </div>
    </div>
  );
};

export default JDCard;
