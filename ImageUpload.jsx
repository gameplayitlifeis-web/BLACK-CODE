import React, { useState } from "react";

export default function ImageUpload() {
  const [file, setFile] = useState(null);

  const handleUpload = (e) => {
    const f = e.target.files[0];
    if (f) {
      setFile(URL.createObjectURL(f));
    }
  };

  return (
    <div>
      <h3>Visual Search</h3>
      <input type="file" accept="image/*" onChange={handleUpload} />
      {file && (
        <div style={{ marginTop: 10 }}>
          <img src={file} alt="uploaded" style={{ maxWidth: "100%", borderRadius: 8 }} />
        </div>
      )}
    </div>
  );
}