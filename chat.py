from flask import Blueprint, request, jsonify
from datetime import datetime

bp = Blueprint("chat", __name__)

# In-memory storage for chat history
chat_history = {}

# Simple multilingual responses
LANG_RESPONSES = {
    "hello": {
        "en": "Hello! How can I assist you today?",
        "ta": "வணக்கம்! எப்படி உதவலாம்?",
        "hi": "नमस्ते! मैं आपकी कैसे मदद कर सकता हूँ?",
        "de": "Hallo! Wie kann ich Ihnen helfen?",
        "jp": "こんにちは！何かお手伝いできますか？"
    },
    "default": {
        "en": "Hello! You said: {msg}",
        "ta": "நீங்கள் கூறியது: {msg}",
        "hi": "आपने कहा: {msg}",
        "de": "Sie sagten: {msg}",
        "jp": "あなたが言った: {msg}"
    }
}

# Function to detect language (basic keyword-based, can be replaced with AI)
def detect_language(message):
    msg_lower = message.lower()
    if any(w in msg_lower for w in ["vanakkam", "வணக்கம்"]):
        return "ta"
    elif any(w in msg_lower for w in ["hello", "hi"]):
        return "en"
    elif any(w in msg_lower for w in ["swagatam", "नमस्ते"]):
        return "hi"
    elif any(w in msg_lower for w in ["willkommen", "hallo"]):
        return "de"
    elif any(w in msg_lower for w in ["yokoso", "こんにちは"]):
        return "jp"
    return "en"  # default

@bp.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_id = data.get("user_id")
    message = data.get("message")

    if not user_id or not message:
        return jsonify({"error": "user_id and message required"}), 400

    lang = detect_language(message)
    reply_text = LANG_RESPONSES.get(message.lower(), LANG_RESPONSES["default"]).get(lang, LANG_RESPONSES["default"]["en"]).format(msg=message)

    bot_message = {
        "sender": "bot",
        "text": reply_text,
        "timestamp": datetime.now().isoformat()
    }

    # Save chat history
    if user_id not in chat_history:
        chat_history[user_id] = []
    chat_history[user_id].append({"sender": "user", "text": message, "timestamp": datetime.now().isoformat()})
    chat_history[user_id].append(bot_message)

    return jsonify({"reply": reply_text, "timestamp": bot_message["timestamp"]})

@bp.route("/chat/history", methods=["GET"])
def history():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "user_id required"}), 400
    return jsonify({"messages": chat_history.get(user_id, [])})
