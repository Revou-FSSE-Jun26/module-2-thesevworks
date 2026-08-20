from models import Product
from flask import Blueprint, jsonify
# from validation import admin_required
from flask_jwt_extended import jwt_required 

products_bp = Blueprint('products', __name__)
@products_bp.route("/", methods=["GET"]) 
# @jwt_required() 
# @admin_required 
def get_products(): 
    products = Product.query. all()
    return jsonify([ 
        product.to_dict() 
    for product in products ]), 200