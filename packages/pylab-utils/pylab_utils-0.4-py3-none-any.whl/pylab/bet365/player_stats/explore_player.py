import pandas as pd
from .plot_player import plot_player, plot_player_comparison
from pylab.bet365.renderer import open_html_in_browser, player_rank_page_template, player_summary_page_template, \
    render_player_summary_html, render_player_summary_table
from pylab.bet365.data_preprocessing.data_loader import get_player_dataframe

# read from csv
df = get_player_dataframe()


def get_tier_bracket(pct_tier, loose_tier=False):
    tier_bracket = {
        (0, 0.25): '0-25%',
        (0.25, 0.5): '25%-50%',
        (0.5, 0.75): '50%-75%',
        (0.75, 1): '75%+'
    }

    if loose_tier:
        tier_bracket = {
            (0, 0.33): '0-33%',
            (0.33, 0.66): '33%-66%',
            (0.66, 1): '66%+'
        }

    for brackets in tier_bracket.keys():
        if pct_tier > brackets[0] and pct_tier <= brackets[1]:
            return tier_bracket[brackets]

    raise ValueError('invalid pct_tier: ' + str(pct_tier))


def find_similar_player(player_df: pd.Series, player_type='general', loose_tier=False) -> pd.DataFrame:
    """

    :param player_df:
    :param player_type: player type will decide which set of metrics to use to find similar players
    :param loose_tier: whether to loose tier requirements
    :return:
    """
    general_metrics = ['npxG_tier', 'xA_tier', 'pressSuccess_tier', 'shotCreatingAction_tier', 'progressivePass_tier']
    attack_metrics = ['npxG_tier', 'xA_tier', 'dribbleSuccess_tier', 'shotCreatingAction_tier', 'progressivePass_tier']
    defense_metrics = ['tklInt_tier', 'pressSuccess_tier', 'progressivePass_tier']


    if player_type == 'defense':
        metrics = defense_metrics
    elif player_type == 'attack':
        metrics = attack_metrics
    else:
        metrics = general_metrics

    print(f"Finding similar player for: {player_df['name']}, loose criteria used: {loose_tier}")
    all_players_df = get_player_dataframe()

    similar_player_index = []

    for index, row in all_players_df.iterrows():
        loose_metrics_allowed = 1  # matching metrics tier loosely using at most 2 metrics
        loose_metrics_used = 0

        match_found = False
        if row['name'] == player_df['name']:
            continue

        for metric in metrics:
            if get_tier_bracket(player_df[metric], loose_tier=False) == get_tier_bracket(row[metric],
                                                                                         loose_tier=False):
                match_found = True

            else:
                if loose_tier and loose_metrics_used < loose_metrics_allowed:
                    if get_tier_bracket(player_df[metric], loose_tier=True) == get_tier_bracket(row[metric],
                                                                                                loose_tier=True):
                        match_found = True
                        loose_metrics_used = loose_metrics_used + 1
                    else:
                        match_found = False
                        break
                else:
                    match_found = False
                    break

        if match_found:
            similar_player_index.append(index)

    if similar_player_index:
        if len(similar_player_index) > 8:
            # if too many, only show 8 similar players
            similar_player_index = similar_player_index[:8]
        return all_players_df.loc[similar_player_index, :]
    else:
        # aleady using loose tier, still cannot find players, return empty dataframe
        if loose_tier:
            print('No similar player found')
            return pd.DataFrame()

        # try finding similar players using loose tier
        return find_similar_player(player_df, player_type, loose_tier=True)


def find_player_by_rank(rank: int, player_type='general', range=5) -> pd.DataFrame:
    rank_type = 'total_rank'
    if player_type == 'attack':
        rank_type = 'attack_rank'

    if player_type == 'defense':
        rank_type = 'defense_rank'

    player_df = get_player_dataframe()
    lower_bound = rank - range if rank - range > 0 else 0
    upper_bound = rank + range if rank + range < player_df.shape[0] else player_df.shape[0]

    player_df = player_df.loc[(player_df[rank_type] > lower_bound) & (player_df[rank_type] < upper_bound)].sort_values(
        by=rank_type)

    return player_df


def find_player(name: str, team=None) -> pd.DataFrame:
    """
    find player by name and club
    :param name:
    :param team: optional
    :return:
    """
    df = get_player_dataframe()

    player = df[df['name'].str.contains(name, regex=False, case=False)]

    if team:
        player = player[player['team'].str.contains(team, regex=False, case=False)]

    return player


def top_n(range_n: tuple, rank='attack_rank'):
    open_html_in_browser(player_rank_page_template(),
                         render_player_summary_table(df.sort_values(by=[rank]).iloc[range_n[0]:range_n[1], :]))


def player_details(name, team=None, player_type='general'):
    """
    render player details in 3 parts:
    1. player summary (with percentile)
    2. player rank
    3. similar players

    name + team should identify a single player from the data sets
    :param name: name of the player
    :param team: team of the player
    :return:
    """
    players_found = find_player(name, team)
    print(players_found)
    player_ids = players_found.index.values.tolist()
    assert len(player_ids) == 1

    player = df.loc[player_ids[0], :]
    # player_html_frag = player_summary(df.loc[player_ids, :])  # force .loc to return dataframe
    # open_html_in_browser(player_rank_page_template(), player_html_frag)

    player_summary_frag = render_player_summary_html(player, player_type=player_type)

    rank_type = 'total_rank'
    if player_type == 'attack':
        rank_type = 'attack_rank'

    if player_type == 'defense':
        rank_type = 'defense_rank'

    player_rank_frag = render_player_summary_table(find_player_by_rank(player[rank_type], player_type=player_type),
                                                   player_type=player_type)

    similar_player = find_similar_player(player, player_type=player_type)
    if not similar_player.empty:
        similar_player_frag = render_player_summary_table(similar_player, player_type=player_type)
    else:
        similar_player_frag = 'No similar player found'

    open_html_in_browser(player_summary_page_template(), player_summary_frag, player_rank_frag, similar_player_frag)

    # polar chart
    plot_player(player_ids)


def compare_players(*names, player_type="general"):
    ids = []
    for name in names:
        player = find_player(name)
        player_ids = player.index.values.tolist()
        try:
            assert (len(player_ids) == 1)
        except:
            print('could not identify player by name: ', name)
            return
        ids = ids + player_ids

    html = render_player_summary_table(df.loc[ids, :], player_type)
    open_html_in_browser(player_rank_page_template(), html)

    plot_player_comparison(ids[0], ids[1])
