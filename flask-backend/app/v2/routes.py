from flask import Blueprint, jsonify, request
from app.auth.routes import token_required

v2_bp = Blueprint('v2', __name__)

@v2_bp.route('/products', methods=['GET'])
@token_required
def get_products(current_user):
    # V2 include mai multe detalii și funcționalități
    search = request.args.get('search', '').lower()
    category = request.args.get('category')
    
    products = products_db.values()
    
    if search:
        products = [p for p in products if search in p["name"].lower()]
    if category:
        products = [p for p in products if p.get("category") == category]
        
    return jsonify(list(products))

@v2_bp.route('/products/<int:product_id>', methods=['GET'])
@token_required
def get_product(current_user, product_id):
    product = products_db.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product)