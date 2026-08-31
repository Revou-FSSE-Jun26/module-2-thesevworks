from models import Order
from flask import Blueprint, jsonify, request
from app import db
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

@orders_bp.route("/<int:order_id>", methods=["GET"])
def get_order_by_id(order_id):
    try:
        order = Order.query.get(order_id)
        if order:
            return jsonify(order.to_dict()), 200
        else:
            return jsonify({"error": "Order not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@orders_bp.route("/", methods=["POST"]) 
def create_order():
    try:
        data = request.get_json()

        # validation
        if not data:
            return jsonify({"error": "Request body must be JSON"}), 400

        required_fields = ["user_id", "total_amount", "status"]
        missing = [field for field in required_fields if data.get(field) is None]
        if missing:
            return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

        try:
            total_amount = float(data["total_amount"])
        except (ValueError, TypeError):
            return jsonify({"error": "total_amount must be a number"}), 400

        if total_amount < 0:
            return jsonify({"error": "total_amount cannot be negative"}), 400

        new_order = Order(
            user_id=data["user_id"],
            total_amount=total_amount,
            status=data["status"]
        )

        db.session.add(new_order)
        db.session.commit()

        return jsonify({
            "message": "new_order created",
            "order": new_order.to_dict(),
            "status": "success"
        }), 201

    except Exception as e:
        db.session.rollback()
        print(f"Error creating order: {e}")
        return jsonify({
            "message": "Error creating Order",
            "order": "Not valid",
            "status": "error"
        }), 400
