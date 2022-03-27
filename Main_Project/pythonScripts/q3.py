import pandas as pd

df = pd.read_csv('broadway.csv')

df_cpi = pd.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2020/2020-04-28/cpi.csv')

df['week_ending'] = pd.to_datetime(df["week_ending"],format="%d/%m/%Y")
df_cpi['year_month'] = pd.to_datetime(df_cpi["year_month"])

#https://stackoverflow.com/questions/51992291/how-to-join-2-dataframe-on-year-and-month-in-pandas
df = pd.merge(df.assign(grouper=df['week_ending'].dt.to_period('M')),
               df_cpi.assign(grouper=df_cpi['year_month'].dt.to_period('M')),
               how='left', on='grouper')

df= df[['week_ending', 'show', 'theatre', 'weekly_gross', 'avg_ticket_price','pct_capacity','cpi']]

df['avg_ticket_price_cpi'] = (266.795 / df['cpi']) * df['avg_ticket_price']

df2 = df
df2['num_shows'] = df2.groupby('week_ending')['show'].transform('count')
df2 = df2[['week_ending', 'avg_ticket_price_cpi', 'pct_capacity', 'num_shows']]
df2 = df2.groupby('week_ending').mean()
df2['pct_capacity'] = (df2['pct_capacity'] * 100)
df2 = df2.reset_index()

df_transformed = pd.DataFrame()
types=['avg_ticket_price_cpi', 'pct_capacity', 'num_shows']
for i, row in df2.iterrows():
    for t in types: 
        df_transformed = df_transformed.append({'date': row['week_ending'],
                                'type': t,
                                'data': row[t]},ignore_index=True)
df_transformed.to_csv('transfomed_data.csv')