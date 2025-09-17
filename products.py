from flask import Blueprint, request, jsonify
from backend.models.db_client import products_collection

# ✅ Use __name__ here
bp = Blueprint("products", __name__)

@bp.route("/products/search", methods=["GET"])
def search_products():
    q = request.args.get("q", "")
    min_p = float(request.args.get("min_price", 0))
    max_p = float(request.args.get("max_price", 1e9))
    city = request.args.get("city")
    category = request.args.get("category")

    query = {"price": {"$gte": min_p, "$lte": max_p}}
    if q:
        query["$or"] = [
            {"title": {"$regex": q, "$options": "i"}},
            {"description": {"$regex": q, "$options": "i"}},
            {"tags": {"$regex": q, "$options": "i"}}
        ]
    if city:
        query["shipping_cities"] = city
    if category:
        query["category"] = {"$regex": category, "$options": "i"}

    docs = list(products_collection.find(query).limit(100))

    # Convert ObjectId -> string for JSON serialization
    for d in docs:
        d["_id"] = str(d["_id"])

    return jsonify(docs)