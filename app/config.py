import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

class Config:
    # MongoDB Atlas Connection URI
    MONGO_URI = os.getenv("MONGO_URI")

    # MongoDB Database Name (used if MONGO_URI doesn't specify a database)
    MONGO_DBNAME = os.getenv("MONGO_DBNAME", "deathofme")

    # JWT Secret Key for authentication
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default-secret-key")

    # Optional: Allow CORS from any origin (useful for Vercel frontend)
    CORS_HEADERS = "Content-Type"

    # Optional: Flask Environment Settings
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

