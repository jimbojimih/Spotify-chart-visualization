import statistics

import pandas as pd
import plotly.express as px


class CsvReader():
    def __init__(self, csv_file_name):
        self.csv_file_name = csv_file_name

    def open_csv(self):
        self.csv = pd.read_csv(self.csv_file_name)

    def get_csv(self):
        return self.csv
    

class LineVisualisation():    
    def __init__(self, csv):
        self.csv = csv
        
    def create_chart(self):
        self.fig = px.line(self.csv, x="date", y="number",
                           line_group="musician", color="musician")
        self.fig.update_yaxes(autorange="reversed")
        self.fig.update_layout(margin=dict(l=15, r=15, t=15, b=15))
        
    def show_chart(self):
        self.fig.show()

    def write_chart(self):
        self.fig.write_html("line_chart.html")
        

class BarVisualisation():
    def __init__(self, csv):
        self.csv = csv         

    def _create_the_set_of_musician(self):
        self.musicians = set(list()) 
        for musician in self.csv['musician']:
            self.musicians.add(musician)
            
    def _create_an_empty_dictionary(self):      
        self.dict_for_bar_charts = {}
        self.dict_for_bar_charts['musician'] = []
        self.dict_for_bar_charts['average chart position'] = []
        
    def _extract_data_from_csv(self):
        self._create_the_set_of_musician()
        self._create_an_empty_dictionary()
        
        for musician in self.musicians:
            self.list_of_places=[]
            
            #iterate over the places in the chart for the musician
            self.csv_filter_by_musician = self.csv[
                    self.csv['musician'] == musician]
            
            #save data from column 'number'
            for number in self.csv_filter_by_musician['number']: 
                self.list_of_places.append(number)
                
            self.chart_average = statistics.mean(self.list_of_places)
            self.chart_average_round = round(self.chart_average, 1)
                
            #add data in dict_for_bar_charts
            self.dict_for_bar_charts['average chart position'].append(
                    self.chart_average_round)
            self.dict_for_bar_charts['musician'].append(musician)
            
    def create_chart(self):
        self._extract_data_from_csv()
        self.fig = px.bar(self.dict_for_bar_charts,
                           y='average chart position', x='musician')
        self.fig.update_xaxes(categoryorder = 'total ascending') #sort   
                
    def show_chart(self):
        self.fig.show()   
        
    def write_chart(self):
        self.fig.write_html("chart_average.html")

if __name__ == '__main__':

    csv_reader = CsvReader('csv_chart.csv')
    csv_reader.open_csv()
    csv = csv_reader.get_csv()
    
    line_visualisation = LineVisualisation(csv)
    line_visualisation.create_chart()
    line_visualisation.show_chart()
    line_visualisation.write_chart()

    bar_visualisation = BarVisualisation(csv)
    bar_visualisation.create_chart()
    bar_visualisation.show_chart()
    bar_visualisation.write_chart()
