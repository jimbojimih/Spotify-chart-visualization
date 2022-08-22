from bs4 import BeautifulSoup
import pandas as pd
import requests
from time import sleep
from datetime import date, timedelta
import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
#create empty arrays for data we're collecting
dates=[]
url_list=[]
final = []

#map site

url = "https://charts.spotify.com/charts/view/artist-us-weekly/"
start_date= date(2021, 10, 21)
end_date= date(2022, 8, 18)
delta= end_date-start_date
delta_week = delta // 7

for i in range(delta_week.days+1):    
    day = start_date+timedelta(weeks=i)
    day_string= day.strftime("%Y-%m-%d")
    dates.append(day_string)

for date in dates:
    c_string = url+date
    url_list.append(c_string)

#loop through urls to create array of all of our song info
options = Options()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
driver = webdriver.Chrome(options=options)
driver.get("https://accounts.spotify.com/ru/login")
driver.find_element(By.ID,"login-username").send_keys('jim_hendrix@mail.ru')
driver.find_element(By.ID,"login-password").send_keys('231290qQ')
driver.find_element(By.ID,"login-button").click()
sleep(3)

for u in url_list:
    driver.implicitly_wait(5)
    driver.get(u)
    
    news_elements = driver.find_elements(
        By.CLASS_NAME, "TableRow__TableRowElement-sc-1kuhzdh-0.bANOpw.styled__StyledTableRow-sc-135veyd-3.lsudt")
    for e in news_elements:
        print(e.text)
    print(news_elements)
    #news_elements_1 = news_elements.find_element(By.TAG_NAME, 'tr')
    #print(news_elements_1.text)
    #with open('hight_score.json', 'w') as hs:
    #        json.dump(news_elements.text, hs)
            
    sleep(2000)
    
    

#function for going through each row in each url and finding relevant song info
'''
def song_scrape(x):
    pg = x
    for tr in songs.find("tbody").findAll("tr"):
        artist= tr.find("td", {"class": "chart-table-track"}).find("span").text
        artist= artist.replace("by ","").strip()
  
        title= tr.find("td", {"class": "chart-table-track"}).find("strong").text
 
        songid= tr.find("td", {"class": "chart-table-image"}).find("a").get("href")
        songid= songid.split("track/")[1]
    
        url_date= x.split("daily/")[1]
        
        final.append([title, artist, songid, url_date])
 
#convert to data frame with pandas for easier data manipulation

final_df = pd.DataFrame(final, columns= ["Title", "Artist", "Song ID", "Chart Date"])

#write to csv

with open('spmooddata.csv', 'w') as f:
        final_df.to_csv(f, header= True, index=False)'''
