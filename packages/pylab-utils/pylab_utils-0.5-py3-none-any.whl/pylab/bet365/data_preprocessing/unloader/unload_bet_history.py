"""
Read bet365 history from csv and save to DB
"""
import pandas as pd

from sqlalchemy import create_engine

engine = create_engine('mysql+pymysql://root:root@localhost:3306/bet365')

df = pd.read_csv('./csv/bet365_history.csv')


# convert string input to float
def to_float(input):
    if isinstance(input, int) or isinstance(input, float):
        return input

    if isinstance(input, str):
        input = input.replace('$', '').replace(',', '')

    try:
        output = pd.to_numeric(input)
    except:
        print('fail to convert input to numeric value')
        raise

    return output


# setup correct data type
df['Date'] = pd.to_datetime(df['Date'])

df['Bet'] = df['Bet'].apply(to_float)
df['Return'] = df['Return'].apply(to_float)
df['Gain'] = df['Gain'].apply(to_float)
df['Balance'] = df['Balance'].apply(to_float)

df.to_sql('history', engine, if_exists='replace', index_label='id')  # will use default index col
