import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import LandingPage from "./pages/LandingPage";
import WriterUpload from "./pages/WriterUpload";
import WriterStatus from "./pages/WriterStatus";
import EditorPanel from "./pages/EditorPanel";
import JudgePanel from "./pages/JudgePanel";
import JudgeLogin from "./pages/JudgeLogin";
import AssignJudge from "./pages/AssignJudge";


function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/upload" element={<WriterUpload />} />
        <Route path="/status" element={<WriterStatus />} />
        <Route path="/editor" element={<EditorPanel />} />
        <Route path="/judge" element={<JudgeLogin />} />
        <Route path="/judge/:username" element={<JudgePanel />} />
        <Route path="/assign/:submission_id" element={<AssignJudge />} />
      </Routes>
    </Router>
  );
}

export default App;
