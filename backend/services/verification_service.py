import os
from datetime import datetime
from database import get_connection
from watermark_engine.watermark_system import WatermarkSystem
from watermark_engine.metrics import calculate_metrics

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SUSPICIOUS_FOLDER = os.path.join(BASE_DIR, "static", "suspicious")

os.makedirs(SUSPICIOUS_FOLDER, exist_ok=True)


def verify_image(user_id, image_id, suspicious_file):
    conn = get_connection()
    cursor = conn.cursor()

    # 1️⃣ Fetch original image + seed
    cursor.execute("""
        SELECT original_image_path, watermarked_image_path, watermark_seed
        FROM images
        WHERE id = ? AND user_id = ?
    """, (image_id, user_id))

    record = cursor.fetchone()

    if not record:
        conn.close()
        return {"error": "Image not found or unauthorized"}

    original_path = os.path.abspath(record["original_image_path"])
    watermarked_path = os.path.abspath(record["watermarked_image_path"])
    watermark_seed = record["watermark_seed"]
     

    
    # 2️⃣ Save suspicious image
    suspicious_filename = f"suspicious_{image_id}.png"
    suspicious_path = os.path.join(SUSPICIOUS_FOLDER, suspicious_filename)
    suspicious_file.save(suspicious_path)
    
    suspicious_path = os.path.abspath(suspicious_path)
    
    print("Original path:", original_path)
    print("Watermarked path:", watermarked_path)
    print("Suspicious path:", suspicious_path)

    # 3️⃣ Decode watermark
    system = WatermarkSystem()
    extracted_seed = system.decode(suspicious_path)

    # 4️⃣ Calculate metrics
    metrics = calculate_metrics(watermarked_path, suspicious_path)

    # 5️⃣ Calculate NC (seed match)
    nc = 1.0 if extracted_seed == watermark_seed else 0.0

    # 6️⃣ Store results
    cursor.execute("""
        INSERT INTO robustness_results
        (image_id, attack_type, severity, psnr, ssim, mse, nc, evaluated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        image_id,
        "Unknown",
        "Unknown",
        metrics["psnr"],
        metrics["ssim"],
        metrics["mse"],
        nc,
        datetime.now()
    ))

    conn.commit()
    conn.close()

    return {
        "message": "Verification completed",
        "psnr": metrics["psnr"],
        "ssim": metrics["ssim"],
        "mse": metrics["mse"],
        "nc": nc,
        "status": "Authentic" if nc == 1.0 else "Tampered"
    }