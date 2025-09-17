from flask import Blueprint, request, jsonify
from backend import models
from pymongo import MongoClient
import os
import clip
import torch
from PIL import Image
import requests
from io import BytesIO
import numpy as np
import faiss

bp = Blueprint("visual_search", __name__)

# MongoDB
client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/"))
db = client[os.getenv("DB_NAME", "retail_assistant")]

# Load CLIP model
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

@bp.route("/visual_search", methods=["POST"])
def visual_search():
    """
    Accepts image file and returns top 5 similar products from DB.
    """
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    img_file = request.files["image"]
    try:
        image = Image.open(img_file).convert("RGB")
    except:
        return jsonify({"error": "Cannot read image"}), 400

    # Compute embedding
    with torch.no_grad():
        image_input = preprocess(image).unsqueeze(0).to(device)
        img_embedding = model.encode_image(image_input)
        img_embedding = img_embedding / img_embedding.norm(dim=-1, keepdim=True)
        img_embedding = img_embedding.cpu().numpy().astype("float32")

    # Load all product embeddings from MongoDB
    products = list(db.products.find({"embedding": {"$exists": True}}))
    if not products:
        return jsonify({"error": "No product embeddings found"}), 500

    embeddings = np.array([p["embedding"] for p in products])
    faiss_index = faiss.IndexFlatL2(embeddings.shape[1])
    faiss_index.add(embeddings)
    D, I = faiss_index.search(img_embedding, k=5)

    similar_products = [products[i] for i in I[0]]
    for p in similar_products:
        p.pop("_id", None)  # remove Mongo ID

    return jsonify({"results": similar_products})
