from flask import Blueprint, request, jsonify
from app import db
from models import User

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    #1. validasi input data
    
    #2. validasi ke database

    email = data.get("email"),
    password = data.get("password")

    is_user = User.query.filter_by(email = data.get("email")).first()

    is_true_user = is_user.check_password(password)

    if not is_true_user :
        return {
            "success" : False,
            "message" : "wrong username/email/password"
        }, 404


    return {
            "success" : True,
            "message" : "real user"
        }, 200