import os
import pandas as pd

# read from csv, normalize data using min max scaler, add ranking and tier information, store as a new file

attack_threat = ['avgNpxg', 'avgShotsTotal']

defense = ['avgNpxgAgainst', 'avgShotsTotalAgainst']

buildup = ['avgPassesIntoPenaltyArea', 'avgThroughBalls', 'avgCrosses', 'avgProgressivePasses',
           'avgTouchesAtt3rd', 'avgCornerKicks', 'avgDribbles']

pressing_style = ['avgTacklesAtt3rd', 'avgPressuresAtt3rd']

intensity = ['avgFouls', 'avgAerialsWon']

col_labels = attack_threat + defense + buildup + intensity + pressing_style

exclude_cols = ['createdAt', 'updatedAt', 'id', 'season', 'avgFoulsAgainst', 'avgAerialsWonAgainst',
                'avgAerialsLostAgainst']

source_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../csv/team_season2020-2021_stats.csv')
output_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../csv/team_stats_processed.csv')

df = pd.read_csv(source_file, index_col='team_id', usecols=lambda x: x not in exclude_cols)

max_score = df.shape[0]  # 78 teams from 4 leagues

print('pre_process data for {} teams'.format(max_score))

# ranking_score_bonus_tbl = {
#     (1, 3): int(max_score * 0.95),
#     (4, 10): int(max_score * 0.90),
#     (11, 20): int(max_score * 0.80),
#     (21, 40): int(max_score * 0.60),
#     (40, max_score + 1): int(max_score * 0.40),
# }
#
#
# def get_rank_score(rank: int, metric_name: str, max_s=max_score) -> int:
#     base_core = max_s - rank
#     bonus_score = 0
#
#     for tier in ranking_score_bonus_tbl.keys():
#         if tier[0] <= rank <= tier[1]:
#             bonus_score = ranking_score_bonus_tbl[tier]
#             break
#
#     return base_core + bonus_score
#
#
# df['total_rank_score'] = 0
# df['attack_rank_score'] = 0
# df['defense_rank_score'] = 0

# calculate rank score based on performance
for col in col_labels:
    df[col + '_rank'] = df[col].rank(method='min', na_option='bottom', ascending=False)
    df[col + '_tier'] = df[col].rank(method='min', na_option='bottom', ascending=False, pct=True)

# adjust rank score based on minute played
# for index, row in df.iterrows():
#     # penalty for small amount of time played
#     if row['minutePlayed'] < 1000:
#         df.loc[index, 'total_rank_score'] = row['total_rank_score'] * 0.8
#         df.loc[index, 'attack_rank_score'] = row['attack_rank_score'] * 0.8
#         df.loc[index, 'defense_rank_score'] = row['defense_rank_score'] * 0.8
#
#     if 1000 < row['minutePlayed'] < 1300:
#         df.loc[index, 'total_rank_score'] = row['total_rank_score'] * 0.85
#         df.loc[index, 'attack_rank_score'] = row['attack_rank_score'] * 0.85
#         df.loc[index, 'defense_rank_score'] = row['defense_rank_score'] * 0.85
#
#     # bonus for over 30 matches played
#     if row['minutePlayed'] > 2800:
#         df.loc[index, 'total_rank_score'] = row['total_rank_score'] * 1.1
#         df.loc[index, 'attack_rank_score'] = row['attack_rank_score'] * 1.1
#         df.loc[index, 'defense_rank_score'] = row['defense_rank_score'] * 1.1
#
#     # score penalty for ligue 1
#     if row['league'] == 'Ligue 1':
#         df.loc[index, 'total_rank_score'] = row['total_rank_score'] * 0.9
#         df.loc[index, 'attack_rank_score'] = row['attack_rank_score'] * 0.9
#         df.loc[index, 'defense_rank_score'] = row['defense_rank_score'] * 0.9

df.to_csv(output_file, index_label='team_id')

print(df[buildup].head(30))
