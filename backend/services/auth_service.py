import os
from datetime import datetime
from database import get_connection
from utils.hash_utils import generate_unique_id, hash_text
from flask_jwt_extended import create_access_token

SIGNATURE_FOLDER = "static/signatures"


def register_user(username, password, signature_file):
    conn = get_connection()
    cursor = conn.cursor()

    # Check if username already exists
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        conn.close()
        return {"error": "Username already exists"}

    # Hash password
    password_hash = hash_text(password)

    # Generate unique ID and hash it
    unique_id = generate_unique_id()
    unique_id_hash = hash_text(unique_id)

    # Save signature file
    signature_filename = f"{username}_signature.png"
    signature_path = os.path.join(SIGNATURE_FOLDER, signature_filename)

    signature_file.save(signature_path)

    # Insert into database
    cursor.execute("""
    INSERT INTO users (username, password_hash, unique_id_hash, signature_path, created_at)
    VALUES (?, ?, ?, ?, ?)
    """, (
        username,
        password_hash,
        unique_id_hash,
        signature_path,
        datetime.now()
    ))

    conn.commit()
    conn.close()

    return {"message": "User registered successfully"}


def login_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()

    if not user:
        conn.close()
        return {"error": "User not found"}

    password_hash = hash_text(password)

    if user["password_hash"] != password_hash:
        conn.close()
        return {"error": "Invalid password"}

    # Create JWT token
    access_token = create_access_token(identity=str(user["id"]))
    conn.close()

    return {
        "message": "Login successful",
        "access_token": access_token
    }