from collections import deque
import pandas as pd
import six
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer


def render_player_summary_html(player_series: pd.Series, player_type='general') -> str:
    assert isinstance(player_series, pd.Series)

    general_metrics = ['npxG', 'dribbleSuccess', 'progressivePass', 'shotCreatingAction', 'pressSuccess']
    attack_metrics = ['npxG', 'xA', 'dribbleSuccess', 'progressivePass', 'shotCreatingAction']
    defense_metrics = ['tklInt', 'pressSuccess', 'progressivePass']

    if player_type == 'defense':
        metrics = defense_metrics
    elif player_type == 'attack':
        metrics = attack_metrics
    else:
        metrics = general_metrics

    metrics_html = ""

    for metric in metrics:
        metrics_html = metrics_html + f"""
        <div>
        <span>{metric}: {round(player_series[metric], 3)}</span><span class="percentile">{round(
            player_series[metric + '_tier'],
            2)}</span>
        </div>
        """

    base = """
    <div id="player_summary">
        <h1>Player Summary</h1>
        <h3>{}</h3>
        <div><span>Minute Played: {}</span></div>
        <div>
            <span>Overall Rank: {}</span>
            <span>Attack Rank: {}</span>
            <span>Defense Rank: {}</span>
        </div>
        </p>
        {}
    </div>
    
    """.format(player_series['name'], player_series['minutePlayed'], player_series['total_rank'],
               player_series['attack_rank'],
               player_series['defense_rank'], metrics_html)

    return base


def render_player_summary_table(player_df: pd.DataFrame, player_type='general') -> str:
    assert isinstance(player_df, pd.DataFrame)

    general_metrics = ['npxG', 'dribbleSuccess', 'progressivePass', 'shotCreatingAction', 'pressSuccess', 'xGPlusMinus',
                       'total_rank']
    attack_metrics = ['npxG', 'xA', 'dribbleSuccess', 'progressivePass', 'shotCreatingAction', 'xGPlusMinus',
                      'attack_rank']
    defense_metrics = ['tklInt', 'pressSuccess', 'pressure', 'progressivePass', 'xGPlusMinus', 'defense_rank']

    if player_type == 'defense':
        metrics = defense_metrics
    elif player_type == 'attack':
        metrics = attack_metrics
    else:
        metrics = general_metrics

    metrics = ['name', 'minutePlayed'] + metrics

    player_df = player_df.reset_index(drop=True)

    return player_df[metrics].to_html()


def render_team_summary_html(team: pd.Series, similar_teams: list) -> str:
    return f"""
    <h1>{team['team']}</h1>
    <h3>Similar teams: </h3>
    <div class="similar_team">{', '.join(similar_teams)}</div>
    """


def render_matches_html(matches_df: pd.DataFrame) -> str:
    cols = ['matchDate', 'homeTeam', 'homeGoals', 'homeXg', 'awayXg', 'awayGoals', 'awayTeam']

    return f"""
    <h3>Matches: </h3>
    <div>{matches_df[cols].to_html()}</div>
    """


def match_hisotry_page_template():
    template = """
    <html>
    <head>
    <meta charset="utf-8"/>
    <style>
    div {{display:flex; align-items: center; flex-direction: column}}
    td {{padding: 6px; text-align: center; vertical-align: center}}

    thead th {{padding: 6px; text-align: center; vertical-align: center; font-size: 1.1rem;}}


    div.similar_team {{font-size:1.5rem}}
    </style>
    </head>
    <body style="display: flex; flex-direction: row">
        <div style="width: 50%; overflow: scroll">
            <div>{}</div>
            <div>{}</div>
        </div>
        <div style="width: 50%; overflow: scroll; justify=content:center">
            <div>{}</div>
            <div>{}</div>
        </div>
    </body>
    </html>
    """

    return template


def player_summary_page_template():
    template = """
    <html>
    <head>
    <meta charset="utf-8"/>
    <style>
    div {{display:flex; align-items: center; flex-direction: column}}
    td {{padding: 6px; text-align: center; vertical-align: center}}
    
    thead th {{padding: 6px; text-align: center; vertical-align: center; font-size: 1.1rem;}}
    
    #player_summary span {{padding: 7px}}
    
    span.percentile {{font-weight: 800; color: red;}}
    </style>
    </head>
    <body style="display: flex; flex-direction: row">
        <div style="width: 30%; overflow: scroll">
            {}
        </div>
        <div style="width: 70%; overflow: scroll; justify=content:center">
            <div id="player_rank">
            <h1>Player Rank</h1>
                {}
            </div>
            <div id="similar_players">
                <h1>Similar Players</h1>
                {}
            </div>
        </div>

    </body>
    </html>
    """

    return template


def player_rank_page_template():
    template = """
    <html>
    <head>
    <meta charset="utf-8"/>
    <style>
    td {{padding: 6px; text-align: center; vertical-align: center}}
    thead th {{padding: 6px; text-align: center; vertical-align: center; font-size: 1.1rem;}}
    </style>
    </head>
    <body style="display: flex; justify-content: center; align-items:center; flex-direction: column">
        <h1>Player Rank</h1>
        {}
    </body>
    </html>
    """

    return template


def open_html_in_browser(template, *html_fragments, using=None, new=0, autoraise=True):
    """
    Display html in a web browser without creating a temp file.

    Instantiates a trivial http server and uses the webbrowser module to
    open a URL to retrieve html from that server.

    Parameters
    ----------
    html: str
        HTML string to display
    using, new, autoraise:
        See docstrings in webbrowser.get and webbrowser.open
    """

    html_content = template.format(*html_fragments)

    # print(html_content)

    if isinstance(html_content, six.string_types):
        html_content = html_content.encode("utf8")

    class OneShotRequestHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            bufferSize = 1024 * 1024 * 5
            for i in range(0, len(html_content), bufferSize):
                self.wfile.write(html_content[i: i + bufferSize])

        def log_message(self, format, *args):
            # Silence stderr logging
            pass

    server = HTTPServer(("127.0.0.1", 0), OneShotRequestHandler)
    webbrowser.get(using).open(
        "http://127.0.0.1:%s" % server.server_port, new=new, autoraise=autoraise
    )

    server.handle_request()
