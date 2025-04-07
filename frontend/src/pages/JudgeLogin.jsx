import { useState } from "react";
import { useNavigate } from "react-router-dom";

const JudgeLogin = () => {
  const [username, setUsername] = useState("");
  const navigate = useNavigate();

  const handleLogin = () => {
    if (username.trim()) {
      navigate(`/judge/${username}`);
    }
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h2>🎓 Judge Login</h2>
      <input
        type="text"
        placeholder="Enter judge username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        style={{ padding: "0.5rem", marginRight: "1rem" }}
      />
      <button onClick={handleLogin}>Login</button>
    </div>
  );
};

export default JudgeLogin;
