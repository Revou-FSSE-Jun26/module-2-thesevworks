from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

migrate = Migrate()
app = Flask(__name__)
load_dotenv()

# PostgreSQL connection:
# DATABASE_URL=postgresql+psycopg2://postgres:password@localhost:5432/revoshop_db
database_url = os.getenv("DATABASE_URL")

if not database_url:
    raise RuntimeError("DATABASE_URL is not set. Create a .env file first.")

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

jwt = JWTManager(app)
db = SQLAlchemy(app)
migrate.init_app(app,db)

from routes.products_routes import products_bp
from routes.users_routes import users_bp
# from auth_routes import auth_bp


app.register_blueprint(products_bp, url_prefix="/products")
app.register_blueprint(users_bp, url_prefix="/users")
# app.register_blueprint(auth_bp, url_prefix="/auth")


# ---------------------------------------------------------
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Flask is connected to PostgreSQL!", "status": "ok"})

@app.route('/category')
def category():
    return 'List of all category goes here'

@app.route('/orders')
def orders():
    return 'List of all orders goes here'

@app.route('/orders_item')
def orders_item():
    return 'List of all orders_item goes here'
    
@app.route('/products')
def products():
    return 'List of all products goes here'

@app.route('/users')
def users():
    return 'List of all users goes here'


if __name__ == "__main__":
    app.run(debug=True)
