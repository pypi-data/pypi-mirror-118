import pandas as pd
from sqlalchemy import create_engine

# read from db
# engine = create_engine('mysql+pymysql://alannesta:112233aA#@annie.cwqkbt0pd6s4.us-east-1.rds.amazonaws.com:3306/soccer-dev')
engine = create_engine('mysql+pymysql://root:root@localhost:3306/soccer')

sql = "SELECT * FROM player_stats where season = '2020-2021' and npxG is not null and minutePlayed > 700;"
df = pd.read_sql(sql, engine)

print("unload {} players data to csv: ".format(df.shape[0]))

df.to_csv('../csv/player_data.csv', index_label='seq_id')
