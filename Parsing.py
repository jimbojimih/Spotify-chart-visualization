import csv
from time import sleep
from datetime import date, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

class Parsing():
    def __init__(self, login, password, csv = 'chart.csv', driver = webdriver.Chrome(), 
                 url = "https://charts.spotify.com/charts/view/artist-us-weekly/"):
        self.login = login
        self.password = password
        self.url = url
        self.csv = csv
        self.driver = driver
        
    def _find_number_of_weeks(self):
        '''need for _create_list_of_dates'''
        self.start_date= date(2021, 10, 21)
        self.end_date= date.today()
        self.delta= self.end_date-self.start_date
        self.delta_week = self.delta // 7
        
    def _create_list_of_dates(self):
        '''need for _create_list_of_urls'''
        self._find_number_of_weeks()
        self.dates=[]
        for i in range(self.delta_week.days):    
            self.day = self.start_date+timedelta(weeks=i) #add week
            self.day_string= self.day.strftime("%Y-%m-%d") #to string
            self.dates.append(self.day_string)
            
    def _create_list_of_urls(self):
        '''create list of urls for parsing'''
        self._create_list_of_dates()
        self.url_list=[] #create empty arrays to fill with urls
        for date in self.dates:
            self.url_string = self.url+date
            self.url_list.append(self.url_string)
            
    def _login_to_spotify(self):
        '''need for parsing'''
        #driver = webdriver.Chrome()
        self.driver.get("https://accounts.spotify.com/ru/login")
        self.driver.find_element(By.ID,"login-username").send_keys(self.login)
        self.driver.find_element(By.ID,"login-password").send_keys(self.password)
        self.driver.find_element(By.ID,"login-button").click()
        sleep(3)

    def _main_loop(self):
        '''main page loop'''
        self._create_list_of_urls()
        self._login_to_spotify()
        self.data_list = [] #create the empty list to fill with lists with data and transfers to csv
        for u in self.url_list:        
            self.date = u[56:] #date string to save to data
            self.driver.get(u)    
            #loading data, waiting for them to appear
            self.news_elements = WebDriverWait(self.driver, timeout=50).until(
                lambda d: d.find_elements(
                    By.CLASS_NAME, "TableRow__TableRowElement-sc-1kuhzdh-0.bANOpw.styled" \
                    "__StyledTableRow-sc-135veyd-3.lsudt"))
            self._extract_data()
            
    def _extract_data(self):
        '''extract data from one page'''
        for e in self.news_elements[:10]: #top 10
            self.raw_data = e.text.split('\n')
            self.number = self.raw_data[0]
            self.musicant = self.raw_data[2]
            self.data = []
            self.data.append(self.number)
            self.data.append(self.musicant)
            self.data.append(self.date)
            self.data_list.append(self.data)

    def create_csv(self):        
        '''create csv based on list'''
        self._main_loop()
        with open(self.csv, 'w', encoding="utf-8") as chart:    
            self.w = csv.writer(chart)
            self.w.writerow(['number', 'musician', 'date'])
            self.w.writerows(self.data_list)

if __name__ == '__main__':
    #specify your username and password when creating an instance
    pars = Parsing(login = '', password = '')
    pars.create_csv()
  
