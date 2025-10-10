import React from "react";
import EncryptForm from "./components/EncryptForm";
import DecryptForm from "./components/DecryptForm";
import LogsList from "./components/LogsList";

function App() {
  return (
    <div style={{ padding: "20px" }}>
      <h1>SecureLog Client</h1>
      <EncryptForm />
      <DecryptForm />
      <LogsList />
    </div>
  );
}

export default App;
