const BASE = process.env.REACT_APP_API_BASE || "http://localhost:5000/api";

export async function sendChat(userId, message) {
  const resp = await fetch(${BASE}/chat, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_id: userId, message })
  });
  return resp.json();
}

export async function searchProducts(q="", min_price=0, max_price=1000000, city="") {
  const params = new URLSearchParams({ q, min_price, max_price, city });
  const resp = await fetch(${BASE}/products/search?${params});
  return resp.json();
}