import { useState } from "react";

const WriterStatus = () => {
  const [email, setEmail] = useState("");
  const [submissionId, setSubmissionId] = useState("");
  const [statusInfo, setStatusInfo] = useState(null);
  const [error, setError] = useState(null);

  const checkStatus = () => {
    if (!email || !submissionId) {
      setError("Please enter both email and submission ID.");
      return;
    }

    fetch(`http://localhost:8000/api/writer/status/${submissionId}/?email=${email}`)
      .then((res) => res.json())
      .then((data) => {
        if (data.error) {
          setError(data.error);
          setStatusInfo(null);
        } else {
          setStatusInfo(data);
          setError(null);
        }
      })
      .catch(() => {
        setError("Something went wrong.");
        setStatusInfo(null);
      });
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h2>📋 Check Submission Status</h2>

      <div style={{ marginBottom: "1rem" }}>
        <input
          type="email"
          placeholder="Writer Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          style={{ marginRight: "1rem", padding: "0.5rem" }}
        />
        <input
          type="number"
          placeholder="Submission ID"
          value={submissionId}
          onChange={(e) => setSubmissionId(e.target.value)}
          style={{ padding: "0.5rem" }}
        />
      </div>

      <button onClick={checkStatus}>Check Status</button>

      {error && <p style={{ color: "red", marginTop: "1rem" }}>{error}</p>}

      {statusInfo && (
        <div style={{ marginTop: "2rem" }}>
          <p><strong>Status:</strong> {statusInfo.status}</p>
          {statusInfo.judge_notes && (
            <>
              <h4>📝 Judge Notes:</h4>
              <ul>
                {statusInfo.judge_notes.map((note, i) => (
                  <li key={i}>{note}</li>
                ))}
              </ul>
            </>
          )}
        </div>
      )}
    </div>
  );
};

export default WriterStatus;
