import React, { useState, useEffect } from "react";

export default function ProductList() {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    // In real case: fetch from backend API
    setProducts([
      { id: 1, name: "Traditional Dress", price: 4500, location: "Pune" },
      { id: 2, name: "Modern Kurta", price: 3000, location: "Delhi" },
    ]);
  }, []);

  return (
    <div>
      <h3>Recommended Products</h3>
      {products.map((p) => (
        <div key={p.id} style={{ padding: 8, borderBottom: "1px solid #ddd" }}>
          <strong>{p.name}</strong> <br />
          Price: ₹{p.price} <br />
          Ships to: {p.location}
        </div>
      ))}
    </div>
  );
}