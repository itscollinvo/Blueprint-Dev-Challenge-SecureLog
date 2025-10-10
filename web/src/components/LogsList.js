import React, { useEffect, useState } from "react";

export default function LogsList() {
  const [logs, setLogs] = useState([]);
  const [size, setSize] = useState(5);
  const [offset, setOffset] = useState(0);

  const fetchLogs = async () => {
    try {
      const res = await fetch(
        `http://localhost:8000/api/v1/logs?size=${size}&offset=${offset}`
      );
      const json = await res.json();
      setLogs(json);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    fetchLogs();
  }, [size, offset]);

  return (
    <div>
      <h2>Logs</h2>
      <label>
        Size:{" "}
        <input
          type="number"
          value={size}
          onChange={(e) => setSize(Number(e.target.value))}
        />
      </label>
      <label>
        Offset:{" "}
        <input
          type="number"
          value={offset}
          onChange={(e) => setOffset(Number(e.target.value))}
        />
      </label>
      <button onClick={fetchLogs}>Refresh</button>
      <ul>
        {logs.map((log) => (
          <li key={log.id}>
            <strong>{log.id}</strong> - {new Date(log.timestamp * 1000).toLocaleString()} -{" "}
            {log.data}
          </li>
        ))}
      </ul>
    </div>
  );
}
