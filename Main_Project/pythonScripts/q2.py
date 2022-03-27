import pandas as pd

df = pd.read_csv('broadway.csv')

df_cpi = pd.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2020/2020-04-28/cpi.csv')

df['week_ending'] = pd.to_datetime(df["week_ending"],format="%d/%m/%Y")
df_cpi['year_month'] = pd.to_datetime(df_cpi["year_month"])

#https://stackoverflow.com/questions/51992291/how-to-join-2-dataframe-on-year-and-month-in-pandas
df = pd.merge(df.assign(grouper=df['week_ending'].dt.to_period('M')),
               df_cpi.assign(grouper=df_cpi['year_month'].dt.to_period('M')),
               how='left', on='grouper')

df['avg_ticket_price_cpi'] = (266.795 / df['cpi']) * df['avg_ticket_price']
df['weekly_gross_cpi'] = (266.795 / df['cpi']) * df['weekly_gross']

df= df[['week_ending', 'show', 'theatre', 'weekly_gross', 'avg_ticket_price','pct_capacity','avg_ticket_price_cpi','weekly_gross_cpi','cpi','performances']]

#df['week_ending'] = pd.to_datetime(df['week_ending'], format="%d/%m/%Y")

df = df.sort_values(['show', 'theatre', 'week_ending'])

df['days_diff'] = df.groupby(['show', 'theatre'])['week_ending'].diff().dt.days.fillna(0)
df['days_diff'] = df['days_diff'] > 28
df['key'] = df.groupby(['show', 'theatre'])['days_diff'].cumsum()
df_final = df.groupby(['show', 'theatre', 'key']).mean().reset_index().drop(columns=['key'])

df_final.to_csv('broadway_grouped_cpi.csv')