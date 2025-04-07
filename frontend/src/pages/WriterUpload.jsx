import { useState } from "react";

const WriterUpload = () => {
  const [email, setEmail] = useState("");
  const [file, setFile] = useState(null);
  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);

  const handleUpload = () => {
    if (!email || !file) {
      setError("Please provide an email and select a PDF file.");
      return;
    }

    const formData = new FormData();
    formData.append("writer_email", email);
    formData.append("pdf_file", file);

    fetch("http://localhost:8000/api/writer/upload/", {
      method: "POST",
      body: formData,
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.error) {
          setError(data.error);
          setResponse(null);
        } else {
          setResponse(data);
          setError(null);
        }
      })
      .catch(() => setError("Upload failed. Please try again."));
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h2>📤 Submit Your Paper</h2>

      <div style={{ marginBottom: "1rem" }}>
        <input
          type="email"
          placeholder="Your Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          style={{ padding: "0.5rem", marginRight: "1rem" }}
        />
        <input
          type="file"
          accept="application/pdf"
          onChange={(e) => setFile(e.target.files[0])}
          style={{ padding: "0.5rem" }}
        />
      </div>

      <button onClick={handleUpload}>Upload PDF</button>

      {error && <p style={{ color: "red", marginTop: "1rem" }}>{error}</p>}

      {response && (
        <div style={{ marginTop: "2rem" }}>
          <p><strong>✅ Success!</strong></p>
          <p><strong>Submission ID:</strong> {response.submission_id}</p>
          <p><strong>Status:</strong> {response.status}</p>
        </div>
      )}
    </div>
  );
};

export default WriterUpload;
