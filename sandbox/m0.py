import json
import pandas as pd

PLAYER_STATS = ["Pace", "Shooting", "Passing", "Dribbling", "Defending", "Physical"]


with open('data/bks/players_m1_m2.json', 'r') as f:
    player_data = json.load(f)
player_data_df = pd.DataFrame(player_data)

team_1=["Dan", "Mauro", "Rolo", "Teclas"]
team_2=["Adan", "Artavia", "Bryan", "Charlie", "Josue"]

team_1_df = player_data_df[player_data_df["Name"].isin(team_1)].reset_index(drop=True)
team_2_df = player_data_df[player_data_df["Name"].isin(team_2)].reset_index(drop=True)

team_1_stats = team_1_df[PLAYER_STATS].mean()
team_2_stats = team_2_df[PLAYER_STATS].mean()

teams_dfs = [team_1_stats, team_2_stats]


summary_df = pd.DataFrame(
    teams_dfs, index=[f"Team {i+1}" for i in range(len(teams_dfs))]
)

summary_df["Total"] = summary_df.sum(axis=1)
diff = summary_df.iloc[0] - summary_df.iloc[1]
diff["Total"] = diff.sum()
summary_df.loc["Diff"] = diff

print("\n\nMatch 1 Summary:")
print(team_1_df)
print(team_2_df)
print(summary_df)


with open('data/bks/players_m1_m2.json', 'r') as f:
    player_data = json.load(f)
player_data_df = pd.DataFrame(player_data)

team_1=["Adan", "Andrey", "Birrita", "Rolo", "Teclas"]
team_2=["Artavia", "Bryan", "Chris", "Mauro", "Undrik"]

team_1_df = player_data_df[player_data_df["Name"].isin(team_1)].reset_index(drop=True)
team_2_df = player_data_df[player_data_df["Name"].isin(team_2)].reset_index(drop=True)

team_1_stats = team_1_df[PLAYER_STATS].sum()
team_2_stats = team_2_df[PLAYER_STATS].sum()

teams_dfs = [team_1_stats, team_2_stats]


summary_df = pd.DataFrame(
    teams_dfs, index=[f"Team {i+1}" for i in range(len(teams_dfs))]
)

summary_df["Total"] = summary_df.sum(axis=1)
diff = summary_df.iloc[0] - summary_df.iloc[1]
diff["Total"] = diff.sum()
summary_df.loc["Diff"] = diff

print("\n\nMatch 2 Summary:")
print(team_1_df)
print(team_2_df)
print(summary_df)