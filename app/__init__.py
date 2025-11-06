from flask import Flask
from app.extensions import mongo, jwt
from flask_cors import CORS
from app.routes.auth_routes import auth_bp
from app.routes.report_routes import report_bp
from .routes.admin_update_routes import admin_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    # ✅ CRITICAL FIX: Proper CORS configuration
    CORS(app, 
         resources={r"/api/*": {"origins": "*"}},  # Allow all origins for API routes
         allow_headers=["Content-Type", "Authorization"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         supports_credentials=True
    )

    mongo.init_app(app)
    jwt.init_app(app)

    # Register routes
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(report_bp, url_prefix='/api')
    app.register_blueprint(admin_bp, url_prefix='/api')

    return app