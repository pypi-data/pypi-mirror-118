from typing import List

import plotly.graph_objects as go
from plotly.subplots import make_subplots

from sklearn import preprocessing

from pylab.bet365.data_preprocessing.data_loader import get_player_dataframe

# read from csv
df = get_player_dataframe()

min_max_scaler = preprocessing.MinMaxScaler()

metrics = ['xA', 'npxG', 'dribbleSuccess', 'progressivePass', 'tklInt', 'pressure']

data_set = df.loc[:, metrics]

normalized_stats = min_max_scaler.fit_transform(data_set)


def _get_y_coordinates(fig, idx):
    if idx == 1:
        idx = ""
    else:
        idx = str(idx)

    y_range = fig.layout['polar' + idx].domain.y
    return round((y_range[0] + y_range[1]) / 2, 2)


def _description(player):
    return """
        <b>{name}, attack_rank: {rank}</b><br>
        <i>npxG: </i> {npxG}, <i>xA: </i> {xA} <br>
        <i>pass: </i> {pPass}, <i>SCA: </i> {sca} <br>
        <i>dribble: </i> {dribble}<br>
    """.format(name=player['name'],
               rank=int(player['attack_rank']),
               npxG=round(player['npxG'], 2),
               xA=round(player['xA'], 2),
               pPass=round(player['progressivePass'], 2),
               sca=round(player['shotCreatingAction'], 2),
               dribble=round(player['dribbleSuccess'], 2))


def plot_player(player_ids: List[str]) -> None:
    players_to_show = len(player_ids)

    assert (players_to_show > 0)

    fig = make_subplots(rows=players_to_show, cols=1, start_cell="top-left",
                        specs=[[{'type': 'polar'}]] * players_to_show)

    for i in range(players_to_show):
        row = i + 1

        player_row = df.loc[player_ids[i], :]

        fig.add_trace(go.Scatterpolar(
            r=normalized_stats[player_ids[i]],
            theta=metrics,
            fill='toself',
            showlegend=True,
            name=player_row['name']
        ), row=row, col=1)

        fig.add_annotation(x=1 - 0.1 * players_to_show, y=_get_y_coordinates(fig, i + 1),
                           xref="paper", yref="paper",
                           text=_description(player_row),
                           showarrow=False)

    fig.update_polars(radialaxis=dict(range=[0, 1]))

    fig.show()


def plot_player_comparison(player1: int, player2: int) -> None:
    player1_df = df.loc[player1, :]
    player2_df = df.loc[player2, :]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=normalized_stats[player1],
        theta=metrics,
        fill='toself',
        name=player1_df['name'],
    ))
    fig.add_trace(go.Scatterpolar(
        r=normalized_stats[player2],
        theta=metrics,
        fill='toself',
        name=player2_df['name'],
    ))

    fig.add_annotation(x=0.95, y=0.2,
                       xref="paper", yref="paper",
                       text=_description(player1_df),
                       showarrow=False)

    fig.add_annotation(x=0.95, y=0.8,
                       xref="paper", yref="paper",
                       text=_description(player2_df),
                       showarrow=False)

    fig.update_polars(radialaxis=dict(range=[0, 1]))

    fig.show()
