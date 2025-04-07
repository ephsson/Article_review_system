import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const EditorPanel = () => {
  const [submissions, setSubmissions] = useState([]);
  const [judges, setJudges] = useState([]);
  const [showAdd, setShowAdd] = useState(false);
  const [newJudge, setNewJudge] = useState({ username: "", interests_csv: "" });
  const [expandedId, setExpandedId] = useState(null);
  const [reviewNotes, setReviewNotes] = useState({});

  const navigate = useNavigate();

  useEffect(() => {
    fetch("http://localhost:8000/api/editor/submissions/")
      .then((res) => res.json())
      .then((data) => setSubmissions(data.submissions || []))
      .catch((err) => console.error("Submissions fetch failed", err));

    fetch("http://localhost:8000/api/editor/judges/list/")
      .then((res) => res.json())
      .then((data) => setJudges(data.judges || []))
      .catch((err) => console.error("Judges fetch failed", err));
  }, []);

  const handleAddJudge = () => {
    fetch("http://localhost:8000/api/editor/judges/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(newJudge),
    })
      .then((res) => res.json())
      .then((data) => {
        alert("Judge added!");
        setJudges([...judges, data]);
        setNewJudge({ username: "", interests_csv: "" });
        setShowAdd(false);
      })
      .catch(() => alert("Failed to add judge."));
  };

  const updateStatus = (submissionId, newStatus) => {
    fetch(`http://localhost:8000/api/editor/update-status/${submissionId}/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ new_status: newStatus }),
    })
      .then((res) => res.json())
      .then((data) => {
        alert(data.message);
        window.location.reload();
      })
      .catch(() => alert("Status update failed."));
  };

  const toggleExpand = (submissionId) => {
    if (expandedId === submissionId) {
      setExpandedId(null);
      return;
    }

    fetch(`http://localhost:8000/api/editor/reviews/${submissionId}/`)
      .then((res) => res.json())
      .then((data) => {
        setReviewNotes((prev) => ({ ...prev, [submissionId]: data.judge_notes || [] }));
        setExpandedId(submissionId);
      })
      .catch(() => {
        setReviewNotes((prev) => ({ ...prev, [submissionId]: ["Failed to load notes"] }));
        setExpandedId(submissionId);
      });
  };

  const grouped = submissions.reduce((acc, sub) => {
    const status = sub.status;
    if (!acc[status]) acc[status] = [];
    acc[status].push(sub);
    return acc;
  }, {});

  return (
    <div style={{ display: "flex", padding: "1rem" }}>
      <div style={{ flex: 3, paddingRight: "1rem", borderRight: "1px solid #ccc" }}>
        <h2>📄 All Submissions</h2>

        {Object.entries(grouped).map(([status, group]) => (
          <div key={status} style={{ marginBottom: "2rem" }}>
            <h3>{status.replace("_", " ").toUpperCase()}</h3>
            {group.map((s) => (
              <div
                key={s.submission_id}
                style={{
                  border: "1px solid #ddd",
                  borderRadius: "8px",
                  padding: "1rem",
                  marginBottom: "1rem",
                  cursor: "pointer",
                  backgroundColor: expandedId === s.submission_id ? "#f9f9f9" : "white"
                }}
                onClick={() => toggleExpand(s.submission_id)}
              >
                <strong>Submission #{s.submission_id}</strong><br />
                Authors: {s.authors || "N/A"}<br />
                Organizations: {s.organizations || "N/A"}<br />

                <div style={{ marginTop: "0.5rem" }}>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      navigate(`/assign/${s.submission_id}`);
                    }}
                    style={{ marginRight: "0.5rem" }}
                  >
                    Assign Judge
                  </button>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      updateStatus(s.submission_id, "published");
                    }}
                    style={{ marginRight: "0.5rem" }}
                  >
                    ✅ Publish
                  </button>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      updateStatus(s.submission_id, "revisions_required");
                    }}
                  >
                    🛠️ Request Revisions
                  </button>
                </div>

                {expandedId === s.submission_id && (
                  <div style={{ marginTop: "1rem", paddingTop: "0.5rem", borderTop: "1px solid #ccc" }}>
                    <strong>📋 Judge Notes:</strong>
                    {reviewNotes[s.submission_id]?.length > 0 ? (
                      <ul>
                        {reviewNotes[s.submission_id].map((note, i) => (
                          <li key={i}>{note}</li>
                        ))}
                      </ul>
                    ) : (
                      <p><em>No notes yet.</em></p>
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>
        ))}
      </div>

      <div style={{ flex: 2, paddingLeft: "1rem" }}>
        <h2>👩‍⚖️ Judges</h2>
        <ul>
          {judges.map((j) => (
            <li key={j.username}>
              <strong>{j.username}</strong><br />
              Interests: {j.interests}
            </li>
          ))}
        </ul>

        <button onClick={() => setShowAdd(!showAdd)} style={{ marginTop: "1rem" }}>
          {showAdd ? "Cancel" : "➕ Add Judge"}
        </button>

        {showAdd && (
          <div style={{ marginTop: "1rem" }}>
            <input
              placeholder="Username"
              value={newJudge.username}
              onChange={(e) => setNewJudge({ ...newJudge, username: e.target.value })}
              style={{ display: "block", marginBottom: "0.5rem", width: "100%" }}
            />
            <input
              placeholder="Interests (CSV)"
              value={newJudge.interests_csv}
              onChange={(e) => setNewJudge({ ...newJudge, interests_csv: e.target.value })}
              style={{ display: "block", marginBottom: "0.5rem", width: "100%" }}
            />
            <button onClick={handleAddJudge}>Submit Judge</button>
          </div>
        )}
      </div>
    </div>
  );
};

export default EditorPanel;
