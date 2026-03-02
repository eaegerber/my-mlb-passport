from flask import Blueprint, jsonify, current_app
from backend.db_connection import db

health_bp = Blueprint("health", __name__)

@health_bp.get("/health")
def health():
    return jsonify({"status": "ok"})

@health_bp.get("/db/ping")
def db_ping():
    conn = db.connect()
    cur = conn.cursor()

    cur.execute("SELECT message, created_at FROM ping_test ORDER BY id DESC LIMIT 1;")
    row = cur.fetchone()

    cur.close()
    conn.close()

    return jsonify({
        "db": "ok",
        "latest_row": {
            "message": row["message"],
            "created_at": str(row["created_at"])
        }
    })