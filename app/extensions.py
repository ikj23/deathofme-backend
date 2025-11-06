from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from flask import Flask
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

mongo = PyMongo()
jwt = JWTManager()

def init_extensions(app: Flask):
    """
    Initialize all Flask extensions (PyMongo, JWT, etc.)
    """

    # Configure MongoDB connection using environment variable
    mongo_uri = os.getenv("MONGO_URI")

    if not mongo_uri:
        raise ValueError("❌ MONGO_URI not found in environment variables!")

    app.config["MONGO_URI"] = mongo_uri

    # Initialize extensions with Flask app
    mongo.init_app(app)
    jwt.init_app(app)

    print("✅ MongoDB connected successfully")
    print("✅ JWT initialized successfully")
