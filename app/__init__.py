from flask import Flask, request, jsonify
from app.extensions import mongo, jwt
from flask_cors import CORS
from app.routes.auth_routes import auth_bp
from app.routes.report_routes import report_bp
from .routes.admin_update_routes import admin_bp
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    # Initialize MongoDB and JWT first
    mongo.init_app(app)
    jwt.init_app(app)

    # ✅ CORS configuration - Fixed: Cannot use supports_credentials with origins="*"
    # Get allowed origins from environment or use defaults
    frontend_url = os.getenv('FRONTEND_URL', 'https://menstrucare-frontend.vercel.app')
    allowed_origins = [
        frontend_url,
        "https://menstrucare-frontend.vercel.app",
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173"
    ]
    # Remove duplicates while preserving order
    allowed_origins = list(dict.fromkeys(allowed_origins))
    
    # Configure CORS - must be done before routes are registered
    CORS(app, 
         resources={r"/api/*": {
             "origins": allowed_origins,
             "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
             "allow_headers": ["Content-Type", "Authorization", "X-Requested-With"],
             "supports_credentials": True,
             "max_age": 3600
         }},
         automatic_options=True,
         supports_credentials=True
    )

    # Register routes first
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(report_bp, url_prefix='/api')
    app.register_blueprint(admin_bp, url_prefix='/api')

    # Add explicit OPTIONS handler as fallback for all API routes
    # This ensures preflight requests always return 200 OK even if Flask-CORS fails
    @app.route("/api/<path:path>", methods=["OPTIONS"])
    def handle_options(path):
        """Handle OPTIONS preflight requests for all API routes"""
        response = jsonify({})
        origin = request.headers.get("Origin")
        if origin in allowed_origins:
            response.headers.add("Access-Control-Allow-Origin", origin)
            response.headers.add("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS, PATCH")
            response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Requested-With")
            response.headers.add("Access-Control-Allow-Credentials", "true")
            response.headers.add("Access-Control-Max-Age", "3600")
        return response, 200

    return app
