import { BrowserRouter, Routes, Route } from "react-router-dom"
import Login from "./pages/Login"
import AdminDashboard from "./pages/admin/AdminDashboard"
import CandiDashboard from "./pages/candidate/CandiDashboard"
import Signup from "./pages/Signup"
function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/admin/admindashboard" element={<AdminDashboard />} />
        <Route path="/candidate/Candidashboard" element={<CandiDashboard />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
