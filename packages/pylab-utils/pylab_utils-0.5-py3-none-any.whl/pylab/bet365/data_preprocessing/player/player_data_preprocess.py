import os
import pandas as pd

source_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../csv/player_data.csv')
output_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../csv/player_data_processed.csv')

# read from csv, normalize data using min max scaler, add ranking and tier information, store as a new file
attack_metrics = ['xA', 'npxG', 'dribbleSuccess']
threat_metrics = ['keyPass', 'foulDrawn', 'progressivePass', 'shotCreatingAction']
defense_metrics = ['tklInt', 'pressSuccess']

col_labels = attack_metrics + threat_metrics + defense_metrics

exclude_cols = ['createdAt', 'updatedAt', 'playerId', 'season']

df = pd.read_csv(source_file, index_col='seq_id', usecols=lambda x: x not in exclude_cols)

# remove goal keeper from data set
goal_keeper_index = df[(df['matchPlayed'] > 30) & (df['dribbleSuccess'] < 5) & (df['foul'] < 5)].index

df = df.drop(index=goal_keeper_index)


max_score = df.shape[0]

print('pre_process data for {} playres'.format(max_score))

ranking_score_bonus_tbl = {
    (1, 3): int(max_score * 0.95),
    (4, 10): int(max_score * 0.90),
    (11, 20): int(max_score * 0.80),
    (21, 50): int(max_score * 0.60),
    (51, 100): int(max_score * 0.40),
    (101, 200): int(max_score * 0.10),
    (201, max_score + 1): 0
}

threat_metrics_bonus_coefficient = 0.5  # threat metrics' ranking score weight is 0.5


def get_rank_score(rank: int, metric_name: str, max_s=max_score) -> int:
    base_core = max_s - rank
    bonus_score = 0

    for tier in ranking_score_bonus_tbl.keys():
        if tier[0] <= rank <= tier[1]:
            if metric_name in threat_metrics:
                bonus_score = ranking_score_bonus_tbl[tier] * threat_metrics_bonus_coefficient
            else:
                bonus_score = ranking_score_bonus_tbl[tier]
            break

    return base_core + bonus_score


df['total_rank_score'] = 0
df['attack_rank_score'] = 0
df['defense_rank_score'] = 0

# calculate rank score based on performance
for col in col_labels:
    df[col] = df[col] / (df['minutePlayed'] / 90).round()
    df[col + '_rank'] = df[col].rank(method='min', na_option='bottom', ascending=False)
    df[col + '_tier'] = df[col].rank(method='min', na_option='bottom', ascending=False, pct=True)

    # get rank score based on rank on each metrics
    df['total_rank_score'] = df['total_rank_score'] + df[col + '_rank'].map(lambda x: get_rank_score(x, col))

    if col in attack_metrics:
        df['attack_rank_score'] = df['attack_rank_score'] + df[col + '_rank'].map(
            lambda x: get_rank_score(x, col))
    if col in defense_metrics:
        df['defense_rank_score'] = df['defense_rank_score'] + df[col + '_rank'].map(
            lambda x: get_rank_score(x, col))

# adjust rank score based on minute played
for index, row in df.iterrows():
    # penalty for small amount of time played
    if row['minutePlayed'] < 1000:
        df.loc[index, 'total_rank_score'] = row['total_rank_score'] * 0.8
        df.loc[index, 'attack_rank_score'] = row['attack_rank_score'] * 0.8
        df.loc[index, 'defense_rank_score'] = row['defense_rank_score'] * 0.8

    if 1000 < row['minutePlayed'] < 1300:
        df.loc[index, 'total_rank_score'] = row['total_rank_score'] * 0.85
        df.loc[index, 'attack_rank_score'] = row['attack_rank_score'] * 0.85
        df.loc[index, 'defense_rank_score'] = row['defense_rank_score'] * 0.85

    # bonus for over 30 matches played
    if row['minutePlayed'] > 2800:
        df.loc[index, 'total_rank_score'] = row['total_rank_score'] * 1.1
        df.loc[index, 'attack_rank_score'] = row['attack_rank_score'] * 1.1
        df.loc[index, 'defense_rank_score'] = row['defense_rank_score'] * 1.1

    # score penalty for ligue 1
    if row['league'] == 'Ligue 1':
        df.loc[index, 'total_rank_score'] = row['total_rank_score'] * 0.9
        df.loc[index, 'attack_rank_score'] = row['attack_rank_score'] * 0.9
        df.loc[index, 'defense_rank_score'] = row['defense_rank_score'] * 0.9

df['total_rank'] = df['total_rank_score'].rank(method='min', na_option='bottom', ascending=False).astype(int)
df['attack_rank'] = df['attack_rank_score'].rank(method='min', na_option='bottom', ascending=False).astype(int)
df['defense_rank'] = df['defense_rank_score'].rank(method='min', na_option='bottom', ascending=False).astype(int)

df = df.sort_values(by=['total_rank'])
df = df.reset_index(drop=True)

df.to_csv(output_file, index_label='seq_id')
# print(df[['name', 'minutePlayed', 'total_rank', 'attack_rank']].head(30))
