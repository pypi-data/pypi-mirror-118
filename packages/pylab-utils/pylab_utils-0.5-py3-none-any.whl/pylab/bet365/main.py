import argparse

from pylab.bet365.player_stats.explore_player import player_details, top_n, compare_players
from pylab.bet365.team_stats.explore_team import find_similar_team, team_report
from pylab.bet365.data_preprocessing.bet365.data_enricher import Processor
from pylab.bet365.data_preprocessing.bet365.unload_bet_history import download_history, get_new_history


def run():
    parser = argparse.ArgumentParser(prog='soccer data analysis tool', description='soccer data analysis tool')

    # data analysis command group
    group = parser.add_mutually_exclusive_group()

    group.add_argument('--player', nargs='+', help='show player stats')

    group.add_argument('--team', nargs='+', help='show team stats')

    parser.add_argument('--type', help='stats type, general, attack or defense', default='general')

    # bet365 history command group
    group_b = parser.add_mutually_exclusive_group()

    group_b.add_argument('--download_history', action='store_true',
                         help='download history as csv from bet365 google sheet')

    group_b.add_argument('--enrich_history', action='store_true', help='enrich history data, create new csv')

    group_b.add_argument('--report', action='store_true', help='generate bet history report')

    group_b.add_argument('--suggest_update_history', action='store_true',
                         help='generate csv with update suggestions for manual edit')

    group_b.add_argument('--get_new_history', action='store_true',
                         help='pull bet history data from bet365 website. Need to manually authenticate to bet365')

    args = parser.parse_args()

    if args.player:
        print(args.player)
        if len(args.player) == 1:
            player_details(args.player[0], player_type=args.type)
        else:
            assert len(args.player) == 2
            compare_players(args.player[0], args.player[1], player_type=args.type)

    if args.team:
        print(args.team)
        if len(args.team) == 1:
            print(find_similar_team(args.team[0], team_style=args.type))
        else:
            assert len(args.team) == 2
            team_report(args.team[0], args.team[1])

    if args.get_new_history:
        print('pull bet history data from bet365 website')
        get_new_history()

    if args.download_history:
        print('Download bet365 history from google sheet')
        download_history()

    if args.enrich_history:
        print('enrich history')
        Processor.enrich()

    if args.suggest_update_history:
        print('generate history update suggestions')
        Processor.suggest_update_history()

    if args.report:
        print('generate report')
        Processor.report()

# COMMENT this when building pypi package
# run()
