from flask import Blueprint, request, jsonify
from app import db
from models import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True)

    # 1. validate input data
    if not data:
        return jsonify({
            "success": False,
            "message": "Request body must be JSON"
        }), 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({
            "success": False,
            "message": "email and password are required"
        }), 400

    # 2. validate against database
    is_user = User.query.filter_by(email=email).first()

    if not is_user or not is_user.check_password(password):
        return jsonify({
            "success": False,
            "message": "wrong username/email/password"
        }), 401

    access_token = create_access_token(
        identity=str(is_user.id),
        additional_claims={
            "email": is_user.email,
            "role": is_user.role
        }
    )

    return jsonify({
        "success": True,
        "message": "Login successful",
        "token": access_token
    }), 200

@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    user_id = get_jwt_identity()          # str(user.id) dari klaim "sub"
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_dict()), 200
