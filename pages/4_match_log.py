import streamlit as st
from datetime import datetime
import uuid
from utils.file_management import load_players

st.title("Match Log")

# Match Info
st.header("Match Information")
match_date = st.date_input("Date", value=datetime.today())
match_id = str(uuid.uuid4())

# Load all players (returns a DataFrame)
if "players" not in st.session_state:
    st.session_state.players = load_players()

all_players = st.session_state.players["Name"].tolist()

# Team Rosters (select from loaded players)
st.header("Team Rosters")

if "team_a_players" not in st.session_state:
    st.session_state["team_a_players"] = []
if "team_b_players" not in st.session_state:
    st.session_state["team_b_players"] = []

st.subheader("Players for Team A")
team_a_players = st.multiselect(
    "Select players for Team A",
    options=all_players,
    key="team_a_players",
    default=st.session_state["team_a_players"],
    max_selections=len(all_players)
)

remaining_players = [p for p in all_players if p not in team_a_players]
st.subheader("Players for Team B")
team_b_players = st.multiselect(
    "Select players for Team B",
    options=remaining_players,
    key="team_b_players",
    default=st.session_state["team_b_players"],
    max_selections=len(remaining_players)
)

# Goals
goals_a = st.number_input("Goals (Team A)", min_value=0, step=1)
goals_b = st.number_input("Goals (Team B)", min_value=0, step=1)

# Players' Stats Before Match
st.header("Players' Stats Before Match")
st.write("Stats for each player (from database):")

def player_stats_section(players, team_label):
    stats = {}
    for player in players:
        if player:
            st.subheader(f"{team_label} - {player}")
            row = players_df[players_df["name"] == player].iloc[0] if "name" in players_df.columns else players_df.loc[player]
            default_goals = int(row["goals"]) if "goals" in row else 0
            default_assists = int(row["assists"]) if "assists" in row else 0
            default_matches = int(row["matches"]) if "matches" in row else 0
            st.write(f"Goals: {default_goals}")
            st.write(f"Assists: {default_assists}")
            st.write(f"Matches: {default_matches}")
            stats[player] = {
                "goals": default_goals,
                "assists": default_assists,
                "matches": default_matches
            }
    return stats

team_a_stats = player_stats_section(team_a_players, "A")
team_b_stats = player_stats_section(team_b_players, "B")

# Estimated Minutes Played
st.header("Estimated Minutes Played Per Player")
def minutes_played_section(players, team_label):
    minutes = {}
    for player in players:
        if player:
            min_played = st.number_input(f"{team_label} - {player} Minutes Played", min_value=0, step=1, key=f"{team_label}_{player}_minutes")
            minutes[player] = min_played
    return minutes

team_a_minutes = minutes_played_section(team_a_players, "A")
team_b_minutes = minutes_played_section(team_b_players, "B")

# Submit
if st.button("Log Match"):
    st.success("Match logged successfully!")
    st.write({
        "date": match_date,
        "match_id": match_id,
        "rosters": {
            "A": team_a_players,
            "B": team_b_players
        },
        "goals": {
            "A": goals_a,
            "B": goals_b
        },
        "stats_before": {
            "A": team_a_stats,
            "B": team_b_stats
        },
        "minutes_played": {
            "A": team_a_minutes,
            "B": team_b_minutes
        }
    })
