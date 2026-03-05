from flask import Blueprint, request, jsonify, make_response, current_app
from werkzeug.security import generate_password_hash
from backend.db_connection import db

passport_routes = Blueprint("passport_routes", __name__, url_prefix="/passport")


@passport_routes.post("/users")
def create_user():
    body = request.get_json(silent=True) or {}
    email = (body.get("email") or "").strip().lower()
    password = body.get("password") or ""

    if not email or not password:
        return make_response(jsonify({"error": "email and password are required"}), 400)

    password_hash = generate_password_hash(password)

    conn = db.connect()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO users (email, password_hash) VALUES (%s, %s);",
            (email, password_hash),
        )
        conn.commit()
        user_id = cur.lastrowid
        return make_response(jsonify({"user_id": user_id, "email": email}), 201)
    except Exception as e:
        conn.rollback()
        # likely duplicate email
        current_app.logger.exception("create_user failed")
        return make_response(jsonify({"error": "could not create user", "details": str(e)}), 400)
    finally:
        cur.close()
        conn.close()


@passport_routes.post("/games")
def create_game():
    body = request.get_json(silent=True) or {}

    mlb_game_pk = body.get("mlb_game_pk")
    game_date = body.get("game_date")  # 'YYYY-MM-DD'
    home_team = (body.get("home_team") or "").strip()
    away_team = (body.get("away_team") or "").strip()
    venue_name = (body.get("venue_name") or None)

    if not mlb_game_pk or not game_date or not home_team or not away_team:
        return make_response(jsonify({"error": "mlb_game_pk, game_date, home_team, away_team are required"}), 400)

    conn = db.connect()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            INSERT INTO games (mlb_game_pk, game_date, home_team, away_team, venue_name)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
              game_date=VALUES(game_date),
              home_team=VALUES(home_team),
              away_team=VALUES(away_team),
              venue_name=VALUES(venue_name);
            """,
            (mlb_game_pk, game_date, home_team, away_team, venue_name),
        )
        conn.commit()

        # fetch game_id
        cur.execute("SELECT game_id FROM games WHERE mlb_game_pk=%s;", (mlb_game_pk,))
        row = cur.fetchone()
        return make_response(jsonify({"game_id": row["game_id"], "mlb_game_pk": mlb_game_pk}), 201)
    except Exception as e:
        conn.rollback()
        current_app.logger.exception("create_game failed")
        return make_response(jsonify({"error": "could not create game", "details": str(e)}), 400)
    finally:
        cur.close()
        conn.close()


@passport_routes.post("/users/<int:user_id>/games/<int:game_id>")
def add_attendance(user_id: int, game_id: int):
    body = request.get_json(silent=True) or {}
    notes = body.get("notes")

    conn = db.connect()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO user_games (user_id, game_id, notes) VALUES (%s, %s, %s);",
            (user_id, game_id, notes),
        )
        conn.commit()
        return make_response(jsonify({"ok": True, "user_id": user_id, "game_id": game_id}), 201)
    except Exception as e:
        conn.rollback()
        current_app.logger.exception("add_attendance failed")
        return make_response(jsonify({"error": "could not add attendance", "details": str(e)}), 400)
    finally:
        cur.close()
        conn.close()


@passport_routes.get("/users/<int:user_id>/games")
def list_attended_games(user_id: int):
    conn = db.connect()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            SELECT
              g.game_id, g.mlb_game_pk, g.game_date, g.home_team, g.away_team, g.venue_name,
              ug.attended_at, ug.notes
            FROM user_games ug
            JOIN games g ON g.game_id = ug.game_id
            WHERE ug.user_id = %s
            ORDER BY g.game_date DESC;
            """,
            (user_id,),
        )
        rows = cur.fetchall()
        return make_response(jsonify({"user_id": user_id, "games": rows}), 200)
    finally:
        cur.close()
        conn.close()