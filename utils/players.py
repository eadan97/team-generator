import pandas as pd


def get_player_names(players: list[dict]) -> list[str]:
    return [player["Name"] for player in players]


def get_players_by_names(players: list[dict], names: list[str]) -> list[dict]:
    name_set = set(names)
    return [player for player in players if player["Name"] in name_set]


def get_average_stats_df(players: list[dict], stats_config: dict) -> pd.DataFrame:
    if not players:
        return pd.DataFrame()

    df = pd.DataFrame.from_records(
        [
            {
                **{
                    stat: sum(
                        [
                            player["Stats"]["Outfield"][stat][substat]
                            * stats_config[stat][substat]
                            // 100
                            for substat in stats_config[stat]
                        ]
                    )
                    for stat in stats_config
                },
                "Name": player["Name"],
            }
            for player in players
        ]
    )

    return df
