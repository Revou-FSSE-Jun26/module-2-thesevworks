# coding: utf-8
from app import db


class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    category_name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.FetchedValue())



class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    order_id = db.Column(db.ForeignKey('orders.id', ondelete='CASCADE'), nullable=False)
    product_id = db.Column(db.ForeignKey('products.id', ondelete='RESTRICT'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    price_at_purchase = db.Column(db.Numeric(10, 2), nullable=False)

    order = db.relationship('Order', primaryjoin='OrderItem.order_id == Order.id', backref='order_items')
    product = db.relationship('Product', primaryjoin='OrderItem.product_id == Product.id', backref='order_items')



class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    user_id = db.Column(db.ForeignKey('users.id'), nullable=False)
    total_amount = db.Column(db.Numeric(15, 2), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    ordered_at = db.Column(db.DateTime, server_default=db.FetchedValue())

    user = db.relationship('User', primaryjoin='Order.user_id == User.id', backref='orders')



class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    category_id = db.Column(db.ForeignKey('category.id'), nullable=False)
    product_name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.FetchedValue())

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

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(25), nullable=False, server_default="buyer")
    created_at = db.Column(db.DateTime, server_default=db.FetchedValue())

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

