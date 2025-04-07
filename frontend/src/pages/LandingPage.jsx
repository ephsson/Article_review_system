import { useEffect, useState } from "react";

function LandingPage() {
  const [submissions, setSubmissions] = useState([]);

  useEffect(() => {
    fetch("http://localhost:8000/api/public/published/")
      .then(res => res.json())
      .then(data => setSubmissions(data.published_submissions))
      .catch(err => console.error("Failed to fetch published submissions", err));
  }, []);

  return (
    <div style={{ padding: "2rem" }}>
      <h1>📚 Published Papers</h1>
      {submissions.length === 0 ? (
        <p>No published papers yet.</p>
      ) : (
        <ul>
          {submissions.map((sub) => (
            <li key={sub.submission_id} style={{ marginBottom: "1rem" }}>
              <strong>{sub.title}</strong> <br />
              <a href={sub.pdf_url} target="_blank" rel="noopener noreferrer">
                📄 Download PDF
              </a>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default LandingPage;
