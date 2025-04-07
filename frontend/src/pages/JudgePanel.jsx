import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";

const JudgePanel = () => {
  const { username } = useParams();
  const [assigned, setAssigned] = useState([]);
  const [notes, setNotes] = useState({});  // { submission_id: note }

  useEffect(() => {
    if (!username) return;

    fetch("http://localhost:8000/api/judge/panel/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username }),
    })
      .then((res) => res.json())
      .then((data) => setAssigned(data.submissions || []))
      .catch((err) => console.error("Error fetching submissions", err));
  }, [username]);

  const handleNoteChange = (id, value) => {
    setNotes((prev) => ({ ...prev, [id]: value }));
  };

  const handleNoteSubmit = (submission_id) => {
    const note = notes[submission_id];
    if (!note) return;

    fetch(`http://localhost:8000/api/judge/note/${submission_id}/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, note }),
    })
      .then((res) => res.json())
      .then((data) => {
        alert("Note submitted!");
        setNotes((prev) => ({ ...prev, [submission_id]: "" }));
      })
      .catch(() => alert("Failed to submit note"));
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h2>🔍 Judge Panel: {username}</h2>
      <h3>📄 Assigned Submissions</h3>

      {assigned.length === 0 ? (
        <p>No submissions assigned to you yet.</p>
      ) : (
        <ul>
          {assigned.map((s) => (
            <li key={s.submission_id} style={{ marginBottom: "2rem" }}>
              <strong>Submission #{s.submission_id}</strong><br />
              Status: {s.status} <br />
              <a href={s.anonymized_pdf} target="_blank" rel="noreferrer">
                📄 View PDF
              </a>

              <div style={{ marginTop: "1rem" }}>
                <textarea
                  placeholder="Write your note..."
                  value={notes[s.submission_id] || ""}
                  onChange={(e) => handleNoteChange(s.submission_id, e.target.value)}
                  style={{ width: "100%", height: "60px" }}
                />
                <button
                  onClick={() => handleNoteSubmit(s.submission_id)}
                  style={{ marginTop: "0.5rem" }}
                >
                  Submit Note
                </button>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default JudgePanel;
