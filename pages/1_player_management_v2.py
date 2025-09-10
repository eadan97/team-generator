import streamlit as st

from utils.file_management import load_players, save_players
import pandas as pd

st.title("👤 Player Manager")


def get_player_name_list():
    if "players" in st.session_state:
        return [player["Name"] for player in st.session_state.players]
    return []


def init_page():
    if "players" not in st.session_state:
        players = load_players()
        if players is None:
            st.warning("No players found. Please add players.")
        else:
            players = sorted(players, key=lambda x: x["Name"])
            st.session_state.players = players

    if "show_success" in st.session_state:  # TODO: Wtf is this?
        st.success(st.session_state.show_success)
        del st.session_state.show_success


init_page()


st.header("Player stats")

col1, col2, col3 = st.columns([6, 1, 1], vertical_alignment="bottom")
with col1:
    #     # TODO: Fix the add new player button to work properly
    selected_player = st.selectbox(
        "Select a player to view and edit stats",
        options=st.session_state.players,
        format_func=lambda x: x["Name"],
    )
with col2:
    with st.popover("Add New Player", icon="➕", width="stretch"):
        st.write(
            "Add a new player to the list. TO BE IMPLEMENTED."
        )  # TODO: Implement this
#         st.write(
#             "You can add a new player by entering their name below. "
#             "Make sure the name is unique and does not already exist in the list."
#         )
#         st.text_input(
#             "New Player Name",
#             key="new_player_name",
#             placeholder="Enter new player name",
#         )
#         if st.button("Add Player"):
#             new_player_name = st.session_state.new_player_name.strip()
#             if new_player_name == "":
#                 st.error("Player name cannot be empty.")
#             elif new_player_name in st.session_state.players["Name"].values:
#                 st.error("Player already exists.")
#             else:
#                 selected_player_name = new_player_name
#                 st.session_state.players = pd.concat(
#                     [
#                         st.session_state.players,
#                         pd.Series(
#                             {
#                                 "Name": new_player_name,
#                                 "Pace": 0,
#                                 "Shooting": 0,
#                                 "Passing": 0,
#                                 "Dribbling": 0,
#                                 "Defending": 0,
#                                 "Physical": 0,
#                                 "Diving": 0,
#                                 "Handling": 0,
#                                 "Kicking": 0,
#                                 "Reflexes": 0,
#                                 "Speed": 0,
#                                 "Positioning": 0,
#                             }
#                         )
#                         .to_frame()
#                         .T,
#                     ],
#                     ignore_index=True,
#                 )
#                 st.session_state.selected_player_idx = len(st.session_state.players) - 1
#                 st.session_state.show_success = f"Player '{new_player_name}' added successfully. Remember to add stats for the new player and save."
#                 st.rerun()
with col3:
    if st.button("Save Changes", type="primary", width="stretch"):
        # save_players(st.session_state.players)
        st.success("Player stats saved successfully.")
        # if st.button("Save Changes"):

#     if selected_player["Name"].strip() == "":
#         st.error("Player name cannot be empty.")
#     else:
#         idx = st.session_state.players[
#             st.session_state.players["Name"] == selected_player_name
#         ].index
#         if not idx.empty:
#             st.session_state.players.loc[idx[0]] = selected_player
#             save_players(st.session_state.players)
#             st.success(f"Player '{selected_player_name}' updated successfully.")
#         else:
#             st.error(f"Player '{selected_player_name}' not found.")

st.subheader(f"Player: {selected_player['Name']}")
# with st.expander("Goalkeeper Stats", expanded=False):
#     cols = st.columns(6)
#     for i, stat in enumerate(st.session_state.config["goalkeeper_stats"]):
#         with cols[i]:
#             selected_player[stat] = st.number_input(
#                 stat,
#                 min_value=0,
#                 max_value=100,
#                 value=int(selected_player[stat]),
#                 step=1,
#                 key=f"{stat.lower()}",
#             )
with st.expander("Outfield Stats", expanded=True):
    cols = st.columns(6)
    for i, stat in enumerate(st.session_state.config["Player Stats"]):
        stats_weights = st.session_state.config["Player Stats"][
            stat
        ]  # TODO: Add somewhere to validate they sum 100

        avg_stat = int(
            sum(
                [
                    st.session_state.get(
                        f"{stat.lower()}_{substat.lower()}",
                        selected_player["Stats"]["Outfield"][stat][substat],
                    )
                    * (stats_weights[substat] / 100)
                    for substat in stats_weights
                ]
            )
        )
        with cols[i % 6]:
            st.markdown(f"**{stat}**: {avg_stat}")
            for substat in selected_player["Stats"]["Outfield"][stat]:
                selected_player["Stats"]["Outfield"][stat][substat] = st.number_input(
                    substat,
                    min_value=0,
                    max_value=100,
                    value=int(selected_player["Stats"]["Outfield"][stat][substat]),
                    step=1,
                    key=f"{stat.lower()}_{substat.lower()}",
                )
#     for i, stat in enumerate(st.session_state.config["player_stats"]):
#         with cols[i]:
#             selected_player[stat] = st.number_input(
#                 stat,
#                 min_value=0,
#                 max_value=100,
#                 value=int(selected_player[stat]),
#                 step=1,
#                 key=f"{stat.lower()}",
#             )




# st.header("Goalkeeper Stats Summary")
# goalkeeper_stats = st.session_state.config["goalkeeper_stats"]
# gk_players = st.session_state.players[
#     st.session_state.players[goalkeeper_stats].any(axis=1)
# ]
# st.table(gk_players[goalkeeper_stats + ["Name"]].set_index("Name"))


def display_outfield_stats_summary():
    with st.expander("Outfield Stats Summary", expanded=False):
        st.header("Outfield Stats Summary")
        player_stats = st.session_state.config["Player Stats"]
        # outfield_players = st.session_state.players[
        #     st.session_state.players[player_stats].any(axis=1)
        # ]
        # outfield_stats_df = outfield_players[player_stats + ["Name"]].copy()
        # outfield_stats_df[player_stats] = outfield_stats_df[player_stats].round(0).astype(int)

        outfield_stats_dict = {
            player["Name"]: {
                substat: round(player["Stats"]["Outfield"][stat][substat])
                for stat in player_stats
                for substat in player["Stats"]["Outfield"][stat]
            }
            for player in st.session_state.players
        }
        outfield_stats_df = pd.DataFrame(outfield_stats_dict).T
        st.dataframe(outfield_stats_df)


display_outfield_stats_summary()

# if not st.session_state.players.empty:
#     stats_columns = st.session_state.config["player_stats"]
#     stats_table_df = st.session_state.players.copy()
#     stats_table_df["Total Stats"] = stats_table_df.iloc[:, 1:].sum(axis=1).astype(int)
#     stats_table_df["Average Stats"] = (stats_table_df["Total Stats"] / 6).round(2)
#     stats_table_df = stats_table_df[["Name", "Total Stats", "Average Stats"]]
#     stats_table_df = stats_table_df.sort_values(
#         "Average Stats", ascending=False
#     ).reset_index(drop=True)
#     st.subheader("Stats Leaderboard")
#     st.table(stats_table_df.set_index("Name"))
