import streamlit as st

from utils.file_management import load_players, save_players
import pandas as pd

st.title("👤 Player Manager")

if "players" not in st.session_state:
    st.session_state.players = load_players()
    st.session_state.players = st.session_state.players.sort_values("Name").reset_index(drop=True)
    

st.subheader("Current Players")
player_table = st.data_editor(st.session_state.players, num_rows="dynamic", key="player_table", column_config={
    "Name": st.column_config.TextColumn("Name", required=True),
    "Pace": st.column_config.NumberColumn("Pace", min_value=0, max_value=100, step=1),
    "Shooting": st.column_config.NumberColumn("Shooting", min_value=0, max_value=100, step=1),
    "Passing": st.column_config.NumberColumn("Passing", min_value=0, max_value=100, step=1),
    "Dribbling": st.column_config.NumberColumn("Dribbling", min_value=0, max_value=100, step=1),
    "Defending": st.column_config.NumberColumn("Defending", min_value=0, max_value=100, step=1),
    "Physical": st.column_config.NumberColumn("Physical", min_value=0, max_value=100, step=1),
})

if not player_table.empty:
    stats_columns = st.session_state.config["player_stats"]
    stats_table_df = player_table.copy()
    stats_table_df['Total Stats'] = stats_table_df.iloc[:, 1:].sum(axis=1).astype(int)
    stats_table_df['Average Stats'] = (stats_table_df['Total Stats'] / 6).round(2)
    stats_table_df = stats_table_df[["Name", "Total Stats", "Average Stats"]]
    stats_table_df = stats_table_df.sort_values("Average Stats", ascending=False).reset_index(drop=True)
    st.subheader("Stats Leaderboard")
    st.table(stats_table_df.set_index("Name"))

if st.button("Save Changes"):
    player_table["Name"] = player_table["Name"].str.strip()
    player_table = player_table.dropna(subset=["Name"])
    if len(player_table) != player_table["Name"].nunique():
        st.error("Player names must be unique.")
    else:
        save_players(player_table)
        st.session_state.players = player_table
        st.success("Changes saved.")
