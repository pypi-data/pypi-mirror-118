import os
import pandas as pd
from sqlalchemy import create_engine

output_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../csv/match_season_2020-2021.csv')

# read from db
engine = create_engine('mysql+pymysql://root:root@localhost:3306/soccer')

sql = "SELECT * FROM stats_bomb_matches where matchDate > '2020-08-10' and matchDate < '2021-06-30' order by matchDate"

df = pd.read_sql(sql, engine)

print(f"unload {df.shape[0]} matches to csv: {output_file}")

df.to_csv(output_file, index_label='seq_id')
