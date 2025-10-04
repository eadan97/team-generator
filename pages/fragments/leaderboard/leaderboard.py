import streamlit as st
import pandas as pd

from utils.file_management import load_players
from utils.players import get_average_stats_df

def get_players():
    players = get_average_stats_df(
        load_players(),
        st.session_state.config["Player Stats"],
    )
    players["Total"] = players.drop(["Name"], axis=1).mean(axis=1).round(2)
    players.sort_values(by="Total", ascending=False, inplace=True)
    players.set_index("Name", inplace=True)
    return players


def show_leaderboard(players):
    st.subheader("Players leaderboard")
    st.table(players.style.format(precision=2, subset=["Total"]))


def show_podiums(players: pd.DataFrame):
    st.subheader("🏅 Podiums")
    for col in players.columns:
        if col != "Total":
            with st.expander(f"{col} Podium", expanded=False):
                podium = players.nlargest(5, col)
                st.table(podium)
