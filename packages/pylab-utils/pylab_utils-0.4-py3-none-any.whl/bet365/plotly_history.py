import pandas as pd
import plotly.express as px
import numpy as np

import plotly.graph_objects as go

df = pd.read_csv('./csv/bet365_history.csv')

df['Date'] = pd.to_datetime(df['Date'])


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

df = df.reset_index()

df = df.loc[(df['Gain'] > 45) | (df['Gain'] < -45)]
# df = df.loc[df['Bet Type'].str.lower() == 'corner']


def format_text(text, formatted_text='', padding=False):
    """
    add html break lines to text that is too long
    :param text: comment text
    :return: text
    """
    text = text.replace('\n', '')
    break_len = 30
    if padding:
        text_padding = 15 * ' '
    else:
        text_padding = ''

    if len(text) > break_len:
        next_text = text[break_len:]
        formatted_text = formatted_text + text_padding + text[0: break_len] + '</b><br>'
        return format_text(next_text, formatted_text, padding=True)
    else:
        if formatted_text:
            return formatted_text + '<b>' + text_padding + text + '</b>'
        else:
            return text


fig = go.Figure()

balance = 0

x = []
y = []
#
# for index, row in df.iterrows():
#     balance = row['Gain'] + balance
#     x.append(row['Date'])
#     y.append(balance)
#
# fig.add_trace(go.Scatter(x=x, y=y,
#                          mode='lines',
#                          name='lines'))

for index, row in df.iterrows():
    color = 'Red' if row['Gain'] > 0 else 'Black'
    comment = '' if pd.isnull(row['Comments']) else format_text(row['Comments'])

    fig.add_trace(
        go.Scatter(
            mode='markers',
            x=[row['Date']],
            y=[row['Balance']],
            marker=dict(
                color=color,
                size=abs(row['Gain'] / 10),
                line=dict(
                    color=color
                )
            ),
            hovertemplate="""
                <b>Match: %{text}</b><br>
                <b>Gain: %{customdata[0]}</b><br>
                <b>Date: %{x}</b><br>
                <b>%{customdata[1]}<b>
            """,
            text=[row['Match']],
            customdata=[(row['Gain'], comment)],
            showlegend=False
        )
    )

fig.show()
