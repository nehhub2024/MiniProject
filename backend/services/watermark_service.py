# import os
# from datetime import datetime
# from database import get_connection
# from watermark_engine.watermark_system import WatermarkSystem

# # Absolute base path
# BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
# WATERMARKED_FOLDER = os.path.join(BASE_DIR, "static", "watermarked")
# SUSPICIOUS_FOLDER = os.path.join(BASE_DIR, "static", "suspicious")

# # Ensure folders exist
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# os.makedirs(WATERMARKED_FOLDER, exist_ok=True)


# def verify_image(user_id, image_id, suspicious_file):
#     conn = get_connection()
#     cursor = conn.cursor()

#     # Fetch original + watermarked image + seed
#     cursor.execute("""
#         SELECT original_image_path, watermarked_image_path, watermark_seed
#         FROM images
#         WHERE id = ? AND user_id = ?
#     """, (image_id, user_id))

#     record = cursor.fetchone()

#     if not record:
#         conn.close()
#         return {"error": "Image not found or unauthorized"}

#     # Convert DB paths to absolute
#     original_path = os.path.abspath(record["original_image_path"])
#     watermarked_path = os.path.abspath(record["watermarked_image_path"])
#     watermark_seed = record["watermark_seed"]

#     # ✅ CREATE suspicious_path FIRST
#     suspicious_filename = f"suspicious_{image_id}.png"
#     suspicious_path = os.path.join(SUSPICIOUS_FOLDER, suspicious_filename)

#     # Save file
#     suspicious_file.save(suspicious_path)

#     # Convert to absolute AFTER creation
#     suspicious_path = os.path.abspath(suspicious_path)

#     print("Original path:", original_path)
#     print("Watermarked path:", watermarked_path)
#     print("Suspicious path:", suspicious_path)

#     # Decode watermark
#     system = WatermarkSystem()
#     extracted_seed = system.decode(suspicious_path)

#     # Calculate metrics
#     metrics = calculate_metrics(watermarked_path, suspicious_path)

#     # Compare seed
#     nc = 1.0 if extracted_seed == watermark_seed else 0.0

#     # Store robustness results
#     cursor.execute("""
#         INSERT INTO robustness_results
#         (image_id, attack_type, severity, psnr, ssim, mse, nc, evaluated_at)
#         VALUES (?, ?, ?, ?, ?, ?, ?, ?)
#     """, (
#         image_id,
#         "Unknown",
#         "Unknown",
#         metrics["psnr"],
#         metrics["ssim"],
#         metrics["mse"],
#         nc,
#         datetime.now()
#     ))

#     conn.commit()
#     conn.close()

#     return {
#         "message": "Verification completed",
#         "psnr": metrics["psnr"],
#         "ssim": metrics["ssim"],
#         "mse": metrics["mse"],
#         "nc": nc,
#         "status": "Authentic" if nc == 1.0 else "Tampered"
#     }

import os
from datetime import datetime
from database import get_connection
from watermark_engine.watermark_system import WatermarkSystem

# Base directory
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
WATERMARKED_FOLDER = os.path.join(BASE_DIR, "static", "watermarked")

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(WATERMARKED_FOLDER, exist_ok=True)


def embed_image(user_id, user_hash, image_file):
    conn = get_connection()
    cursor = conn.cursor()

    # 1️⃣ Save original image
    original_filename = f"user_{user_id}_{image_file.filename}"
    original_path = os.path.join(UPLOAD_FOLDER, original_filename)
    image_file.save(original_path)

    # 2️⃣ Insert temporary DB record (generate image_id)
    cursor.execute("""
        INSERT INTO images (
            user_id,
            original_image_path,
            watermarked_image_path,
            watermark_seed,
            timestamp,
            uploaded_at
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        original_path,
        "",
        "",
        "",
        datetime.now()
    ))

    conn.commit()
    image_id = cursor.lastrowid

    # 3️⃣ Prepare watermarked path
    watermarked_filename = f"watermarked_{image_id}.png"
    watermarked_path = os.path.join(WATERMARKED_FOLDER, watermarked_filename)

    # 4️⃣ Call watermark engine
    system = WatermarkSystem()
    watermark_seed, timestamp = system.embed(
        original_path,
        watermarked_path,
        user_hash,
        image_id,
        None
    )

    # 5️⃣ Update DB with watermark info
    cursor.execute("""
        UPDATE images
        SET watermarked_image_path = ?,
            watermark_seed = ?,
            timestamp = ?
        WHERE id = ?
    """, (
        watermarked_path,
        watermark_seed,
        timestamp,
        image_id
    ))

    conn.commit()
    conn.close()

    # 6️⃣ Return response
    return {
        "message": "Image watermarked successfully",
        "image_id": image_id,
        "download_url": f"/static/watermarked/{watermarked_filename}"
    }