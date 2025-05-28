def update_stats(players_a, players_b, goals_a, goals_b, alpha=0.2, stats_columns=None):

    if stats_columns is None:
        raise ValueError("stats_columns must be provided")

    total_goals = goals_a + goals_b

    strength_a = team_strength(players_a, stats_columns)
    strength_b = team_strength(players_b, stats_columns)

    total_strength = strength_a + strength_b

    if total_strength == 0:
        raise ValueError("Total strength cannot be zero")

    expected_a = strength_a / total_strength
    expected_b = strength_b / total_strength

    result_a = goals_a / total_goals
    result_b = goals_b / total_goals

    delta_a = result_a - expected_a
    delta_b = result_b - expected_b

    new_players_a = players_a.copy()
    new_players_b = players_b.copy()

    def update_player_stats(row, delta):
        for stat in stats_columns:
            current = row[stat]
            performance = 1 + alpha * delta
            new_value = int(round(min(99, max(1, current * performance))))
            row[stat] = new_value
        return row

    new_players_a = new_players_a.apply(lambda row: update_player_stats(row, delta_a), axis=1)
    new_players_b = new_players_b.apply(lambda row: update_player_stats(row, delta_b), axis=1)

    return new_players_a, new_players_b


def team_strength(team_df, stats_columns):
    return team_df[stats_columns].mean().sum()
