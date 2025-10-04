import streamlit as st

from utils.file_management import load_players, save_players
import pandas as pd

st.title("👤 Player Manager")


def init_page():
    st.session_state.changed_stats = st.session_state.get("changed_stats", set())
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


def update_player_with_ui_stats():
    print("Updating player with UI stats...")
    print(f"Changed stats: {st.session_state.changed_stats}")
    print(f"Player name: {st.session_state.players[selected_player_idx]['Name']}")

    for stat, substat in st.session_state.changed_stats:
        st.session_state.players[selected_player_idx]["Stats"]["Outfield"][stat][
            substat
        ] = st.session_state.get(
            f"{stat.lower()}_{substat.lower()}",
            st.session_state.players[selected_player_idx]["Stats"]["Outfield"][stat][
                substat
            ],
        )
    st.session_state.changed_stats = set()


st.header("Player stats")
cols = st.columns([6, 1, 1, 1], vertical_alignment="bottom")
with cols[0]:
    selected_player_idx, selected_player = st.selectbox(
        "Select a player to view and edit stats",
        options=enumerate(st.session_state.players),
        format_func=lambda x: x[1]["Name"],
        on_change=update_player_with_ui_stats,
    )
with cols[1]:
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
with cols[2]:
    if st.button("Save Changes", type="primary", width="stretch"):
        update_player_with_ui_stats()
        if save_players(st.session_state.players):
            st.success("Players updated successfully.")
        else:
            st.error("Error updating players.")

with cols[3]:
    if st.button("Cancel Changes", type="secondary", width="stretch"):
        del st.session_state.players
        del st.session_state.changed_stats
        init_page()
        st.info("Changes canceled.")
        st.rerun()

st.subheader(f"Player: {selected_player['Name']}")

with st.expander("Outfield Stats", expanded=True):
    cols = st.columns(6)
    for i, stat in enumerate(st.session_state.config["Player Stats"]):
        stats_weights = st.session_state.config["Player Stats"][
            stat
        ]  # TODO: Add somewhere to validate they sum 100

        avg_stat = int(
            sum(
                [
                    (
                        st.session_state.get(f"{stat.lower()}_{substat.lower()}")
                        if (stat, substat) in st.session_state.changed_stats
                        else selected_player["Stats"]["Outfield"][stat][substat]
                    )
                    * (stats_weights[substat] / 100)
                    for substat in stats_weights
                ]
            )
        )
        with cols[i % 6]:
            st.markdown(f"**{stat}**: {avg_stat}")
            for substat in selected_player["Stats"]["Outfield"][stat]:
                st.number_input(
                    substat,
                    on_change=lambda stat, substat: st.session_state.changed_stats.add(
                        (stat, substat)
                    ),
                    min_value=0,
                    max_value=100,
                    value=int(selected_player["Stats"]["Outfield"][stat][substat]),
                    step=1,
                    key=f"{stat.lower()}_{substat.lower()}",
                    args=(stat, substat),
                )


def display_outfield_stats_summary():
    with st.expander("Outfield Stats Summary", expanded=False):
        st.header("Outfield Stats Summary")
        player_stats = st.session_state.config["Player Stats"]

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
