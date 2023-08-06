import os

from pprint import pprint
import pandas as pd


csv_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), './output/out.csv')

df = pd.read_csv(csv_file)

# print(df.tail(10))

# pprint(df.groupby(['TEAM_1', 'TEAM_2']).groups)
df.groupby(['TEAM_1', 'TEAM_2']).apply(pprint)