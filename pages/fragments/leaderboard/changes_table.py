import streamlit as st
import pandas as pd

from utils.file_management import load_players
from utils.players import get_average_stats_df

def show_changes_table():
    st.subheader("Files to compare")
    col1, col2 = st.columns(2)
    with col1:
        new_file = st.selectbox("Select new file", options=st.session_state.bk_files, index=len(st.session_state.bk_files)-1)
    with col2:
        old_file = st.selectbox("Select old file", options=st.session_state.bk_files, index=len(st.session_state.bk_files)-2)

    old_player_stats = load_players(old_file)
    new_player_stats = load_players(new_file)
    try:
        if "Stats" in old_player_stats[0]:
            old_player_stats = get_average_stats_df(old_player_stats, st.session_state.config["Player Stats"])
        else:
            old_player_stats = pd.DataFrame(old_player_stats)
    except Exception as e:
        st.error(f"Error loading player data from {old_file}: {e}")
    try:
        if "Stats" in new_player_stats[0]:
            new_player_stats = get_average_stats_df(new_player_stats, st.session_state.config["Player Stats"])
        else:
            new_player_stats = pd.DataFrame(new_player_stats)
    except Exception as e:
        st.error(f"Error loading player data from {new_file}: {e}")

    # Keep only columns present in both dataframes (excluding "Name")
    common_stats = [col for col in old_player_stats.columns if col in new_player_stats.columns and col != "Name"]
    
    old_player_stats = old_player_stats[["Name"] + common_stats]
    new_player_stats = new_player_stats[["Name"] + common_stats]

    # Assume both players1 and players2 have the same structure and "Name" column
    merged = pd.merge(old_player_stats, new_player_stats, on="Name", suffixes=("_before", "_after"), how="right").fillna(0)
    stats_columns = [col for col in old_player_stats.columns if col != "Name"]

    def format_change(before, after):
        if before == after:
            return f"{int(after)}"
        elif after > before:
            return f"<s>{int(before)}</s> {int(after)} <span style='color:green;'>⬆️</span>"
        else:
            return f"<s>{int(before)}</s> {int(after)} <span style='color:red;'>⬇️</span>"

    display_df = pd.DataFrame()
    display_df["Name"] = merged["Name"]
    for stat in stats_columns:
        display_df[stat] = [
            format_change(merged[f"{stat}_before"].iloc[i], merged[f"{stat}_after"].iloc[i])
            for i in range(len(merged))
        ]

    st.markdown("### Player Stats Comparison")
    st.write(display_df.to_html(escape=False, index=False), unsafe_allow_html=True)

    # Calculate total stats for before and after
    merged["Total_before"] = merged[[f"{stat}_before" for stat in common_stats]].sum(axis=1)
    merged["Total_after"] = merged[[f"{stat}_after" for stat in common_stats]].sum(axis=1)

    # Get rankings before and after
    merged["Rank_before"] = merged["Total_before"].rank(ascending=False, method="min").astype(int)
    merged["Rank_after"] = merged["Total_after"].rank(ascending=False, method="min").astype(int)

    # Calculate position change (positive means moved up)
    merged["Position Change"] = merged["Rank_before"] - merged["Rank_after"]

    # Format position change with emoji
    def format_position_change(change):
        if change > 0:
            return f"+{change} <span style='color:green;'>⬆️</span>"
        elif change < 0:
            return f"{change} <span style='color:red;'>⬇️</span>"
        else:
            return "0"

    # Format total stats with streakthrough and emoji
    def format_total_change(before, after):
        if before == after:
            return f"{int(after)}"
        elif after > before:
            return f"<s>{int(before)}</s> {int(after)} <span style='color:green;'>⬆️</span>"
        else:
            return f"<s>{int(before)}</s> {int(after)} <span style='color:red;'>⬇️</span>"
        
    leaderboard_df = pd.DataFrame({
        "Name": merged["Name"],
        "Total Stats": [
            format_total_change(merged["Total_before"].iloc[i], merged["Total_after"].iloc[i])
            for i in range(len(merged))
        ],
        "Position Change": [format_position_change(merged["Position Change"].iloc[i]) for i in range(len(merged))]
    })

    # Sort by new rank
    leaderboard_df["Rank"] = merged["Rank_after"]
    leaderboard_df = leaderboard_df.sort_values("Rank").reset_index(drop=True)
    leaderboard_df = leaderboard_df[["Name", "Total Stats", "Position Change"]]

    st.subheader("Stats Leaderboard")
    st.write(leaderboard_df.to_html(escape=False, index=False), unsafe_allow_html=True)