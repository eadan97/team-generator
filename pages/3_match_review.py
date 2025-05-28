import streamlit as st
import pandas as pd
from utils.file_management import load_players

st.title("Match Review: Team Selection & Stats Update")

# Load players using the provided utility
if "players" not in st.session_state:
    st.session_state.players = load_players()

teams = df['team'].unique()
team_players = {}

# Select players for each team
st.header("Select Players for Each Team")
for team in teams:
    available_players = df[df['team'] == team]['name'].tolist()
    selected = st.multiselect(
        f"Select players for Team {team}",
        options=available_players,
        default=available_players
    )
    team_players[team] = selected

# Input goals for each team
st.header("Input Team Goals")
team_goals = {}
for team in teams:
    team_goals[team] = st.number_input(
        f"Goals scored by Team {team}",
        min_value=0,
        step=1,
        value=0
    )



if st.button("Submit"):
    updated_df = update_stats(team_players, team_goals)

    st.header("Player Stats Comparison")

    for team in teams:
        st.subheader(f"Team {team}")
        orig = df[df['name'].isin(team_players[team])].set_index('name')
        updated = updated_df[updated_df['name'].isin(team_players[team])].set_index('name')
        comparison = orig.join(updated, lsuffix='_old', rsuffix='_new')
        st.dataframe(comparison)
