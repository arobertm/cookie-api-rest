from flask import Blueprint, jsonify
from app.auth.routes import token_required

v1_bp = Blueprint('v1', __name__)

# Simulăm o bază de date de produse
products_db = {
    1: {"id": 1, "name": "Produs 1", "price": 100},
    2: {"id": 2, "name": "Produs 2", "price": 200}
}

@v1_bp.route('/products', methods=['GET'])
@token_required
def get_products(current_user):
    # V1 returnează doar date de bază
    basic_products = [{
        "id": p["id"],
        "name": p["name"],
        "price": p["price"]
    } for p in products_db.values()]
    return jsonify(basic_products)