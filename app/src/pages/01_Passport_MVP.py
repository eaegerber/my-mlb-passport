import streamlit as st
import requests

API_BASE = "http://web-api:4000"  # docker-to-docker hostname

st.title("My MLB Passport — MVP")

st.subheader("Active selection")

col1, col2 = st.columns(2)

with col1:
    active_user_id = st.number_input(
        "Active user_id",
        min_value=1,
        value=int(st.session_state.get("user_id") or 1),
        step=1,
    )
    if st.button("Set active user"):
        st.session_state["user_id"] = int(active_user_id)
        st.session_state.pop("game_id", None)  # avoid linking new user to old game by accident

with col2:
    active_game_id = st.number_input(
        "Active game_id",
        min_value=1,
        value=int(st.session_state.get("game_id") or 1),
        step=1,
    )
    if st.button("Set active game"):
        st.session_state["game_id"] = int(active_game_id)

st.caption(f"Using user_id={st.session_state.get('user_id')} and game_id={st.session_state.get('game_id')}")
st.divider()


# -----------------------------
# Helpers
# -----------------------------
def api_get(path: str):
    url = f"{API_BASE}{path}"
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    return r.json()

def api_post(path: str, payload: dict | None = None):
    url = f"{API_BASE}{path}"
    r = requests.post(url, json=payload or {}, timeout=10)
    r.raise_for_status()
    return r.json()

# -----------------------------
# Health checks (optional but useful)
# -----------------------------
with st.expander("Connection checks", expanded=False):
    try:
        st.write("API /health:", api_get("/health"))
        st.write("API /db/ping:", api_get("/db/ping"))
        st.success("API + DB reachable")
    except Exception as e:
        st.error(f"Could not reach API/DB: {e}")

st.divider()

# -----------------------------
# 1) Create user
# -----------------------------
st.header("1) Create user (MVP)")

with st.form("create_user_form"):
    email = st.text_input("Email", value="test@example.com")
    password = st.text_input("Password", type="password", value="test123")
    create_user_btn = st.form_submit_button("Create user")

if create_user_btn:
    try:
        resp = api_post("/passport/users", {"email": email, "password": password})
        st.success(f"User created: {resp}")
        st.session_state["user_id"] = resp["user_id"]
        st.session_state.pop("game_id", None)
    except requests.HTTPError as e:
        st.error(f"API error: {e.response.status_code} {e.response.text}")
    except Exception as e:
        st.error(f"Error: {e}")

st.write("Current user_id:", st.session_state.get("user_id"))

st.divider()

# -----------------------------
# 2) Create game
# -----------------------------
st.header("2) Add game (manual for now)")

with st.form("create_game_form"):
    mlb_game_pk = st.number_input("MLB gamePk (int)", min_value=1, value=1, step=1)
    if int(mlb_game_pk) == 1:
        st.warning("Enter a real gamePk (we’ll automate this later via MLB Stats API).")
    game_date = st.date_input("Game date")
    home_team = st.text_input("Home team (e.g., NYY)", value="NYY")
    away_team = st.text_input("Away team (e.g., BOS)", value="BOS")
    venue_name = st.text_input("Venue (optional)", value="Yankee Stadium")
    create_game_btn = st.form_submit_button("Create / update game")

if create_game_btn:
    try:
        payload = {
            "mlb_game_pk": int(mlb_game_pk),
            "game_date": str(game_date),  # YYYY-MM-DD
            "home_team": home_team,
            "away_team": away_team,
            "venue_name": venue_name or None,
        }
        resp = api_post("/passport/games", payload)
        st.success(f"Game saved: {resp}")
        st.session_state["game_id"] = resp["game_id"]
    except requests.HTTPError as e:
        st.error(f"API error: {e.response.status_code} {e.response.text}")
    except Exception as e:
        st.error(f"Error: {e}")

st.write("Current game_id:", st.session_state.get("game_id"))

st.divider()

# -----------------------------
# 3) Mark attendance
# -----------------------------
st.header("3) Mark attendance (link user ↔ game)")

user_id = st.session_state.get("user_id")
game_id = st.session_state.get("game_id")

with st.form("attendance_form"):
    st.caption("This links the selected user_id and game_id in the database.")
    notes = st.text_input("Notes (optional)", value="Great game")
    attend_btn = st.form_submit_button("Mark attended")

if attend_btn:
    if not user_id or not game_id:
        st.warning("Create a user and a game first (need both user_id and game_id).")
    else:
        try:
            resp = api_post(f"/passport/users/{user_id}/games/{game_id}", {"notes": notes})
            st.success(f"Attendance saved: {resp}")
            resp_list = api_get(f"/passport/users/{user_id}/games")
            st.dataframe(resp_list.get("games", []), use_container_width=True)
        except requests.HTTPError as e:
            st.error(f"API error: {e.response.status_code} {e.response.text}")
        except Exception as e:
            st.error(f"Error: {e}")

st.divider()

# -----------------------------
# 4) List attended games
# -----------------------------
st.header("4) List attended games")

list_user_id = st.number_input(
    "User ID to list games for",
    min_value=1,
    value=int(st.session_state.get("user_id") or 1),
    step=1,
)

if st.button("Refresh attended games"):
    try:
        resp = api_get(f"/passport/users/{int(list_user_id)}/games")
        games = resp.get("games", [])
        st.write(f"Found {len(games)} games")
        st.dataframe(games, use_container_width=True)
    except requests.HTTPError as e:
        st.error(f"API error: {e.response.status_code} {e.response.text}")
    except Exception as e:
        st.error(f"Error: {e}")