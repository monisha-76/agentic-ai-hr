import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { FiUser } from "react-icons/fi";

const CandidateHeader = ({ title }) => {
  const navigate = useNavigate();
  const [showMenu, setShowMenu] = useState(false);

  const userName = localStorage.getItem("userName");

  return (
    <header className="bg-gray-300 border-b px-8 py-4 flex justify-between items-center">

      {/* Page Title */}
      <h1 className="text-2xl font-semibold text-gray-800">
        {title}
      </h1>

      {/* Profile Dropdown */}
      <div className="relative">
        <button
          onClick={() => setShowMenu(!showMenu)}
          className="flex items-center gap-3 bg-gray-100 px-4 py-2 rounded-full hover:bg-gray-200 transition"
        >
          {/* User Icon */}
          <div className="w-9 h-9 rounded-full bg-indigo-600 text-white flex items-center justify-center">
            <FiUser size={18} />
          </div>

          {/* Name */}
          <span className="font-medium text-gray-700">
            {userName || "Candidate"}
          </span>

          {/* Arrow */}
          <span className="text-gray-500">⌄</span>
        </button>

        {showMenu && (
          <div className="absolute right-0 mt-3 w-52 bg-white border rounded-xl shadow-lg z-50 overflow-hidden">
            
             <button
              onClick={() => navigate("/candidate/Candidashboard")}
              className="block w-full text-left px-5 py-3 hover:bg-gray-100 transition"
            >
             Home
            </button>
            <button
              onClick={() => navigate("/candidate/profile")}
              className="block w-full text-left px-5 py-3 hover:bg-gray-100 transition"
            >
              Profile
            </button>

            <button
              onClick={() => navigate("/candidate/applications")}
              className="block w-full text-left px-5 py-3 hover:bg-gray-100 transition"
            >
              My Applications
            </button>

            <div className="border-t"></div>

            <button
              onClick={() => {
                localStorage.removeItem("token");
                localStorage.removeItem("userName");
                navigate("/");
              }}
              className="block w-full text-left px-5 py-3 text-red-600 hover:bg-red-50 transition"
            >
              Logout
            </button>

          </div>
        )}
      </div>

    </header>
  );
};

export default CandidateHeader;
