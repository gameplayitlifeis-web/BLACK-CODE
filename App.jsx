import React from "react";
import ChatBox from "./components/ChatBox";
import ProductList from "./components/ProductList";
import ImageUpload from "./components/ImageUpload";

export default function App() {
  return (
    <div style={{ maxWidth: 1100, margin: "20px auto", fontFamily: "Arial, sans-serif" }}>
      <h2>Retail — Intelligent Personalized Shopping Assistant</h2>
      <div style={{ display: "grid", gridTemplateColumns: "1fr 420px", gap: 16 }}>
        <div style={{ background: "#fff", padding: 12, borderRadius: 8 }}>
          <ChatBox />
        </div>
        <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
          <div style={{ background: "#fff", padding: 12, borderRadius: 8 }}>
            <ProductList />
          </div>
          <div style={{ background: "#fff", padding: 12, borderRadius: 8 }}>
            <ImageUpload />
          </div>
        </div>
      </div>
    </div>
  );
}