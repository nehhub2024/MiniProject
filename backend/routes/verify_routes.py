from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.verification_service import verify_image

verify_bp = Blueprint("verify", __name__)

@verify_bp.route("/api/verify", methods=["POST"])
@jwt_required()
def verify():
    try:
        user_id = int(get_jwt_identity())

        image_id = request.form.get("image_id")
        suspicious_image = request.files.get("image")

        if not image_id or not suspicious_image:
            return jsonify({"error": "Image ID and suspicious image required"}), 400

        result = verify_image(user_id, int(image_id), suspicious_image)

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# from flask import Blueprint, request, jsonify
# from flask_jwt_extended import jwt_required, get_jwt_identity
# from services.watermark_service import embed_image
# from database import get_connection

# watermark_bp = Blueprint("watermark", __name__)

# @watermark_bp.route("/api/embed", methods=["POST"])
# @jwt_required()
# def embed():
#     try:
#         # 1️⃣ Get logged-in user from JWT
#         user_id = int(get_jwt_identity())

#         # 2️⃣ Get uploaded image
#         image = request.files.get("image")
#         if not image:
#             return jsonify({"error": "Image file is required"}), 400

#         # 3️⃣ Fetch user unique hash
#         conn = get_connection()
#         cursor = conn.cursor()
#         cursor.execute("SELECT unique_id_hash FROM users WHERE id = ?", (user_id,))
#         user = cursor.fetchone()
#         conn.close()

#         if not user:
#             return jsonify({"error": "User not found"}), 404

#         # 4️⃣ Call service layer
#         result = embed_image(user_id, user["unique_id_hash"], image)

#         return jsonify(result), 200

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500