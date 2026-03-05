import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout="wide", page_title="About — My MLB Passport")

SideBarLinks(show_home=True)

st.title("About My MLB Passport")

st.markdown(
    """
**My MLB Passport** is a personal project to track the Major League Baseball games you’ve attended and explore fun “passport-style” stats:

- Which players have you seen hit the most home runs?
- Does your team win more often when you’re in the stands?
- How many ballparks have you visited?

### How it works (at a high level)
- **Streamlit** provides the UI
- A **Flask REST API** handles data ingestion + queries
- **MySQL** stores users, games, and attendance data
- **Docker Compose** runs everything locally in containers

### Current build
Right now the app supports a minimal MVP flow:
1. Create a user
2. Add a game manually (temporary)
3. Mark that you attended the game
4. View your attended games list

Next steps will automate game lookup and ingestion using the MLB Stats API.
"""
)

st.subheader("Tech Stack")
st.markdown(
    """
- Streamlit (frontend)
- Flask (REST API)
- MySQL
- Docker / Docker Compose
"""
)

st.subheader("Project Status")
st.markdown(
    """
- ✅ Step 1: Containers + API/DB connectivity
- ✅ Step 2: MVP schema + API endpoints + MVP UI
- ⏳ Step 3: Authentication + user sessions
- ⏳ Step 4: Game selection by date (MLB Stats API)
- ⏳ Step 5: Boxscore ingestion + dashboards
"""
)