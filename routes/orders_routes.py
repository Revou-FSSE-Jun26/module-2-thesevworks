from models import Order
from flask import Blueprint, jsonify
# from validation import admin_required
from flask_jwt_extended import jwt_required 

orders_bp = Blueprint('orders', __name__)

@orders_bp.route("/", methods=["GET"]) 
# @jwt_required() 
# @admin_required 
def get_orders(): 
    orders = Order.query.all()
    
    return jsonify([ 
        order.to_dict() 
    for order in orders ]), 200


