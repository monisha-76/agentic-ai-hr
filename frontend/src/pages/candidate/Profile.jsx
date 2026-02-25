import { useState } from "react";
import CandidateHeader from "./CandidateHeader";
import {
  FiEdit,
  FiLinkedin,
  FiGithub,
  FiUploadCloud,
} from "react-icons/fi";
import api from "../../api/api";
import { useEffect } from "react";


const Profile = () => {

  // 🔥 Edit mode state
  const [isEditing, setIsEditing] = useState(false);

  // 🔥 Profile form state
  const [formData, setFormData] = useState({
    full_name: "",
    gender: "",
    email: "",
    phone: "",
    degree: "",
    university: "",
    cgpa: "",
    year_of_passing: "",
    skills: "",
    company: "",
    role: "",
    description: "",
    linkedin: "",
    github: "",
  });

  useEffect(() => {
  fetchProfile();
}, []);

const fetchProfile = async () => {
  try {
    const res = await api.get("/candidate/profile");

    if (res.data && !res.data.message) {
      setFormData({
        full_name: res.data.full_name || "",
        gender: res.data.gender || "",
        email: res.data.email || "",
        phone: res.data.phone || "",
        degree: res.data.degree || "",
        university: res.data.university || "",
        cgpa: res.data.cgpa || "",
        year_of_passing: res.data.year_of_passing || "",
        skills: res.data.skills?.join(", ") || "",
        company: res.data.experience?.company || "",
        role: res.data.experience?.role || "",
        description: res.data.experience?.description || "",
        linkedin: res.data.linkedin || "",
        github: res.data.github || "",
      });
    }

  } catch (err) {
    console.log("No profile yet");
  }
};

const handleSave = async () => {
  try {
    await api.put("/candidate/profile", {
      full_name: formData.full_name,
      gender: formData.gender,
      phone: formData.phone,
      degree: formData.degree,
      university: formData.university,
      cgpa: formData.cgpa,
      year_of_passing: formData.year_of_passing,
      skills: formData.skills.split(",").map(s => s.trim()),
      experience: {
        company: formData.company,
        role: formData.role,
        description: formData.description,
      },
      linkedin: formData.linkedin,
      github: formData.github,
    });

    alert("Profile saved successfully!");
    setIsEditing(false);

  } catch (err) {
    alert("Failed to save profile");
  }
};

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <CandidateHeader title="Profile" />

      <div className="max-w-5xl mx-auto p-8 space-y-8">

        {/* ================= TOP PROFILE CARD ================= */}
        <div className="bg-white rounded-2xl shadow p-6 flex justify-between items-center">

          <div className="flex items-center gap-6">
            <div className="w-28 h-28 rounded-full bg-gray-200 flex items-center justify-center text-gray-500 text-sm">
              Photo
            </div>

            <div>
              <h2 className="text-2xl font-semibold text-gray-800">
                {formData.full_name || "Full Name"}
              </h2>
              <p className="text-gray-500 mt-2">
                {formData.email || "email@example.com"}
              </p>
            </div>
          </div>

          {/* ✏️ Edit Toggle */}
          <button
            onClick={() => setIsEditing(!isEditing)}
            className="p-3 bg-gray-100 rounded-lg hover:bg-gray-200 transition"
          >
            <FiEdit />
          </button>
        </div>

        {/* ================= PERSONAL INFORMATION ================= */}
        <div className="bg-white rounded-2xl shadow">
          <div className="border-b px-6 py-4">
            <h3 className="text-lg font-semibold text-gray-700">
              Personal Information
            </h3>
          </div>

          <div className="p-6 grid md:grid-cols-2 gap-6">
            <InputField
              label="Full Name"
              name="full_name"
              value={formData.full_name}
              onChange={handleChange}
              disabled={!isEditing}
            />

            <SelectField
              label="Gender"
              name="gender"
              value={formData.gender}
              onChange={handleChange}
              disabled={!isEditing}
              options={["Male", "Female", "Other"]}
            />

            <InputField
              label="Email Address"
              name="email"
              value={formData.email}
               onChange={handleChange}
             disabled={!isEditing}
            />

            <InputField
              label="Phone Number"
              name="phone"
              value={formData.phone}
              onChange={handleChange}
              disabled={!isEditing}
            />
          </div>
        </div>

        {/* ================= EDUCATION DETAILS ================= */}
        <div className="bg-white rounded-2xl shadow">
          <div className="border-b px-6 py-4">
            <h3 className="text-lg font-semibold text-gray-700">
              Education Details
            </h3>
          </div>

          <div className="p-6 space-y-6">
            <InputField
              label="Degree"
              name="degree"
              value={formData.degree}
              onChange={handleChange}
              disabled={!isEditing}
            />

            <InputField
              label="University / College"
              name="university"
              value={formData.university}
              onChange={handleChange}
              disabled={!isEditing}
            />

            <div className="grid md:grid-cols-2 gap-6">
              <InputField
                label="CGPA"
                name="cgpa"
                value={formData.cgpa}
                onChange={handleChange}
                disabled={!isEditing}
              />

              <InputField
                label="Year of Passing"
                name="year_of_passing"
                value={formData.year_of_passing}
                onChange={handleChange}
                disabled={!isEditing}
              />
            </div>
          </div>
        </div>

        {/* ================= SKILLS & EXPERIENCE ================= */}
        <div className="bg-white rounded-2xl shadow">
          <div className="border-b px-6 py-4">
            <h3 className="text-lg font-semibold text-gray-700">
              Skills & Experience
            </h3>
          </div>

          <div className="p-6 space-y-6">
            <InputField
              label="Skills (comma separated)"
              name="skills"
              value={formData.skills}
              onChange={handleChange}
              disabled={!isEditing}
            />

            <div className="grid md:grid-cols-2 gap-6">
              <InputField
                label="Company Name"
                name="company"
                value={formData.company}
                onChange={handleChange}
                disabled={!isEditing}
              />

              <InputField
                label="Role"
                name="role"
                value={formData.role}
                onChange={handleChange}
                disabled={!isEditing}
              />
            </div>

            <div>
              <label className="block text-sm text-gray-600 mb-2">
                Description
              </label>
              <textarea
                name="description"
                rows="3"
                value={formData.description}
                onChange={handleChange}
                disabled={!isEditing}
                className="w-full border rounded-xl px-4 py-3 focus:ring-2 focus:ring-blue-500 outline-none disabled:bg-gray-50"
              />
            </div>
          </div>
        </div>

        {/* ================= SOCIAL LINKS ================= */}
        <div className="bg-white rounded-2xl shadow">
          <div className="border-b px-6 py-4">
            <h3 className="text-lg font-semibold text-gray-700">
              Social Media Links
            </h3>
          </div>

          <div className="p-6 space-y-4">
            <InputWithIcon
              icon={<FiLinkedin />}
              name="linkedin"
              value={formData.linkedin}
              onChange={handleChange}
              disabled={!isEditing}
              placeholder="LinkedIn URL"
            />

            <InputWithIcon
              icon={<FiGithub />}
              name="github"
              value={formData.github}
              onChange={handleChange}
              disabled={!isEditing}
              placeholder="GitHub URL"
            />
          </div>
        </div>

        {/* ================= SAVE BUTTON ================= */}
     {isEditing && (
  <div className="text-center">
    <button
      onClick={handleSave}
      className="bg-blue-600 text-white px-14 py-3 rounded-xl hover:bg-blue-700 transition shadow"
    >
      Save Changes
    </button>
  </div>
)}


      </div>
    </div>
  );
};

/* ================= Reusable Components ================= */

const InputField = ({ label, disabled, ...props }) => (
  <div>
    <label className="block text-sm text-gray-600 mb-2">{label}</label>
    <input
      {...props}
      disabled={disabled}
      className="w-full border rounded-xl px-4 py-3 focus:ring-2 focus:ring-blue-500 outline-none disabled:bg-gray-50"
    />
  </div>
);

const SelectField = ({ label, options, disabled, ...props }) => (
  <div>
    <label className="block text-sm text-gray-600 mb-2">{label}</label>
    <select
      {...props}
      disabled={disabled}
      className="w-full border rounded-xl px-4 py-3 focus:ring-2 focus:ring-blue-500 outline-none disabled:bg-gray-50"
    >
      <option value="">Select</option>
      {options.map((opt, i) => (
        <option key={i}>{opt}</option>
      ))}
    </select>
  </div>
);

const InputWithIcon = ({ icon, disabled, ...props }) => (
  <div className="flex items-center gap-3 border rounded-xl px-4 py-3 disabled:bg-gray-50">
    {icon}
    <input
      {...props}
      disabled={disabled}
      className="w-full outline-none disabled:bg-gray-50"
    />
  </div>
);

export default Profile;
