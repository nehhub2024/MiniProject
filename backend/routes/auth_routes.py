from flask import Blueprint, request, jsonify
from services.auth_service import register_user
from services.auth_service import register_user, login_user

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/api/register", methods=["POST"])
def register():
    username = request.form.get("username")
    password = request.form.get("password")
    signature = request.files.get("signature")

    if not username or not password or not signature:
        return jsonify({"error": "All fields are required"}), 400

    result = register_user(username, password, signature)

    if "error" in result:
        return jsonify(result), 400

    return jsonify(result), 201


@auth_bp.route("/api/login", methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    result = login_user(username, password)

    if "error" in result:
        return jsonify(result), 401

    return jsonify(result), 200
