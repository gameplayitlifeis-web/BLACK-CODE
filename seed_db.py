from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)

# Explicitly pick the database
DB_NAME = os.getenv("DB_NAME", "retaildb")
db = client[DB_NAME]

products_collection = db["products"]

# ✅ Sample products
sample_products = [
    {
        "name": "Blue Cotton Kurta",
        "price": 1500,
        "category": "kurta",
        "shipping_cities": ["Pune", "Mumbai", "Delhi"],
        "image_url": "https://example.com/images/blue-kurta.jpg"
    },
    {
        "name": "Red Traditional Saree",
        "price": 4500,
        "category": "traditional dress",
        "shipping_cities": ["Pune", "Chennai"],
        "image_url": "https://example.com/images/red-saree.jpg"
    },
    {
        "name": "Casual Sneakers",
        "category": "casual shoes",
        "price": 2500,
        "shipping_cities": ["Mumbai", "Pune"],
        "occasion": ["daily wear", "casual"],
        "image_url": "https://example.com/sneakers.jpg"
    },
    {
        "name": "Wedding Sherwani",
        "price": 7000,
        "category": "traditional dress",
        "shipping_cities": ["Delhi", "Pune"],
        "image_url": "https://example.com/images/sherwani.jpg"
    }
]

def load_products():
    """Fetch all products (without MongoDB _id)."""
    return list(products_collection.find({}, {"_id": 0}))

def insert_sample_products(products):
    """Insert sample products if not already present."""
    for product in products:
        # avoid duplicates by name
        if not products_collection.find_one({"name": product["name"]}):
            products_collection.insert_one(product)

if __name__ == "__main__":
    insert_sample_products(sample_products)
    all_products = load_products()
    print(f"✅ Seed completed! {len(all_products)} products in database.")
