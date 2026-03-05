import streamlit as st

def SideBarLinks(show_home: bool = True):
    """
    Minimal sidebar navigation for My MLB Passport.
    Keeps navigation independent from template RBAC pages.
    """

    # Optional logo (won't crash if missing)
    try:
        st.sidebar.image("assets/logo.png", width=150)
    except Exception:
        pass

    st.sidebar.title("Navigation")

    if show_home:
        st.sidebar.page_link("Home.py", label="Home", icon="🏠")

    st.sidebar.page_link("pages/01_Passport_MVP.py", label="Passport MVP", icon="⚾")

    # Optional: keep an about page if you want it; otherwise delete this line
    # If you delete the about page file, also delete/comment this link.
    st.sidebar.page_link("pages/30_About.py", label="About", icon="🧠")