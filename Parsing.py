import csv
from time import sleep
from datetime import date, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

#create empty arrays to fill with addresses
dates=[]
url_list=[]

#base url
url = "https://charts.spotify.com/charts/view/artist-us-weekly/"

#find the number of weeks to run a cycle
start_date= date(2021, 10, 21)
end_date= date.today()
delta= end_date-start_date
delta_week = delta // 7

#complete list of dates
for i in range(delta_week.days):    
    day = start_date+timedelta(weeks=i) #add week
    day_string= day.strftime("%Y-%m-%d") #to string
    dates.append(day_string)
    
#complete list of urls
for date in dates:
    url_string = url+date
    url_list.append(url_string)

#login to spotify
driver = webdriver.Chrome()
driver.get("https://accounts.spotify.com/ru/login")
driver.find_element(By.ID,"login-username").send_keys('jim_hendrix@mail.ru')
driver.find_element(By.ID,"login-password").send_keys('231290qQ')
driver.find_element(By.ID,"login-button").click()
sleep(3)

#main page loop
data_list = [] #create the empty list to fill with lists with data and transfers to csv
for u in url_list:        
    date = u[56:] #date string to save to data
    driver.get(u)
    
    #loading data, waiting for them to appear
    news_elements = WebDriverWait(driver, timeout=10).until(
        lambda d: d.find_elements(
            By.CLASS_NAME, "TableRow__TableRowElement-sc-1kuhzdh-0.bANOpw.styled" \
            "__StyledTableRow-sc-135veyd-3.lsudt"))
    
    #extract data and write in data_list
    for e in news_elements[:10]: #top 10
        raw_data = e.text.split('\n')
        number = raw_data[0]
        musicant = raw_data[2]
        data = []
        data.append(number)
        data.append(musicant)
        data.append(date)
        data_list.append(data)
        
#create csv based on list
with open('chart.csv', 'w') as chart:    
    w = csv.writer(chart)
    w.writerow(['number', 'musician', 'date'])
    w.writerows(data_list)

