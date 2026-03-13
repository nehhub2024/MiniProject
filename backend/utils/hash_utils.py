import hashlib
import uuid


def generate_unique_id():
    return str(uuid.uuid4())


def hash_text(text):
    return hashlib.sha256(text.encode()).hexdigest()
