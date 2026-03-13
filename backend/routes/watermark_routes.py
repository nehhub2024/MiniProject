from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.watermark_service import embed_image
from database import get_connection

watermark_bp = Blueprint("watermark", __name__)

@watermark_bp.route("/api/embed", methods=["POST"])
@jwt_required()
def embed():
    try:
        # Get logged-in user ID from JWT
        user_id = int(get_jwt_identity())

        # Get uploaded image
        image = request.files.get("image")
        if not image:
            return jsonify({"error": "Image file is required"}), 400

        # Fetch user unique hash
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT unique_id_hash FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        conn.close()

        if not user:
            return jsonify({"error": "User not found"}), 404

        # Call service layer
        result = embed_image(user_id, user["unique_id_hash"], image)

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500