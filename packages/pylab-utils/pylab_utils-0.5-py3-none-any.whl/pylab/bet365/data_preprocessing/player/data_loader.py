import os
from functools import lru_cache

import pandas as pd


@lru_cache(maxsize=1)
def get_player_dataframe() -> pd.DataFrame:
    csv_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../csv/player_data_processed.csv')

    df = pd.read_csv(csv_file, index_col='seq_id')

    return df


@lru_cache(maxsize=1)
def get_team_dataframe() -> pd.DataFrame:
    csv_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../csv/team_stats_processed.csv')

    df = pd.read_csv(csv_file, index_col='team_id')

    return df


@lru_cache(maxsize=1)
def get_match_dataframe() -> pd.DataFrame:
    csv_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../csv/match_season_2020-2021.csv')

    df = pd.read_csv(csv_file, index_col='seq_id')

    df['matchDate'] = pd.to_datetime(df['matchDate']).dt.date

    return df
