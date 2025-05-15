import streamlit as st

from utils.team_generation import generate_teams
from utils.file_management import load_players
import pandas as pd

# from utils import load_players_json
# from team_builder import generate_teams

st.title("⚽ Team Generator")

restricted_pairs = st.session_state.get("restricted_pairs", [])

if "players" not in st.session_state:
    st.session_state.players = load_players()

selected_players = st.multiselect(
    "Select players to include in the team generation",
    options=st.session_state.players["Name"].tolist(),
    default=st.session_state.players["Name"].tolist(),
)

st.write(f"Selected players: {len(selected_players)}")

gks = st.multiselect(
    "Select goalkeepers",
    options=selected_players,
)


with st.expander("### Player Pair Restrictions"):
    st.write("Select pairs of players who should NOT be on the same team:")

    # Prepare DataFrame for display
    pairs_df = pd.DataFrame(restricted_pairs, columns=["Player 1", "Player 2"])
    if not pairs_df.empty:
        pairs_df["Remove"] = "Remove"

    # Add a checkbox column for selection
    if not pairs_df.empty:
        pairs_df["Delete?"] = False

    edited_df = st.data_editor(
        pairs_df,
        key="restricted_pairs_table",
        column_config={
            "Player 1": st.column_config.TextColumn("Player 1", required=True),
            "Player 2": st.column_config.TextColumn("Player 2", required=True),
            "Delete?": st.column_config.CheckboxColumn("Delete?", required=False),
        },
        disabled=["Player 1", "Player 2"],
    )

    # Remove selected rows when user clicks "Delete Selected"
    if not edited_df.empty and st.button("Delete Selected"):
        to_delete = edited_df[edited_df["Delete?"]].index.tolist()
        for idx in sorted(to_delete, reverse=True):
            restricted_pairs.pop(idx)
        st.session_state["restricted_pairs"] = restricted_pairs
        st.rerun()

    col1, col2 = st.columns(2)
    with col1:
        player1 = st.selectbox(
            "Player 1", options=selected_players, key="restrict_player1"
        )
    with col2:
        player2 = st.selectbox(
            "Player 2",
            options=[p for p in selected_players if p != player1],
            key="restrict_player2",
        )
    if st.button("Add Restriction"):
        pair = tuple(sorted([player1, player2]))
        if player1 != player2 and pair not in restricted_pairs:
            restricted_pairs.append(pair)
            st.session_state["restricted_pairs"] = restricted_pairs
            st.rerun()
        else:
            st.error("Invalid pair or pair already exists.")
    st.write(f"Restricted pairs: {len(restricted_pairs)}")


col1, col2 = st.columns(2)
with col1:
    team_size = st.number_input(
        "Team Size", min_value=4, max_value=11, value=5, step=1, format="%d"
    )
with col2:
    num_variations = st.number_input(
        "Number of variations", min_value=1, max_value=10, value=1, step=1, format="%d"
    )

if st.button("Generate Teams"):
    selected_players_df = st.session_state.players[
        st.session_state.players["Name"].isin(selected_players)
    ].reset_index(drop=True)

    # TODO: fix this when the goalkeepers are added
    # selected_players_df.loc[selected_players_df["Name"].isin(gks), ["DEF", "MID", "FWD"]] = 0
    variations = generate_teams(
        selected_players_df,
        team_size,
        restricted_pairs,
        st.session_state.config["player_stats"],
        n_solutions=num_variations,
    )
    if variations is None:
        st.error("No valid teams could be generated with the current restrictions.")
    else:
        st.session_state.variations = variations
        tabs = st.tabs(
            [f"Variation {i+1}" for i in range(len(variations))]
        )

        for i, tab in enumerate(tabs):
            with tab:
                st.subheader(f"Variation {i+1}")
                selected_var_list = variations[i][1]

                teams_dfs = []
                for i in range(2): # TODO: change this to a max value of selected_var_list
                    st.subheader(f"Team {i+1}")
                    team_df = selected_players_df[[x == i for x in selected_var_list]].reset_index(drop=True)
                    st.table(team_df)
                    teams_dfs.append(team_df[st.session_state.config["player_stats"]].sum())

                summary_df = pd.DataFrame(
                    teams_dfs, index=[f"Team {i+1}" for i in range(len(teams_dfs))]
                )
                summary_df["Total"] = summary_df.sum(axis=1)
                diff = summary_df.iloc[0] - summary_df.iloc[1]
                diff["Total"] = diff.sum()
                summary_df.loc["Diff"] = diff
                st.table(summary_df)
