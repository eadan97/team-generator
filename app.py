import streamlit as st

from utils import config

st.session_state.config = config.load_config("config.yml")
# Define the pages
main_page = st.Page("pages/main_page.py", title="Main Page", icon="🏠")
page_2 = st.Page("pages/1_player_management.py", title="Player management", icon="👤")
page_3 = st.Page("pages/2_team_generator.py", title="Team generator", icon="⚽")

# Set up navigation
pg = st.navigation([main_page, page_2, page_3])

# Run the selected page
pg.run()