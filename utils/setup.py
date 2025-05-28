import streamlit as st
from utils import config

def setup():
    st.session_state.config = config.load_config("config.yml")
    # Define the pages
    main_page = st.Page("pages/main_page.py", title="Main Page", icon="🏠")
    page_1 = st.Page("pages/1_player_management.py", title="Player management", icon="👤")
    page_2 = st.Page("pages/2_team_generator.py", title="Team generator", icon="⚽")
    page_3 = st.Page("pages/4_match_log.py", title="Match log", icon="📋")
    leaderboard = st.Page("pages/5_leaderboard.py", title="Leaderboard", icon="🏆")

    # Set up navigation
    pg = st.navigation([main_page, page_1, page_2, page_3, leaderboard])