import csv
from time import sleep
from datetime import date, timedelta

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait


class UrlLisCreator():    
    def __init__(self, url):
        self. url = url
        
        self.dates_list=[]
        self.url_list=[]
        
    def _find_number_of_weeks(self):        
        self.start_date= date(2021, 10, 21)
        self.end_date= date.today()
        self.delta= self.end_date-self.start_date
        self.delta_week = self.delta // 7
        
    def _create_list_of_dates(self):        
        self._find_number_of_weeks()
        
        for i in range(self.delta_week.days):    
            self.day = self.start_date+timedelta(weeks=i) #add week
            self.day_string= self.day.strftime("%Y-%m-%d") 
            self.dates_list.append(self.day_string)
            
    def create_list_of_urls(self):        
        self._create_list_of_dates()
        
        for date in self.dates_list:
            self.url_string = self.url+date
            self.url_list.append(self.url_string)
        
    def get_list_of_urls(self):        
        return self.url_list
        
        
class Autorization():    
    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.driver = webdriver.Chrome()
        
    def log_in(self):        
        self.driver.get("https://accounts.spotify.com/ru/login")
        self.driver.find_element(
                By.ID,"login-username").send_keys(self.login)
        self.driver.find_element(
                By.ID,"login-password").send_keys(self.password)
        self.driver.find_element(
                By.ID,"login-button").click()
        sleep(3)
        
    def get_driver(self):        
        return self.driver

    
class DataExtractor():
    def __init__(self, driver, list_of_urls):
        self.driver = driver
        self.list_of_urls = list_of_urls

        self.data_list = []

    def extract_data_from_all_page(self):        
        for url in self.list_of_urls:        
            self.date = url[56:]  #date string to save to data_list
            self.driver.get(url)
            
            #loading data, waiting for them to appear
            search_element = ("TableRow__TableRowElement-sc-1kuhzdh-0.bANOpw."
                             "styled__StyledTableRow-sc-135veyd-3.lsudt")
            self.news_elements = WebDriverWait(self.driver, timeout=50).until(
                    lambda d: d.find_elements(By.CLASS_NAME, search_element))
            
            self._extract_data_from_one_page()
           
    def _extract_data_from_one_page(self):        
        '''extract data from one page'''
        
        for element in self.news_elements[:10]: #top 10
            self.raw_data = element.text.split('\n')
            self.number = self.raw_data[0]
            self.musicant = self.raw_data[2]
            
            self.data_from_one_page = []
            self.data_from_one_page.append(self.number)
            self.data_from_one_page.append(self.musicant)
            self.data_from_one_page.append(self.date)
            
            self.data_list.append(self.data_from_one_page)

    def get_data_list(self):
        return self.data_list
            
            
class CsvCreator():
    def __init__(self, name_csv_file, data_list):
        self.name_csv_file = name_csv_file
        self.data_list = data_list
        
    def create_csv(self):  
        with open(self.name_csv_file, 'w', encoding="utf-8") as chart:    
            self.w = csv.writer(chart)
            self.w.writerow(['number', 'musician', 'date'])
            self.w.writerows(self.data_list)
            
if __name__ == '__main__':
    
    url_list_creator = UrlLisCreator(
            "https://charts.spotify.com/charts/view/artist-us-weekly/")
    url_list_creator.create_list_of_urls()    
    list_of_urls = url_list_creator.get_list_of_urls()
    
    autorization = Autorization('your login', 'your password')
    autorization.log_in()
    driver = autorization.get_driver()
    
    data_extractor = DataExtractor(driver, list_of_urls)
    data_extractor.extract_data_from_all_page()
    data_list = data_extractor.get_data_list()
    
    csv_creator = CsvCreator('csv_chart.csv', data_list)
    csv_creator.create_csv()

