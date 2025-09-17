# controllers/compute_embeddings.py

import os
import torch
import clip
from PIL import Image
import requests
from io import BytesIO
from pymongo import MongoClient

# ----------------- Config -----------------
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

# Connect to MongoDB
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "retail_assistant")
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
products_collection = db["products"]

# Load CLIP model
model, preprocess = clip.load("ViT-B/32", device=device)

# ----------------- Helper Functions -----------------
def load_image(url_or_path):
    """Load image from URL or local path and preprocess it for CLIP"""
    try:
        if url_or_path.startswith("http"):
            response = requests.get(url_or_path, timeout=10)
            img = Image.open(BytesIO(response.content)).convert("RGB")
        else:
            img = Image.open(url_or_path).convert("RGB")
        return preprocess(img).unsqueeze(0).to(device)
    except Exception as e:
        print("Failed to load image:", url_or_path, e)
        return None

def compute_embedding(image_tensor):
    """Compute CLIP image embedding"""
    with torch.no_grad():
        embedding = model.encode_image(image_tensor)
    return embedding.cpu().numpy()

def save_embedding(product_id, embedding):
    """Save embedding to MongoDB"""
    products_collection.update_one(
        {"id": product_id},
        {"$set": {"embedding": embedding.tolist()}}
    )

# ----------------- Main Loop -----------------
def main():
    products = list(products_collection.find())
    print(f"Found {len(products)} products in DB.")

    for product in products:
        image_url = product.get("image_url")
        if not image_url:
            print("Skipping product with no image:", product.get("id"))
            continue

        img_tensor = load_image(image_url)
        if img_tensor is None:
            print("Skipping product due to load failure:", product.get("id"))
            continue

        emb = compute_embedding(img_tensor)
        save_embedding(product.get("id"), emb)
        print("✅ Computed embedding for product:", product.get("title") or product.get("id"))

    print("✅ All embeddings computed and stored in MongoDB.")

# ----------------- Entry Point -----------------
if __name__ == "__main__":
    main()
