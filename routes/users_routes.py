from models import User
from flask import Blueprint, jsonify
# from validation import admin_required
from flask_jwt_extended import jwt_required 

users_bp = Blueprint('users', __name__)
@users_bp.route("/", methods=["GET"]) 
# @jwt_required() 
# @admin_required 
def get_users(): 
    users = User.query. all()

    return jsonify([ 
        user.to_dict() 
        for user in users ]), 200