from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from app.extensions import mongo
from flask_jwt_extended import create_access_token
from flask_pymongo.wrappers import Database
from typing import cast

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        # ✅ Safely parse incoming JSON
        data = request.get_json(force=True, silent=True) or {}

        email = data.get('email')
        password = data.get('password')
        role = data.get('role')

        if not all([email, password, role]):
            return jsonify({"error": "Missing required fields"}), 400

        collection_name = 'admins' if role == 'admin' else 'users'
        db = cast(Database, mongo.db)
        user = db[collection_name].find_one({"email": email})

        if not user:
            return jsonify({"error": "User not found"}), 404

        if check_password_hash(user.get('password', ''), password):
            access_token = create_access_token(identity={'email': email, 'role': role})
            return jsonify({"access_token": access_token}), 200

        return jsonify({"error": "Invalid credentials"}), 401

    except Exception as e:
        print("Login error:", e)
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


@auth_bp.route('/signup', methods=['POST'])
def signup():
    try:
        # ✅ Safe JSON parsing
        data = request.get_json(force=True, silent=True) or {}

        email = data.get('email')
        password = data.get('password')
        role = data.get('role', 'user')  # default to user

        if not all([email, password]):
            return jsonify({"error": "Missing required fields"}), 400

        db = cast(Database, mongo.db)
        collection_name = 'admins' if role == 'admin' else 'users'

        existing_user = db[collection_name].find_one({"email": email})
        if existing_user:
            return jsonify({"error": "Email already registered"}), 409

        # ✅ Hash the password
        hashed_password = generate_password_hash(password)
        user_data = {
            "email": email,
            "password": hashed_password,
            "role": role
        }

        db[collection_name].insert_one(user_data)

        # ✅ Create access token
        access_token = create_access_token(identity={'email': email, 'role': role})
        return jsonify({
            "message": "User created successfully",
            "access_token": access_token
        }), 201

    except Exception as e:
        print("Signup error:", e)
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
