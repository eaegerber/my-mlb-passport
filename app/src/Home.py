##################################################
# My MLB Passport - Home
##################################################

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout="wide", page_title="My MLB Passport")

# Simple navigation (no RBAC)
SideBarLinks(show_home=False)

st.title("My MLB Passport")
st.write("Track the MLB games you've attended and explore fun stats from your personal baseball history.")

st.markdown("""
### What you can do right now
- Go to **Passport MVP** in the sidebar
- Create a test user
- Add a game manually (temporary)
- Mark attendance
- List your attended games

Next up: we’ll replace manual entry with game selection via the MLB Stats API.
""")