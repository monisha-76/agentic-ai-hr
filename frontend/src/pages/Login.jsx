import { useState } from "react";
import { loginUser } from "../api/auth";

const ADMIN_EMAIL = "admin@gmail.com";
const ADMIN_PASSWORD = "123456";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async (e) => {
  e.preventDefault();

  try {
    const res = await loginUser({ email, password });

    // Save token to localStorage
    localStorage.setItem("token", res.data.token);

    // Redirect based on role
    if (res.data.role === "admin") {
      window.location.href = "/admin/admindashboard";
    } else {
      window.location.href = "/candidate/Candidashboard";
    }
  } catch (err) {
    alert("Invalid credentials");
  }
};

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-r from-blue-500 to-purple-600">
      <div className="bg-white p-8 rounded-xl shadow-lg w-96">
        <h2 className="text-2xl font-bold text-center mb-6">Login</h2>

        <form onSubmit={handleLogin} className="space-y-4">
          <input
            placeholder="Email"
            onChange={(e) => setEmail(e.target.value)}
            className="w-full border p-2 rounded"
            required
          />
          <input
            type="password"
            placeholder="Password"
            onChange={(e) => setPassword(e.target.value)}
            className="w-full border p-2 rounded"
            required
          />

          <button className="w-full bg-purple-600 text-white py-2 rounded hover:bg-purple-700">
            Login
          </button>
        </form>

        <p className="text-sm text-center mt-4">
          New user?{" "}
          <a href="/signup" className="text-purple-600">Signup</a>
        </p>
      </div>
    </div>
  );
}
