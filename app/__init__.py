from flask import Flask
from app.extensions import mongo, jwt
from flask_cors import CORS
from app.routes.auth_routes import auth_bp
from app.routes.report_routes import report_bp
from .routes.admin_update_routes import admin_bp
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

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
    
    CORS(app, 
         resources={r"/api/*": {
             "origins": allowed_origins,
             "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
             "allow_headers": ["Content-Type", "Authorization", "X-Requested-With"],
             "supports_credentials": True,
             "max_age": 3600
         }},
         automatic_options=True
    )

    mongo.init_app(app)
    jwt.init_app(app)

    # Register routes
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(report_bp, url_prefix='/api')
    app.register_blueprint(admin_bp, url_prefix='/api')

    return app
