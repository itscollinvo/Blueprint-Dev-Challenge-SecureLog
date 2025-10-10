import React, { useState } from "react";

export default function DecryptForm() {
  const [key, setKey] = useState("");
  const [data, setData] = useState("");
  const [result, setResult] = useState("");

  const handleDecrypt = async () => {
    try {
      const res = await fetch("http://localhost:8000/api/v1/decrypt", {
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
      <h2>Decrypt</h2>
      <textarea
        placeholder="Private Key"
        value={key}
        onChange={(e) => setKey(e.target.value)}
        rows={6}
        cols={50}
      />
      <br />
      <textarea
        placeholder="Encrypted Data"
        value={data}
        onChange={(e) => setData(e.target.value)}
        rows={3}
        cols={50}
      />
      <br />
      <button onClick={handleDecrypt}>Decrypt</button>
      <div>
        <strong>Result:</strong>
        <pre>{result}</pre>
      </div>
    </div>
  );
}
