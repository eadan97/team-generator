import streamlit as st

st.set_page_config(
    page_title="Soccer Team Generator",
    page_icon="⚽",
    layout="wide",
)

st.title("⚽ Welcome to the Soccer Team Generator")

st.markdown("""
Use the sidebar to navigate between pages:

- 👤 **Player Manager**: Add, view, or update player data and positions.
- 🧠 **Team Generator**: Select available players and generate fair teams based on your rules.
""")
