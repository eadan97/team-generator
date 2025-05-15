import pandas as pd
import json

# Load the JSON file
with open('data/players.json', 'r') as f:
    players = json.load(f)

# Create a DataFrame
df = pd.DataFrame(players)

# Sum the numeric player stats
df['total_stats'] = df.iloc[:, 1:].sum(axis=1)

print("Total player stats:")
print(df.sort_values(by='total_stats', ascending=False))