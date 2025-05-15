import streamlit as st

from utils.file_management import load_players, save_players

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

if st.button("Save Changes"):
    player_table["Name"] = player_table["Name"].str.strip()
    player_table = player_table.dropna(subset=["Name"])
    if len(player_table) != player_table["Name"].nunique():
        st.error("Player names must be unique.")
    else:
        save_players(player_table)
        st.session_state.players = player_table
        st.success("Changes saved.")
