from flask import Blueprint, jsonify

health_bp = Blueprint("health", __name__, url_prefix="/api")

@health_bp.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok", "message": "CriptoRace API is running!"}), 200
