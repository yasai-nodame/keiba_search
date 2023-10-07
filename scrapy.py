import requests 
from bs4 import BeautifulSoup 
import re
import def_list_scrapy
import sqlite3

url = 'https://db.netkeiba.com//?pid=race_list&word=&start_year=2017&start_mon=1&end_year=2022&end_mon=12&jyo%5B0%5D=10&kyori_min=&kyori_max=&sort=date&list=100&page=1'


response = requests.get(url)

response.encoding = 'UTF-8'

soup = BeautifulSoup(response.content,'html.parser')

a_tag = soup.find_all(href = re.compile('/race/20'))

#空のリスト作成
race_link_list = []

#1pageにつき100件のリンクをリストに追加する
for element in a_tag:
    link = element.attrs['href']
    race_link_list.append(link)
    

# for i in range(len(race_link_list)):
#     def_list_scrapy.link_html(race_link_list[i]).to_csv(f'csv_folda/keiba_list{i}.csv')
    
    
def_list_scrapy.delete_recode()
    