from models import Order, User, Product, OrderItem
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
    """Create an order. The client sends user_id and a list of items
    ({product_id, quantity}); the SERVER computes total_amount from the
    real product prices. The client cannot set total_amount directly.

    Expected body:
    {
        "user_id": 1,
        "items": [
            {"product_id": 2, "quantity": 1},
            {"product_id": 3, "quantity": 2}
        ]
    }
    """
    try:
        data = request.get_json(silent=True)

        # validation
        if not data:
            return jsonify({"error": "Request body must be JSON"}), 400

        user_id = data.get("user_id")
        items = data.get("items")

        if user_id is None:
            return jsonify({"error": "Missing required field: user_id"}), 400

        if not User.query.get(user_id):
            return jsonify({"error": "user_id does not exist"}), 400

        if not items or not isinstance(items, list):
            return jsonify({"error": "items must be a non-empty list of {product_id, quantity}"}), 400

        # Resolve each item, validate, and compute the total server-side.
        resolved = []
        total_amount = 0
        for item in items:
            product_id = item.get("product_id")
            quantity = item.get("quantity", 1)

            if product_id is None:
                return jsonify({"error": "each item requires a product_id"}), 400

            try:
                quantity = int(quantity)
            except (ValueError, TypeError):
                return jsonify({"error": f"quantity for product_id {product_id} must be an integer"}), 400

            if quantity <= 0:
                return jsonify({"error": f"quantity for product_id {product_id} must be greater than 0"}), 400

            product = Product.query.get(product_id)
            if product is None:
                return jsonify({"error": f"product_id {product_id} does not exist"}), 400

            if product.stock < quantity:
                return jsonify({"error": f"insufficient stock for product_id {product_id}"}), 400

            # total is computed from the ACTUAL product price, never from the client
            total_amount += float(product.price) * quantity
            resolved.append((product, quantity))

        # Create the order with the system-calculated total.
        new_order = Order(
            user_id=user_id,
            total_amount=total_amount,
            status=data.get("status", "pending")
        )
        db.session.add(new_order)
        db.session.flush()  # get new_order.id before creating items

        for product, quantity in resolved:
            db.session.add(OrderItem(
                order_id=new_order.id,
                product_id=product.id,
                quantity=quantity,
                price_at_purchase=product.price
            ))
            product.stock -= quantity  # decrement stock

        db.session.commit()

        return jsonify({
            "message": "new_order created",
            "order": new_order.to_dict(include_items=True),
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

    # total_amount is system-calculated and cannot be set by the client.
    if "total_amount" in data:
        return jsonify({"error": "total_amount is calculated by the system and cannot be set manually"}), 400

    # Only the order status can be updated here.
    if data.get("status") is not None:
        if data["status"] not in valid_statuses:
            return jsonify({"error": f"status must be one of {valid_statuses}"}), 400
        order.status = data["status"]

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
