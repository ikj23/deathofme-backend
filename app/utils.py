"""
Utility functions for the application
"""
from flask_pymongo.wrappers import Database
from app.extensions import mongo
from typing import cast, Optional
import os

def get_database() -> Optional[Database]:
    """
    Safely get the database connection.
    If mongo.db is None (database not in URI), use mongo.cx to get it.
    """
    if mongo.db is not None:
        return cast(Database, mongo.db)
    
    # Fallback: if db is None, try to get it from the client
    # Use MONGO_DB_NAME env var or default to 'deathofme'
    if mongo.cx is not None:
        db_name = os.getenv('MONGO_DB_NAME', 'deathofme')
        return cast(Database, mongo.cx[db_name])
    
    return None

