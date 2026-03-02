import os
from flask import Blueprint, jsonify
import mysql.connector

health_bp = Blueprint("health", __name__)

def get_db_conn():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "db"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE"),
    )

@health_bp.get("/health")
def health():
    return jsonify({"status": "ok"})

@health_bp.get("/db/ping")
def db_ping():
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("SELECT message, created_at FROM ping_test ORDER BY id DESC LIMIT 1;")
    row = cur.fetchone()
    cur.close()
    conn.close()

    return jsonify({
        "db": "ok",
        "latest_row": {"message": row[0], "created_at": str(row[1])}
    })