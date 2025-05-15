import numpy as np
from ortools.sat.python import cp_model
import pandas as pd


def generate_teams(players: pd.DataFrame, team_size, restricted_pairs, player_stats=["GK", "DEF", "MID", "FWD"], n_solutions=1):
    """
    Generates teams based on the selected players, team size, and restricted pairs.

    Args:
        players (list): List of player names.
        team_size (int): Number of players per team.
        restricted_pairs (list): List of tuples representing player pairs that should not be on the same team.

    Returns:
        list: List of generated teams.
    """
    model = cp_model.CpModel()

    n_players = len(players)
    team_vars = [model.NewBoolVar(f"team_{i}") for i in range(n_players)]

    # Convert stats columns to int (fill NaN with 0, then cast to int)
    # TODO: Should we use the mean of the stats instead of 0?
    for stats in player_stats:
        players[stats] = players[stats].fillna(0).astype(int)

    ### CONSTRAINTS ###

    # C: Team size constraint
    model.Add(sum(team_vars) == team_size)

    # C: Each team should have a GK

    # TODO: Fix this to use goalkeepers
    # # Fetch goalkeepers
    # gk_indices = players[players['GK'] > 0].index.tolist()
    # gk_vars = [team_vars[i] for i in gk_indices]
    # model.Add(sum(tv for tv in gk_vars) == 1)               # team 1 gets 1 GK
    # model.Add(sum(1 - tv for tv in gk_vars) == 1)           # team 0 gets 1 GK

    # C: restricted players not on the same team
    for p1, p2 in restricted_pairs:
        i1 = players[players["Name"] == p1].index[0]
        i2 = players[players["Name"] == p2].index[0]
        model.Add(team_vars[i1] != team_vars[i2])

    ### OBJECTIVE FUNCTION ###

    position_vars = []
    for stats in player_stats:
        pos_diff = model.NewIntVar(0, 10000, f"{stats}_diff")
        t0_skill = model.NewIntVar(0, 10000, f"team0_{stats}_skill")
        t1_skill = model.NewIntVar(0, 10000, f"team1_{stats}_skill")

        skills = players[stats].tolist()

        model.Add(t0_skill == sum(
            (1 - team_vars[i]) * skills[i] for i in range(n_players)))
        model.Add(t1_skill == sum(
            team_vars[i] * skills[i] for i in range(n_players)))
        model.AddAbsEquality(pos_diff, t0_skill - t1_skill)
        position_vars.append(pos_diff)

    model.Minimize(sum(position_vars))

    # Creates a solver and solves the model.

    solutions = []
    for _ in range(n_solutions):
        solver = cp_model.CpSolver()
        status = solver.Solve(model)

        if status != cp_model.OPTIMAL and status != cp_model.FEASIBLE:
            print("No solution found.")
            break
        assignment = [solver.Value(var) for var in team_vars]
        objective_value = solver.ObjectiveValue()
        solutions.append((objective_value, assignment))

        # Exclude this exact solution
        # Add a constraint to exclude the current solution:
        # At least one variable must differ from the current assignment
        model.AddBoolOr([
            team_vars[i].Not() if assignment[i] else team_vars[i]
            for i in range(len(team_vars))
        ])
        
        model.AddBoolOr([
            team_vars[i] if assignment[i] else team_vars[i].Not()
            for i in range(len(team_vars))
        ])
        # team0 = []
        # team1 = []
        # for i, row in players.iterrows():
        #     if solver.Value(team_vars[i]) == 0:
        #         team0.append(row["Name"])
        #     else:
        #         team1.append(row["Name"])
        # print("Team 0:", team0)
        # print("Team 1:", team1)
        # return [team0, team1]
    return solutions
