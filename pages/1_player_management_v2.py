import streamlit as st

from utils.file_management import load_players, save_players
import pandas as pd

st.title("👤 Player Manager")

if "players" not in st.session_state:
    st.session_state.players = load_players()
    st.session_state.players = st.session_state.players.sort_values("Name").reset_index(
        drop=True
    )
if "show_success" in st.session_state:
    st.success(st.session_state.show_success)
    del st.session_state.show_success

selected_player_idx = st.session_state.get("selected_player_idx", 0)

st.header("Player stats")

col1, col2 = st.columns([4, 1], vertical_alignment="bottom")
with col1:
    # TODO: Fix the add new player button to work properly
    selected_player_name = st.selectbox(
        "Select a player to view and edit stats",
        options=st.session_state.players["Name"].tolist(),
        index=selected_player_idx,
    )
with col2:
    with st.popover("Add New Player", icon="➕"):
        st.write(
            "You can add a new player by entering their name below. "
            "Make sure the name is unique and does not already exist in the list."
        )
        st.text_input(
            "New Player Name",
            key="new_player_name",
            placeholder="Enter new player name",
        )
        if st.button("Add Player"):
            new_player_name = st.session_state.new_player_name.strip()
            if new_player_name == "":
                st.error("Player name cannot be empty.")
            elif new_player_name in st.session_state.players["Name"].values:
                st.error("Player already exists.")
            else:
                selected_player_name = new_player_name
                st.session_state.players = pd.concat(
                    [
                        st.session_state.players,
                        pd.Series(
                            {
                                "Name": new_player_name,
                                "Pace": 0,
                                "Shooting": 0,
                                "Passing": 0,
                                "Dribbling": 0,
                                "Defending": 0,
                                "Physical": 0,
                                "Diving": 0,
                                "Handling": 0,
                                "Kicking": 0,
                                "Reflexes": 0,
                                "Speed": 0,
                                "Positioning": 0,
                            }
                        )
                        .to_frame()
                        .T,
                    ],
                    ignore_index=True,
                )
                st.session_state.selected_player_idx = len(st.session_state.players) - 1
                st.session_state.show_success = f"Player '{new_player_name}' added successfully. Remember to add stats for the new player and save."
                st.rerun()


selected_player = st.session_state.players[
    st.session_state.players["Name"] == selected_player_name
].iloc[0]


st.subheader(f"Player: {selected_player['Name']}")
with st.expander("Goalkeeper Stats", expanded=False):
    cols = st.columns(6)
    for i, stat in enumerate(st.session_state.config["goalkeeper_stats"]):
        with cols[i]:
            selected_player[stat] = st.number_input(
                stat,
                min_value=0,
                max_value=100,
                value=int(selected_player[stat]),
                step=1,
                key=f"{stat.lower()}",
            )
with st.expander("Outfield Stats", expanded=False):
    cols = st.columns(6)
    for i, stat in enumerate(st.session_state.config["player_stats"]):
        with cols[i]:
            selected_player[stat] = st.number_input(
                stat,
                min_value=0,
                max_value=100,
                value=int(selected_player[stat]),
                step=1,
                key=f"{stat.lower()}",
            )


if st.button("Save Changes"):

    if selected_player["Name"].strip() == "":
        st.error("Player name cannot be empty.")
    else:
        idx = st.session_state.players[
            st.session_state.players["Name"] == selected_player_name
        ].index
        if not idx.empty:
            st.session_state.players.loc[idx[0]] = selected_player
            save_players(st.session_state.players)
            st.success(f"Player '{selected_player_name}' updated successfully.")
        else:
            st.error(f"Player '{selected_player_name}' not found.")

st.header("Goalkeeper Stats Summary")
goalkeeper_stats = st.session_state.config["goalkeeper_stats"]
gk_players = st.session_state.players[
    st.session_state.players[goalkeeper_stats].any(axis=1)
]
st.table(gk_players[goalkeeper_stats + ["Name"]].set_index("Name"))

st.header("Outfield Stats Summary")
player_stats = st.session_state.config["player_stats"]
outfield_players = st.session_state.players[
    st.session_state.players[player_stats].any(axis=1)
]
st.table(outfield_players[player_stats + ["Name"]].set_index("Name"))


# player_table = st.data_editor(st.session_state.players, num_rows="dynamic", key="player_table", column_config={
#     "Name": st.column_config.TextColumn("Name", required=True),
#     "Pace": st.column_config.NumberColumn("Pace", min_value=0, max_value=100, step=1),
#     "Shooting": st.column_config.NumberColumn("Shooting", min_value=0, max_value=100, step=1),
#     "Passing": st.column_config.NumberColumn("Passing", min_value=0, max_value=100, step=1),
#     "Dribbling": st.column_config.NumberColumn("Dribbling", min_value=0, max_value=100, step=1),
#     "Defending": st.column_config.NumberColumn("Defending", min_value=0, max_value=100, step=1),
#     "Physical": st.column_config.NumberColumn("Physical", min_value=0, max_value=100, step=1),
# })

if not st.session_state.players.empty:
    stats_columns = st.session_state.config["player_stats"]
    stats_table_df = st.session_state.players.copy()
    stats_table_df["Total Stats"] = stats_table_df.iloc[:, 1:].sum(axis=1).astype(int)
    stats_table_df["Average Stats"] = (stats_table_df["Total Stats"] / 6).round(2)
    stats_table_df = stats_table_df[["Name", "Total Stats", "Average Stats"]]
    stats_table_df = stats_table_df.sort_values(
        "Average Stats", ascending=False
    ).reset_index(drop=True)
    st.subheader("Stats Leaderboard")
    st.table(stats_table_df.set_index("Name"))

# if st.button("Save Changes"):
#     player_table["Name"] = player_table["Name"].str.strip()
#     player_table = player_table.dropna(subset=["Name"])
#     if len(player_table) != player_table["Name"].nunique():
#         st.error("Player names must be unique.")
#     else:
#         save_players(player_table)
#         st.session_state.players = player_table
#         st.success("Changes saved.")
