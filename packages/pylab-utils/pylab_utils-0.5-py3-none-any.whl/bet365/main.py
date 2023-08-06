import argparse

from pylab.bet365.player_stats.explore_player import player_details, top_n, compare_players
from pylab.bet365.team_stats.explore_team import find_similar_team, team_report


def run():
    parser = argparse.ArgumentParser(prog='soccer data analysis tool', description='soccer data analysis tool')

    group = parser.add_mutually_exclusive_group()

    group.add_argument('--player', nargs='+', help='show player stats')

    group.add_argument('--team', nargs='+', help='show team stats')

    parser.add_argument('--type', help='stats type, general, attack or defense', default='general')

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
