import pandas as pd

# df = pd.read_csv('./csv/history.csv', index_col='Match')

# df['Date'] = pd.to_datetime(df['Date'])

# df.loc[df.index[0], 'Date'] = 'lol'
# df.iloc[0, df.columns.get_loc('Date')] = 'lol'

# print(df)


# for index, row in df.iterrows():
# print(row[2])

# df.loc[index, 'Comments'] = 'lol'  # DO THIS if need to update dataframe

# print(df['Comments'])

# for tup in df.itertuples():
#     print(isinstance(tup, tuple)) # True

# print(pd.to_numeric('2,330'))
# print(pd.to_numeric('1,312'))