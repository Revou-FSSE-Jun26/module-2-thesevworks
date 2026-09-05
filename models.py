# coding: utf-8
from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, server_default=db.func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "category_name": self.category_name,
            "description": self.description,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }



class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.ForeignKey('orders.id', ondelete='CASCADE'), nullable=False)
    product_id = db.Column(db.ForeignKey('products.id', ondelete='RESTRICT'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1, server_default=db.text("1"))
    price_at_purchase = db.Column(db.Numeric(10, 2), nullable=False)

    order = db.relationship('Order', primaryjoin='OrderItem.order_id == Order.id', backref='order_items')
    product = db.relationship('Product', primaryjoin='OrderItem.product_id == Product.id', backref='order_items')

    def to_dict(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "price_at_purchase": float(self.price_at_purchase) if self.price_at_purchase is not None else 0,
            "subtotal": float(self.price_at_purchase) * self.quantity if self.price_at_purchase is not None else 0,
        }



class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.ForeignKey('users.id'), nullable=False)
    total_amount = db.Column(db.Numeric(15, 2), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    ordered_at = db.Column(db.DateTime, default=datetime.utcnow, server_default=db.func.now())
    is_deleted = db.Column(db.Boolean, nullable=False, default=False, server_default=db.text("false"))

    user = db.relationship('User', primaryjoin='Order.user_id == User.id', backref='orders')

    def to_dict(self, include_items=False):
        data = {
            "id": self.id,
            "user_id": self.user_id,
            "total_amount": float(self.total_amount) if self.total_amount is not None else 0,
            "status": self.status,
            "ordered_at": self.ordered_at.isoformat() if self.ordered_at else None,
            "is_deleted": self.is_deleted
        }
        if include_items:
            data["items"] = [item.to_dict() for item in self.order_items]
        return data

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_id = db.Column(db.ForeignKey('category.id'), nullable=False)
    product_name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, server_default=db.func.now())

    category = db.relationship('Category', primaryjoin='Product.category_id == Category.id', backref='products')

    def to_dict(self):
        return {
            "id": self.id,
            "category_id": self.category_id,
            "product_name": self.product_name,
            "description": self.description,
            "price": self.price,
            "stock": self.stock,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(25), nullable=False, default="buyer", server_default="buyer")
    created_at = db.Column(db.DateTime, default=datetime.utcnow, server_default=db.func.now())

    def hashing_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
