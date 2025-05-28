import streamlit as st

from utils.file_management import get_bk_players_list, load_players, save_players
import pandas as pd

st.title("🏆 Leaderboard")

if "bk_files" not in st.session_state:
    st.session_state.bk_files = get_bk_players_list()
    st.session_state.bk_files.append("players.json")

st.subheader("Files to compare")
col1, col2 = st.columns(2)
with col1:
    file1 = st.selectbox("Select File 1", options=st.session_state.bk_files)
with col2:
    file2 = st.selectbox("Select File 2", options=st.session_state.bk_files)

players1 = load_players(file1)
players2 = load_players(file2)

# Assume both players1 and players2 have the same structure and "Name" column
merged = pd.merge(players1, players2, on="Name", suffixes=("_before", "_after"), how="outer").fillna(0)
stats_columns = [col for col in players1.columns if col != "Name"]

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

stats_columns = st.session_state.config["player_stats"]
# Calculate total stats for before and after
merged["Total_before"] = merged[[f"{stat}_before" for stat in stats_columns]].sum(axis=1)
merged["Total_after"] = merged[[f"{stat}_after" for stat in stats_columns]].sum(axis=1)

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
