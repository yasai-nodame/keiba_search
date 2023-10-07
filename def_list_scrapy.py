import requests 
from bs4 import BeautifulSoup 
import pandas as pd
import pandas.io.sql as psql 
import sqlite3 
import csv
import re 
import io,sys

#引数に競馬のリンクのリストを取得した関数処理
def link_html(race_link_list):
    #リンクのページを取得
    url = 'https://db.netkeiba.com'+race_link_list
    
    read_html = pd.read_html(url)[0]
    
    return read_html
    
    

#csvをデータベースに追加する関数
def database_from_csv():
    conn = sqlite3.connect('keiba.db')
    cur = conn.cursor()
    
    
    for i in range(100):
            
            
        sql = f'''
        CREATE TABLE IF NOT EXISTS keiba_list{i}
        (
            '着順' TEXT,
            '枠番' TEXT,
            '馬番' TEXT,
            '馬名' TEXT,
            '性齢' TEXT,
            '斤量' TEXT,
            '騎手' TEXT,
            'タイム' TEXT,
            '着差' TEXT,
            '単勝' TEXT,
            '人気' TEXT,
            '馬体重' TEXT,
            '調教師' TEXT
        )
        '''
        cur.execute(sql)
        
        open_csv = open(f'csv_folda/keiba_list{i}.csv',encoding="utf-8")
        read_csv = csv.reader(open_csv)
        
        rows = []
        for row in read_csv:
            row_drop = row.pop(0) #多重リストだからrowはリスト。なのでリストの０番目のインデックスを消す。
            rows.append(row)
        
        
        
        cur.executemany(
            f"INSERT INTO keiba_list{i}(着順,枠番,馬番,馬名,性齢,斤量,騎手,タイム,着差,単勝,人気,馬体重,調教師)VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",rows
        )
        
        conn.commit()
        open_csv.close()
        
            
def date_from_name():
    
    race_r_list = []
    
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
    
    url = 'https://db.netkeiba.com//?pid=race_list&word=&start_year=2017&start_mon=1&end_year=2022&end_mon=12&jyo%5B0%5D=10&kyori_min=&kyori_max=&sort=date&list=100&page=1'


    response = requests.get(url)

    soup = BeautifulSoup(response.content,'html.parser')

    race_date = soup.find_all(href = re.compile('/race/list/20'))
    
    race_name = soup.find_all(href = re.compile('/race/20'))
    
    race_round = soup.find_all('td',class_='txt_r') #レースラウンド、頭数、タイムの順でスクレイピングされる
    
    #レースラウンドだけ取得
    for i,j in enumerate(race_round):
        if i == 0 or i % 3 == 0:
            race_r_list.append(race_round[i].text + 'R')
    
    conn = sqlite3.connect('keiba.db')
    cur = conn.cursor()
    
    for i in range(100):
        
        race_total = race_date[i].text + ' ' + ' ' + race_r_list[i] + ' ' + race_name[i].text
    
    #keiba.dbに新しいカラム名を追加し、日付と名前を合わせて追加する
        sql = f'''
        ALTER TABLE keiba_list{i} ADD COLUMN レース名 TEXT default '{race_total}';

        '''
        
        cur.execute(sql)
    
    conn.commit()
    conn.close()


def race_turn():
    race_r_list = []
    
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
    
    url = 'https://db.netkeiba.com//?pid=race_list&word=&start_year=2017&start_mon=1&end_year=2022&end_mon=12&jyo%5B0%5D=10&kyori_min=&kyori_max=&sort=date&list=100&page=1'
    
    response = requests.get(url)
    
    soup = BeautifulSoup(response.content,'html.parser')
    
    race_round = soup.find_all('td',class_='txt_r') #レースラウンド、頭数、タイムの順でスクレイピングされる
    
    #レースラウンドだけ取得
    for i,j in enumerate(race_round):
        if i == 0 or i % 3 == 0:
            race_r_list.append(race_round[i].text + 'R')
            
    conn = sqlite3.connect('keiba.db')
    cur = conn.cursor()
    
    #レースラウンドを既存のテーブルの新しいカラムに追加していく
    for index in range(100):
        sql = f'''
        ALTER TABLE keiba_list{index} ADD COLUMN レースR TEXT default '{race_r_list[index]}';
        '''
        cur.execute(sql)
        
    
    conn.commit()
    conn.close()

def delete_recode():
    #必要のないレコードを削除する
    conn = sqlite3.connect('keiba.db')
    cur = conn.cursor()
    
    #keiba.dbに新しいカラム名を追加し、日付と名前を合わせて追加する
    for i in range(100):
        sql = f'''
        DELETE FROM keiba_list{i} WHERE 着順 = (SELECT 着順 FROM keiba_list{i} limit 1);
        '''
        
        cur.execute(sql)
    
    conn.commit()
    conn.close()