import sqlite3
from datetime import datetime

DB_NAME = "watermark.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # ---------------- USERS TABLE ----------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        unique_id_hash TEXT NOT NULL,
        signature_path TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    """)

    # ---------------- IMAGES TABLE ----------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS images (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        original_image_path TEXT NOT NULL,
        watermarked_image_path TEXT NOT NULL,
        watermark_seed TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        phash TEXT,
        uploaded_at TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    # ---------------- ROBUSTNESS RESULTS TABLE ----------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS robustness_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        image_id INTEGER NOT NULL,
        attack_type TEXT,
        severity TEXT,
        psnr REAL,
        ssim REAL,
        mse REAL,
        nc REAL,
        evaluated_at TEXT NOT NULL,
        FOREIGN KEY(image_id) REFERENCES images(id)
    )
    """)

    # ---------------- ATTACK LOGS TABLE ----------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attack_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        image_id INTEGER NOT NULL,
        suspicious_image_path TEXT NOT NULL,
        result TEXT,
        checked_at TEXT NOT NULL,
        FOREIGN KEY(image_id) REFERENCES images(id)
    )
    """)

    conn.commit()
    conn.close()
