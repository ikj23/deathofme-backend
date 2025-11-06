from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

from app.extensions import init_extensions
from app.routes.auth_routes import auth_bp
from app.routes.report_routes import report_bp
from app.routes.admin_update_routes import admin_bp


def create_app():
    # Load environment variables
    load_dotenv()

    app = Flask(__name__)

    # Load config from Config class
    app.config.from_object("app.config.Config")

    # Enable CORS for all routes
    CORS(app)

    # Initialize extensions (MongoDB, JWT)
    init_extensions(app)

    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(report_bp, url_prefix="/api")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")

    print("✅ Flask app initialized successfully")
    return app
