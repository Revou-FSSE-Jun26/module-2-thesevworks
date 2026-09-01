from models import User
from flask import Blueprint, jsonify, request
from app import db
# from validation import admin_required
from flask_jwt_extended import jwt_required 

users_bp = Blueprint('users', __name__)

@users_bp.route("/", methods=["GET"]) 
# @jwt_required() 
# @admin_required 
def get_users(): 
    users = User.query.all()

    return jsonify([ 
        user.to_dict() 
        for user in users ]), 200

@users_bp.route("/<int:user_id>", methods=["GET"])
def get_user_by_id(user_id):
    try:
        user = User.query.get(user_id)
        if user:
            return jsonify(user.to_dict()), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e : 
        return jsonify({"error": str(e)}), 500

@users_bp.route("/", methods=["POST"]) 
def create_users():
    try:
        data = request.get_json()

        # validation
        if not data:
            return jsonify({"error": "Request body must be JSON"}), 400

        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        required_fields = {"username": username, "email": email, "password": password}
        missing = [field for field, value in required_fields.items() if not value]
        if missing:
            return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

        if "@" not in email or "." not in email:
            return jsonify({"error": "Invalid email format"}), 400

        if len(password) < 6:
            return jsonify({"error": "Password must be at least 6 characters"}), 400

        if User.query.filter_by(email=email).first():
            return jsonify({"error": "Email already registered"}), 409

        new_user = User(
            username=username,
            email=email
        )
        new_user.hashing_password(password)

        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            "message": "new_user created",
            "user": new_user.to_dict(),
            "status": "success"
        }), 201

    except Exception as e:
        db.session.rollback()
        print(f"Error creating user: {e}")
        return jsonify({
            "message": "Error creating User",
            "user": "Not valid",
            "status": "error"
        }), 400

@users_bp.route("/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    # Partial update
    if data.get("username") is not None:
        user.username = data["username"]

    if data.get("email") is not None:
        email = data["email"]
        if "@" not in email or "." not in email:
            return jsonify({"error": "Invalid email format"}), 400
        existing = User.query.filter_by(email=email).first()
        if existing and existing.id != user.id:
            return jsonify({"error": "Email already registered"}), 409
        user.email = email

    if data.get("role") is not None:
        user.role = data["role"]

    if data.get("password") is not None:
        if len(data["password"]) < 6:
            return jsonify({"error": "Password must be at least 6 characters"}), 400
        user.hashing_password(data["password"])

    try:
        db.session.commit()
        return jsonify({
            "message": "User updated successfully",
            "user": user.to_dict(),
            "status": "ok"
        }), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error updating user: {e}")
        return jsonify({"error": "Error updating user"}), 500


@users_bp.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"message": "User not found", "status": "error"}), 404

    user_data = user.to_dict()

    try:
        db.session.delete(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting user: {e}")
        return jsonify({"error": "Error deleting user"}), 500

    return jsonify({
        "message": "User deleted successfully",
        "user": user_data,
        "status": "ok"
    }), 200
