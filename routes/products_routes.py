from models import Product, Category
from flask import Blueprint, jsonify, request
from app import db
# from validation import admin_required
from flask_jwt_extended import jwt_required 

products_bp = Blueprint('products', __name__)

@products_bp.route("/", methods=["GET"]) 
# @jwt_required() 
# @admin_required 
def get_products(): 
    products = Product.query.all()
    return jsonify([ 
        product.to_dict() 
    for product in products ]), 200

@products_bp.route("/<int:product_id>", methods=["GET"])
def get_product_by_id(product_id):
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({"error": "Product not found"}), 404
        return jsonify(product.to_dict()), 200        
    except Exception as e : 
        return jsonify({"error": str(e)}), 500

@products_bp.route("/", methods=["POST"])
def create_product():
    try:
        data = request.get_json(silent=True)

        # validation
        if not data:
            return jsonify({"error": "Request body must be JSON"}), 400

        required_fields = ["category_id", "product_name", "price", "stock"]
        missing = [field for field in required_fields if data.get(field) is None]
        if missing:
            return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

        try:
            price = float(data["price"])
            stock = int(data["stock"])
        except (ValueError, TypeError):
            return jsonify({"error": "price must be a number and stock must be an integer"}), 400

        if price < 0 or stock < 0:
            return jsonify({"error": "price and stock cannot be negative"}), 400

        new_product = Product(
            category_id=data["category_id"],
            product_name=data["product_name"],
            description=data.get("description"),
            price=price,
            stock=stock
        )
        db.session.add(new_product)
        db.session.commit()

        return jsonify({
            "message": "new_product created",
            "product": new_product.to_dict(),
            "status": "success"
        }), 201

    except Exception as e:
        db.session.rollback()
        print(f"Error creating product: {e}")
        return jsonify({
            "message": "Error creating product",
            "product": "Not valid",
            "status": "error"
        }), 400


@products_bp.route('/<int:product_id>', methods=['PUT'])
# @roles_required('seller')
def update_product(product_id):
    product = Product.query.get(product_id)
    if product is None:
        return jsonify({"error": "Product not found"}), 404

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    # Partial update
    if data.get('product_name') is not None:
        product.product_name = data['product_name']

    if data.get('description') is not None:
        product.description = data['description']

    if data.get('price') is not None:
        try:
            price = float(data['price'])
        except (ValueError, TypeError):
            return jsonify({"error": "price must be a number"}), 400
        if price < 0:
            return jsonify({"error": "price cannot be negative"}), 400
        product.price = price

    if data.get('stock') is not None:
        try:
            stock = int(data['stock'])
        except (ValueError, TypeError):
            return jsonify({"error": "stock must be an integer"}), 400
        if stock < 0:
            return jsonify({"error": "stock cannot be negative"}), 400
        product.stock = stock

    if data.get('category_id') is not None:
        category = Category.query.get(data['category_id'])
        if not category:
            return jsonify({"error": "Category not found"}), 404
        product.category_id = data['category_id']

    try:
        db.session.commit()
        return jsonify({
            "message": "Product updated successfully",
            "product": product.to_dict(),
            "status": "ok"
        }), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error updating product: {e}")
        return jsonify({"error": "Error updating product"}), 500


@products_bp.route('/<int:product_id>', methods=['DELETE'])
# @roles_required('admin')
def delete_product(product_id):
    product = Product.query.get(product_id)
    if product is None:
        return jsonify({"message": "Product not found", "status": "error"}), 404

    # Serialize before deleting so we can return the details in the response
    product_data = product.to_dict()

    try:
        db.session.delete(product)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting product: {e}")
        return jsonify({"error": "Error deleting product"}), 500

    return jsonify({
        "message": "Product deleted successfully",
        "product": product_data,
        "status": "ok"
    }), 200
