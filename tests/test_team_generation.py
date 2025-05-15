import unittest
import pytest
import pandas as pd
from utils.team_generation import generate_teams
import json
import yaml


class TestTeamGeneration(unittest.TestCase):

    def setUp(self):
        # Load the players DataFrame from a JSON file
        with open("data/players.json", "r") as f:
            data = json.load(f)
        self.players_df = pd.DataFrame(data)

        with open("config.yml", "r") as f:
            self.config = yaml.safe_load(f)

    def test_generate_teams_basic(self):
        players_df = self.players_df
        players_df = players_df[players_df['Name'].isin([
            "Adan", "Andrey", "Artavia", "Bryan", "Charlie",
            "Dan", "Rolo", "Undrik", "Teclas", "Mauro"
        ])]
        team_size = 5
        restricted_pairs = []
        teams = generate_teams(players_df, team_size, restricted_pairs,
                               player_stats=self.config['player_stats'], n_solutions=4,)
        assert isinstance(teams, list)
        assert all(isinstance(team, list) for team in teams)
        assert all(len(team) == team_size for team in teams)

    def test_generate_teams_with_restricted_pairs(self):
        team_size = 5
        # Assume player names are in a 'Name' column
        names = self.players_df['Name'].tolist()
        if len(names) >= 2:
            restricted_pairs = [(names[0], names[1])]
            teams = generate_teams(
                self.players_df, team_size, restricted_pairs)
            for team in teams:
                assert not (names[0] in team and names[1] in team)

    def test_generate_teams_with_gk(self):
        team_size = 5
        restricted_pairs = []
        teams = generate_teams(self.players_df, team_size, restricted_pairs)
        # Each team should have at least one GK
        for team in teams:
            gks = self.players_df[self.players_df['Name'].isin(
                team) & ~self.players_df['GK'].isna()]
            assert len(gks) >= 1


if __name__ == "__main__":
    pytest.main([__file__])
