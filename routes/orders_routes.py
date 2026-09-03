from models import Order, User
from flask import Blueprint, jsonify, request
from app import db
# from validation import admin_required
from flask_jwt_extended import jwt_required 

orders_bp = Blueprint('orders', __name__)

@orders_bp.route("/", methods=["GET"]) 
# @jwt_required() 
# @admin_required 
def get_orders(): 
    orders = Order.query.filter_by(is_deleted=False).all()

    return jsonify([ 
        order.to_dict() 
        for order in orders ]), 200

@orders_bp.route("/<int:order_id>", methods=["GET"])
def get_order_by_id(order_id):
    try:
        order = Order.query.get(order_id)
        if order and not order.is_deleted:
            return jsonify(order.to_dict()), 200
        else:
            return jsonify({"error": "Order not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@orders_bp.route("/", methods=["POST"]) 
def create_order():
    try:
        data = request.get_json(silent=True)

        # validation
        if not data:
            return jsonify({"error": "Request body must be JSON"}), 400

        required_fields = ["user_id", "total_amount", "status"]
        missing = [field for field in required_fields if data.get(field) is None]
        if missing:
            return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

        if not User.query.get(data["user_id"]):
            return jsonify({"error": "user_id does not exist"}), 400

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


@orders_bp.route("/<int:order_id>", methods=["PUT"])
def update_order(order_id):
    order = Order.query.get(order_id)
    if order is None:
        return jsonify({"error": "Order not found"}), 404

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    valid_statuses = ("pending", "shipped", "completed", "cancelled")

    # Partial update
    if data.get("status") is not None:
        if data["status"] not in valid_statuses:
            return jsonify({"error": f"status must be one of {valid_statuses}"}), 400
        order.status = data["status"]

    if data.get("total_amount") is not None:
        try:
            total_amount = float(data["total_amount"])
        except (ValueError, TypeError):
            return jsonify({"error": "total_amount must be a number"}), 400
        if total_amount < 0:
            return jsonify({"error": "total_amount cannot be negative"}), 400
        order.total_amount = total_amount

    try:
        db.session.commit()
        return jsonify({
            "message": "Order updated successfully",
            "order": order.to_dict(),
            "status": "ok"
        }), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error updating order: {e}")
        return jsonify({"error": "Error updating order"}), 500


@orders_bp.route("/<int:order_id>", methods=["DELETE"])
def delete_order(order_id):
    order = Order.query.get(order_id)
    if order is None or order.is_deleted:
        return jsonify({"message": "Order not found", "status": "error"}), 404

    try:
        order.is_deleted = True
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting order: {e}")
        return jsonify({"error": "Error deleting order"}), 500

    return jsonify({
        "message": "Order deleted successfully",
        "order": order.to_dict(),
        "status": "ok"
    }), 200
