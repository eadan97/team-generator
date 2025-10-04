import streamlit as st

from pages.fragments.leaderboard.changes_table import show_changes_table
from pages.fragments.leaderboard.leaderboard import get_players, show_leaderboard, show_podiums
from utils.file_management import get_bk_players_list

st.title("🏆 Leaderboard")

if "bk_files" not in st.session_state:
    st.session_state.bk_files = get_bk_players_list()
    st.session_state.bk_files.append("./data/players.json")


players = get_players()
show_leaderboard(players)
show_podiums(players)
show_changes_table()

# leaderboard_df = pd.DataFrame({
#     "Name": merged["Name"],
#     "Total Stats": [
#         format_total_change(merged["Total_before"].iloc[i], merged["Total_after"].iloc[i])
#         for i in range(len(merged))
#     ],
#     "Position Change": [format_position_change(merged["Position Change"].iloc[i]) for i in range(len(merged))]
# })

# # Sort by new rank
# leaderboard_df["Rank"] = merged["Rank_after"]
# leaderboard_df = leaderboard_df.sort_values("Rank").reset_index(drop=True)
# leaderboard_df = leaderboard_df[["Name", "Total Stats", "Position Change"]]

# st.subheader("Stats Leaderboard")
# st.write(leaderboard_df.to_html(escape=False, index=False), unsafe_allow_html=True)


