from flask import Flask
from flask_cors import CORS
from database import init_db
from routes.auth_routes import auth_bp
from flask_jwt_extended import JWTManager
from routes.watermark_routes import watermark_bp
from routes.verify_routes import verify_bp


# Create Flask app
app = Flask(__name__)

# Enable CORS (so React can connect later)
CORS(app)

#Secret Key for JWT
app.config["JWT_SECRET_KEY"] = "super-secret-key-change-this"

jwt = JWTManager(app)

#Register BP
app.register_blueprint(auth_bp)
app.register_blueprint(watermark_bp)
app.register_blueprint(verify_bp)

@app.route("/")
def home():
    return "Watermark Backend Running!"

if __name__ == "__main__":
    init_db()          # Create tables automatically
    app.run(host="0.0.0.0", port=5000, debug=True)
