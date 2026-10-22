from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS

migrate = Migrate()
app = Flask(__name__)
load_dotenv()

# Allow the frontend (local dev + deployed Vercel site) to call this API.
# Reads a comma-separated list from CORS_ORIGINS, defaults to "*" (all origins).
cors_origins = os.getenv("CORS_ORIGINS", "*")
CORS(
    app,
    resources={r"/*": {"origins": [o.strip() for o in cors_origins.split(",")]}},
    supports_credentials=True,
)

# PostgreSQL connection:
# DATABASE_URL=postgresql+psycopg2://postgres:password@localhost:5432/revoshop_db
database_url = os.getenv("DATABASE_URL")

if not database_url:
    raise RuntimeError("DATABASE_URL is not set. Create a .env file first.")

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Engine options untuk deployment (Render + Supabase pooler).
# Platform hosting seperti Render menutup koneksi TCP yang idle; tanpa
# pemeriksaan, SQLAlchemy memakai koneksi mati dan request gagal dengan 500
# (mis. "SSL connection has been closed unexpectedly").
#   - pool_pre_ping : uji koneksi sebelum dipakai; ganti otomatis jika mati.
#   - pool_recycle  : daur ulang koneksi lebih tua dari 280 detik (< batas idle).
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_pre_ping": True,
    "pool_recycle": 280,
}

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
