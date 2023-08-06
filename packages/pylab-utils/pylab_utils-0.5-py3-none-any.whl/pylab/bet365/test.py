from pylab.bet365.team_stats.explore_team import find_similar_team

from pylab.bet365.data_preprocessing.player.data_loader import get_team_dataframe




df = get_team_dataframe()

total = df.shape[0]
found = 0
not_found = 0

similar_count = 0

# print(df[['team', 'avgShotsTotal_tier', 'avgShotsTotal']].head(20))

for i in range(total):
    result = find_similar_team(df.iloc[i, :])
    if result.empty:
        not_found += 1
    else:
        found += 1
        similar_count += result.shape[0]

print(f'Teams with similar teams found: {found}')
print(f'Teams without similar teams found: {not_found}')
print(f'Avg similar teams found per team: {similar_count/found}')