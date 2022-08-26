import pandas as pd
import plotly.express as px
import statistics

class Visualisation():
    '''spotify chart visualization (line and bar)'''
    def __init__(self, csv_file = 'chart.csv'):
        self.csv_file = csv_file
        
    def _open_csv(self):     
        self.df = pd.read_csv(self.csv_file)
        
    def _create_line_chart(self):
        self._open_csv()
        self.fig = px.line(self.df, x="date", y="number",
                           line_group="musician", color = "musician")
        self.fig.update_yaxes(autorange="reversed")
        self.fig.update_layout(margin=dict(l=15, r=15, t=15, b=15))
        
    def _create_the_set_of_musician(self):
        '''need for bar charts'''
        self._open_csv()
        self.musicians = set(list()) 
        for m in self.df['musician']:
            self.musicians.add(m)
            
    def _create_an_empty_dictionary(self):
        '''dictionary(musician / average chart position) need for bar chart'''        
        self.dict_for_bar_charts = {}
        self.dict_for_bar_charts['musician'] = []
        self.dict_for_bar_charts['average chart position'] = []
        
    def _extract_need_data_from_csv_for_bar(self):
        '''average chart positions'''
        self._open_csv()
        self._create_the_set_of_musician()
        self._create_an_empty_dictionary()
        for musician in self.musicians:
            self.list_of_places=[] #empty list of places on the chart    
            #iterate over the places in the chart for the musician
            self.df_list = self.df[self.df['musician'] == musician]   
            for m in self.df_list['number']: #save data from column 'number'
                self.list_of_places.append(m) 
                self.chart_average = statistics.mean(self.list_of_places)
                self.chart_average_round = round(self.chart_average, 1)
            #add data in dict_for_bar_charts
            self.dict_for_bar_charts['average chart position'].append(
                self.chart_average_round)
            self.dict_for_bar_charts['musician'].append(musician)
            
    def _create_bar_chart(self):
        self._extract_need_data_from_csv_for_bar()
        self.fig2 = px.bar(self.dict_for_bar_charts,
                           y='average chart position', x='musician')
        self.fig2.update_xaxes(categoryorder = 'total ascending') #sort
        
    def show_line_chart(self):
        self._create_line_chart()
        self.fig.show()
        
    def show_bar_chart(self):
        self._create_bar_chart()
        self.fig2.show()
        
    def write_line_chart(self):
        self._create_line_chart()
        self.fig.write_html("chart.html")
        
    def write_bar_chart(self):
        self._create_bar_chart()
        self.fig2.write_html("chart_average.html")

if __name__ == '__main__':
    vis = Visualisation()
    vis.show_line_chart()
    vis.show_bar_chart()
    vis.write_line_chart()
    vis.write_bar_chart()

    
