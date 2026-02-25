import { BrowserRouter, Routes, Route } from "react-router-dom"
import Login from "./pages/Login"
import AdminDashboard from "./pages/admin/AdminDashboard"
import CandiDashboard from "./pages/candidate/CandiDashboard"
import Signup from "./pages/Signup"
import MyApplication from "./pages/candidate/MyApplication";
import Profile from "./pages/candidate/Profile"
import MatchedCandidates from "./pages/admin/MatchedCandidates";
 

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/admin/admindashboard" element={<AdminDashboard />} />
        <Route path="/candidate/Candidashboard" element={<CandiDashboard />} />
        <Route path="/candidate/applications" element={<MyApplication />} />
        <Route path="/candidate/profile" element={<Profile/>}/>
        <Route path="/admin/matches/:jdId" element={<MatchedCandidates />} />

      </Routes>
    </BrowserRouter>
  )
}

export default App
