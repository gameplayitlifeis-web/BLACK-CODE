from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Allow frontend to call backend

# Simple in-memory chat history
chat_history = {}

# Dummy products DB
products_db = [
    {"title": "Traditional Dress", "price": 4500, "occasion": ["wedding"], "image_url": "/placeholder.png", "city": "Pune"},
    {"title": "Modern Kurta", "price": 3000, "occasion": ["festival"], "image_url": "/placeholder.png", "city": "Delhi"},
]

@app.route("/")
def home():
    return jsonify({"status": "ok", "service": "retail_assistant backend"})

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_id = data.get("user_id")
    message = data.get("message")

    # Save user message
    if user_id not in chat_history:
        chat_history[user_id] = []
    chat_history[user_id].append({
        "sender": "user",
        "text": message,
        "timestamp": datetime.now().isoformat()
    })

    # Always reply with fixed text
    reply = {
        "sender": "bot",
        "text": "Hello! How can I assist you today?",
        "timestamp": datetime.now().isoformat(),
        "products": products_db
    }
    chat_history[user_id].append(reply)

    return jsonify(reply)

@app.route("/api/chat/history", methods=["GET"])
def history():
    user_id = request.args.get("user_id")
    messages = chat_history.get(user_id, [])
    return jsonify({"messages": messages})

@app.route("/api/chat/visual-search", methods=["POST"])
def visual_search():
    # Always return dummy products
    return jsonify({"products": products_db})

if __name__ == "__main__":
    print("🚀 Starting backend server...")
    app.run(host="0.0.0.0", port=5000, debug=True)

