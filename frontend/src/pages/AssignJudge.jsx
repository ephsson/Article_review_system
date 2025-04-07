import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

const AssignJudge = () => {
  const { submission_id } = useParams();
  const [judges, setJudges] = useState([]);

  useEffect(() => {
        fetch("http://localhost:8000/api/editor/suggest-judges/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ submission_id: submission_id })
      })
      .then((res) => res.json())
      .then((data) => {
        setJudges(data.judges || []);
      })
      .catch(() => alert("Failed to fetch suggested judges"));
  }, [submission_id]);

  const handleAssign = (judgeUsername) => {
    fetch(`http://localhost:8000/api/editor/assign/${submission_id}/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ judge_username: judgeUsername }),
    })
      .then((res) => res.json())
      .then(() => {
        alert(`Assigned ${judgeUsername} to submission ${submission_id}`);
      })
      .catch(() => alert("Assignment failed"));
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h2>📄 Assign Judge to Submission #{submission_id}</h2>

      <h3 style={{ marginTop: "2rem" }}>Most Related Judges</h3>
      <div style={{ display: "flex", flexWrap: "wrap", gap: "1rem" }}>
        {judges.map((j) => (
          <div key={j.username} style={{
            border: "1px solid #ccc",
            borderRadius: "8px",
            padding: "1rem",
            width: "250px"
          }}>
            <strong>👤 {j.username}</strong><br />
            <p><strong>🧠 Interests:</strong> {j.interests}</p>
            <p><strong>📊 Score:</strong> {j.score.toFixed(2)}</p>
            <button onClick={() => handleAssign(j.username)}>Assign Judge</button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default AssignJudge;
