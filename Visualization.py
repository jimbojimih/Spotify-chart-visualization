import pandas as pd
import plotly.express as px
import statistics

#create the line chart based on csv
df = pd.read_csv('chart.csv')
fig = px.line(df, x="date", y="number", line_group="musician",
              color = "musician")
fig.update_yaxes(autorange="reversed")
fig.update_layout(margin=dict(l=15, r=15, t=15, b=15))
fig.show()
fig.write_html("chart.html")


#create the bar charts of average values of places in the chart

#create the set of musicians
musicians = set(list()) 
for m in df['musician']:
    musicians.add(m)
    
#create an empty dictionary (musician / average chart position)
dict_for_bar_charts = {}
dict_for_bar_charts['musician'] = []
dict_for_bar_charts['average chart position'] = []

#extract need data from csv
for musician in musicians:
    list_of_places=[] #empty list of places on the chart
    
    #iterate over the places in the chart
    df_list = df[df['musician'] == musician] #strings of the musician    
    for m in df_list['number']: #save data from column 'number'
        list_of_places.append(m) 
        chart_average = statistics.mean(list_of_places)
        chart_average_round = round(chart_average, 1)
    #add data in dict_for_bar_charts
    dict_for_bar_charts['average chart position'].append(chart_average_round)
    dict_for_bar_charts['musician'].append(musician)
    

fig2 = px.bar(dict_for_bar_charts, y='average chart position', x='musician')
fig2.update_xaxes(categoryorder = 'total ascending') #sort
fig2.show()
fig2.write_html("chart_average.html")
