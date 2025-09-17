import React, { useState, useEffect, useRef } from "react";

export default function ChatBox() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [visualResults, setVisualResults] = useState([]);
  const chatEndRef = useRef(null);
  const USER_ID = "123";

  const scrollToBottom = () => chatEndRef.current?.scrollIntoView({ behavior: "smooth" });

  // Load dummy chat history
  useEffect(() => {
    const dummyHistory = [
      { sender: "bot", text: "Hello! How can I assist you today?", timestamp: new Date().toISOString() }
    ];
    setMessages(dummyHistory);
  }, []);

  useEffect(scrollToBottom, [messages, visualResults]);

  const sendMessage = () => {
    if (!input.trim()) return;

    const userMessage = { sender: "user", text: input, timestamp: new Date().toISOString() };
    setMessages(prev => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    // Dummy bot response
    setTimeout(() => {
      const botMessage = { sender: "bot", text: `I received: "${input}"`, timestamp: new Date().toISOString() };
      setMessages(prev => [...prev, botMessage]);
      setLoading(false);
    }, 800);
  };

  // Dummy visual search
  const handleVisualSearch = e => {
    const file = e.target.files[0];
    if (!file) return;

    const dummyProducts = [
      { image_url: "/placeholder.png", title: "Traditional Dress", price: 4500 },
      { image_url: "/placeholder.png", title: "Modern Kurta", price: 3000 }
    ];
    setVisualResults(dummyProducts);
  };

  return (
    <div style={{ border: "1px solid #ddd", borderRadius: 10, padding: 12, height: 700, display: "flex", flexDirection: "column", background: "#f9f9f9" }}>
      
      <div style={{ flex: 1, overflowY: "auto", marginBottom: 10 }}>
        {messages.map((msg, i) => (
          <div key={i} style={{ textAlign: msg.sender === "user" ? "right" : "left", margin: "10px 0" }}>
            <span style={{ display: "inline-block", padding: "8px 12px", borderRadius: 12, background: msg.sender === "user" ? "#0078FF" : "#eee", color: msg.sender === "user" ? "#fff" : "#000", maxWidth: "70%", wordWrap: "break-word" }}>
              {msg.text}
            </span>
            <div style={{ fontSize: "0.7rem", color: "#666", marginTop: 2 }}>{msg.timestamp ? new Date(msg.timestamp).toLocaleTimeString() : ""}</div>
          </div>
        ))}

        {loading && <div style={{ fontStyle: "italic", color: "#0078FF" }}>Assistant is typing...</div>}

        {visualResults.length > 0 && (
          <div>
            <h4>Visual Search Results:</h4>
            <div style={{ display: "flex", flexWrap: "wrap", gap: 12 }}>
              {visualResults.map((p, idx) => (
                <div key={idx} style={{ border: "1px solid #ccc", borderRadius: 8, padding: 8, width: 160, textAlign: "center", background: "#fff" }}>
                  <img src={p.image_url} alt={p.title} style={{ width: "100%", height: 100, objectFit: "cover", borderRadius: 6 }} />
                  <div style={{ fontWeight: "bold", marginTop: 5 }}>{p.title}</div>
                  <div style={{ color: "#0078FF", marginTop: 2 }}>₹{p.price}</div>
                </div>
              ))}
            </div>
          </div>
        )}

        <div ref={chatEndRef} />
      </div>

      <div style={{ display: "flex", gap: 8, marginBottom: 10 }}>
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === "Enter" && sendMessage()}
          placeholder="Type a message..."
          style={{ flex: 1, padding: "8px 10px", borderRadius: 8, border: "1px solid #ccc" }}
        />
        <button onClick={sendMessage} style={{ padding: "8px 16px", borderRadius: 8, background: "#0078FF", color: "#fff", border: "none", cursor: "pointer" }}>
          Send
        </button>
      </div>

      <div>
        <label style={{ marginRight: 8, fontWeight: "bold" }}>Visual Search:</label>
        <input type="file" accept="image/*" onChange={handleVisualSearch} />
      </div>
    </div>
  );
}
