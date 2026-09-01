from models import Category
from flask import Blueprint, jsonify, request
from app import db
# from validation import admin_required
from flask_jwt_extended import jwt_required 

category_bp = Blueprint('category', __name__)

@category_bp.route("/", methods=["GET"]) 
# @jwt_required() 
# @admin_required 
def get_categories(): 
    categories = Category.query.all()

    return jsonify([ 
        category.to_dict() 
        for category in categories ]), 200

@category_bp.route("/<int:category_id>", methods=["GET"])
def get_category_by_id(category_id):
    try:
        category = Category.query.get(category_id)
        if category:
            return jsonify(category.to_dict()), 200
        else:
            return jsonify({"error": "Category not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@category_bp.route("/", methods=["POST"]) 
def create_category():
    try:
        data = request.get_json(silent=True)

        # validation
        if not data:
            return jsonify({"error": "Request body must be JSON"}), 400

        category_name = data.get("category_name")
        if not category_name:
            return jsonify({"error": "Missing required field: category_name"}), 400

        if len(category_name) > 50:
            return jsonify({"error": "category_name must be 50 characters or fewer"}), 400

        if Category.query.filter_by(category_name=category_name).first():
            return jsonify({"error": "Category already exists"}), 409

        new_category = Category(
            category_name=category_name,
            description=data.get("description")
        )

        db.session.add(new_category)
        db.session.commit()

        return jsonify({
            "message": "new_category created",
            "category": new_category.to_dict(),
            "status": "success"
        }), 201

    except Exception as e:
        db.session.rollback()
        print(f"Error creating category: {e}")
        return jsonify({
            "message": "Error creating Category",
            "category": "Not valid",
            "status": "error"
        }), 400

@category_bp.route("/<int:category_id>", methods=["PUT"])
def update_category(category_id):
    category = Category.query.get(category_id)
    if category is None:
        return jsonify({"error": "Category not found"}), 404

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    # Partial update
    if data.get("category_name") is not None:
        category_name = data["category_name"]
        if len(category_name) > 50:
            return jsonify({"error": "category_name must be 50 characters or fewer"}), 400
        existing = Category.query.filter_by(category_name=category_name).first()
        if existing and existing.id != category.id:
            return jsonify({"error": "Category already exists"}), 409
        category.category_name = category_name

    if data.get("description") is not None:
        category.description = data["description"]

    try:
        db.session.commit()
        return jsonify({
            "message": "Category updated successfully",
            "category": category.to_dict(),
            "status": "ok"
        }), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error updating category: {e}")
        return jsonify({"error": "Error updating category"}), 500


@category_bp.route("/<int:category_id>", methods=["DELETE"])
def delete_category(category_id):
    category = Category.query.get(category_id)
    if category is None:
        return jsonify({"message": "Category not found", "status": "error"}), 404

    category_data = category.to_dict()

    try:
        db.session.delete(category)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting category: {e}")
        return jsonify({"error": "Error deleting category"}), 500

    return jsonify({
        "message": "Category deleted successfully",
        "category": category_data,
        "status": "ok"
    }), 200
