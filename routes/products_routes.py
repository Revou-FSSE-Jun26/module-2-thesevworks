from models import Product
from flask import Blueprint, jsonify
# from validation import admin_required
from flask_jwt_extended import jwt_required 

products_bp = Blueprint('products', __name__)
@products_bp.route("/", methods=["GET"]) 
# @jwt_required() 
# @admin_required 
def get_products(): 
    products = Product.query.all()
    return jsonify([ 
        product.to_dict() 
    for product in products ]), 200

@products_bp.route("/<int:product_id>", methods=["GET"])
def get_product_by_id(product_id):
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({"error": "Product not found"}), 404
        return jsonify(product.to_dict()), 200        
    except Exception as e : 
        return jsonify({"error": str(e)}), 500

# @product_bp.routes("/products", method=["POST"])
# def create_product():
#         data = request.get_json ()
#         try
#             new_product = Product(
#                 name=data['name'],
#                 description=data['description'],
#                 price=data['price'],
#                 stock=data['stock']
#             )
#             db.session.add(new_product)
#             db.session.commit()
#             return jsonify("message" : "new_product created",
#                             "product": new_product.to_dict(),
#                             "status": success),
#                              201
#         except Exception as e:
#             db.session.rollback()
#             print(f"Error creating product: {e}")
#             return jsonify({"message": "Error creating product",
#                             "product": "Not valid",
#                             "status": "error"}),
#                              400

