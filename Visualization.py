import pandas as pd
import plotly.express as px
import csv
import statistics

df = pd.read_csv('chart.csv')
fig = px.line(df, x="date", y="number", line_group="musicant",
              color = "musicant")
fig.update_yaxes(autorange="reversed")
fig.update_layout(margin=dict(l=15, r=15, t=15, b=15))
fig.show()
fig.write_html("chart.html")




musicants = set(list())
for m in df['musicant']:
    musicants.add(m)

dict_ = {}
dict_['musician'] = []
dict_['average value of the place in the chart'] = []
for musicant in musicants:
    list_=[]
    df_tall = df[df['musicant'] == musicant]
    for m in df_tall['number']:
        list_.append(m)
        res = statistics.mean(list_)
        res_round = round(res, 1)
    dict_['average value of the place in the chart'].append(res_round)
    dict_['musician'].append(musicant)
    

fig2 = px.bar(dict_, y='average value of the place in the chart', x='musician')
fig2.update_xaxes(categoryorder = 'total ascending')

fig2.show()
fig2.write_html("chart_average.html")
