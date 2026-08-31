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
from routes.orders_routes import orders_bp
from routes.category_routes import category_bp
from routes.auth_routes import auth_bp


app.register_blueprint(products_bp, url_prefix="/products")
app.register_blueprint(users_bp, url_prefix="/users")
app.register_blueprint(orders_bp, url_prefix="/orders")
app.register_blueprint(category_bp, url_prefix="/category")
app.register_blueprint(auth_bp, url_prefix="/auth")


@app.route('/')
def home():
    return 'Welcome to Sevoshop!'


if __name__ == "__main__":
    app.run(debug=True)
