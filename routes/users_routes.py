from models import User
from flask import Blueprint, jsonify
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
