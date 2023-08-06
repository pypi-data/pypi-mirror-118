import pandas as pd

from pylab.bet365.data_preprocessing.data_loader import get_team_dataframe, get_match_dataframe
from pylab.bet365.renderer import open_html_in_browser, match_hisotry_page_template, render_matches_html, \
    render_team_summary_html


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


def find_similar_team(team: str, team_style='general', loose_tier=False) -> pd.DataFrame:
    """

    :param team: name of the target team
    :param team_style: player type will decide which set of metrics to use to find similar players
    :param loose_tier: whether to loose tier requirements
    :return:
    """
    general_metrics = ['avgShotsTotal', 'avgPassesIntoPenaltyArea', 'avgThroughBalls',
                       'avgProgressivePasses', 'avgDribbles']

    core_metrics = ['avgCrosses', 'avgPressuresAtt3rd', 'avgTouchesAtt3rd']

    metrics = [metric + '_tier' for metric in (general_metrics + core_metrics)]

    target_team = find_team(team)

    print(f"Finding similar team for: {target_team['team']}, using loose criteria: {loose_tier}")
    team_df = get_team_dataframe()

    similar_team_index = []

    for index, row in team_df.iterrows():

        loose_metrics_allowed = 3
        loose_metrics_used = 0
        loose_metrics = []

        match_failure_cnt = 0
        match_failure_allowed = 1
        match_failure = []

        match_found = True
        if row['team'] == target_team['team']:
            continue

        for metric in metrics:
            if get_tier_bracket(target_team[metric], loose_tier=False) == get_tier_bracket(row[metric],
                                                                                           loose_tier=False):
                continue
            else:
                if loose_tier and loose_metrics_used < loose_metrics_allowed:
                    if get_tier_bracket(target_team[metric], loose_tier=True) == get_tier_bracket(row[metric],
                                                                                                  loose_tier=True):
                        loose_metrics_used = loose_metrics_used + 1
                        loose_metrics.append(metric)
                    else:
                        if metric not in core_metrics and match_failure_cnt < match_failure_allowed:
                            match_failure_cnt += 1
                            match_failure.append(metric)
                            continue
                        else:
                            match_found = False
                            break
                else:
                    match_found = False
                    break

        if match_found:
            similar_team_index.append(index)

    if similar_team_index:
        if len(similar_team_index) > 8:
            # if too many, only show 8 similar players
            print('{} similar teams found, only show 8 teams'.format(len(similar_team_index)))
            similar_team_index = similar_team_index[:8]

        return team_df.loc[similar_team_index, :]
    else:
        # aleady using loose tier, still cannot find players, return empty dataframe
        if loose_tier:
            return pd.DataFrame()

        # try finding similar players using loose tier
        return find_similar_team(team, team_style, loose_tier=True)


def find_matches(team1: str, team2: str) -> pd.DataFrame:
    """
    find matches between certain teams
    :param team1:
    :param team2:
    :return:
    """
    all_matches = get_match_dataframe()
    print(f'find similar teams for {team2}...')

    similar_teams = find_similar_team(team2)

    if not similar_teams.empty:
        opponents = [team2] + similar_teams['team'].tolist()
    else:
        opponents = [team2]

    matches_found = all_matches.drop(all_matches.index)

    print(f'complie match report using team1: {team1} vs opponents: {opponents}')

    for oteam in opponents:
        matches = all_matches[((all_matches['homeTeam'] == team1) & (all_matches['awayTeam'] == oteam)) | (
                (all_matches['homeTeam'] == oteam) & (all_matches['awayTeam'] == team1))]

        if not matches.empty:
            matches_found = matches_found.append(matches, ignore_index=True)

    matches_found = matches_found.sort_values(by='matchDate', inplace=False)
    return matches_found


def find_team(name: str) -> pd.Series:
    """
    find team by team name
    :param name: team name The name provided should be able to identify a single team
    :return: pandas series
    """

    df = get_team_dataframe()
    matches = df['team'].str.contains(name, regex=False, case=False)
    assert df[matches].shape[0] == 1  # only 1 team should be matched

    return df.iloc[df[matches].head(1).index[0], :]


def team_report(team1: str, team2: str = None) -> None:
    if not team2:
        raise Exception('Team2 is not provided')

    team1_series = find_team(team1)
    team1_similar = find_similar_team(team1)
    team1_matches = find_matches(team1, team2)

    team2_series = find_team(team2)
    team2_similar = find_similar_team(team2)
    team2_matches = find_matches(team2, team1)

    if not team1_similar.empty:
        team1_sum_html = render_team_summary_html(team1_series, team1_similar['team'].tolist())
    else:
        team1_sum_html = render_team_summary_html(team1_series, [])

    team1_matches_html = render_matches_html(team1_matches)

    if not team2_similar.empty:
        team2_sum_html = render_team_summary_html(team2_series, team2_similar['team'].tolist())
    else:
        team2_sum_html = render_team_summary_html(team2_series, [])

    team2_matches_html = render_matches_html(team2_matches)

    open_html_in_browser(match_hisotry_page_template(), team1_sum_html, team1_matches_html, team2_sum_html,
                         team2_matches_html)
