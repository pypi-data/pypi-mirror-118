# from .explore_player import compare_players, top_n, player_details
from pylab.bet365.team_stats.explore_team import find_matches

# top_n((15, 50), rank='total_rank')
#
# player_details('Pedri', player_type='general')

# compare_players('Hakan Çalhanoğlu', 'Barella', player_type='attack')


# team data
# df = get_team_dataframe()

# print(df[['team', 'avgShotsTotal_tier', 'avgShotsTotal']].head(20))

# result = find_similar_team(df.iloc[70, :])

# print(result)

print(find_matches('Lazio', 'Roma'))