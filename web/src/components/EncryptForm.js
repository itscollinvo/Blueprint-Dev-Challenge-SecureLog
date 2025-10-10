import React, { useState } from "react";

export default function EncryptForm() {
  const [key, setKey] = useState("");
  const [data, setData] = useState("");
  const [result, setResult] = useState("");

  const handleEncrypt = async () => {
    try {
      const res = await fetch("http://localhost:8000/api/v1/encrypt", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ key, data }),
      });
      const json = await res.json();
      if (res.ok) setResult(json.data);
      else setResult(`Error: ${json.detail}`);
    } catch (e) {
      setResult(`Error: ${e.message}`);
    }
  };

  return (
    <div>
      <h2>Encrypt</h2>
      <textarea
        placeholder="Public Key"
        value={key}
        onChange={(e) => setKey(e.target.value)}
        rows={6}
        cols={50}
      />
      <br />
      <textarea
        placeholder="Data"
        value={data}
        onChange={(e) => setData(e.target.value)}
        rows={3}
        cols={50}
      />
      <br />
      <button onClick={handleEncrypt}>Encrypt</button>
      <div>
        <strong>Result:</strong>
        <pre>{result}</pre>
      </div>
    </div>
  );
}
