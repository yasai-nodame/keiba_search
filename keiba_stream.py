import streamlit as st
import sqlite3
import pandas as pd

db_name = 'keiba.db'

race_name_list = []

for i in range(100):
    race_sql = f'SELECT レース名 FROM keiba_list{i}'

    with sqlite3.connect(db_name) as conn:
        
        df_from_sql = pd.read_sql(race_sql,conn)
        
        race_column_array = df_from_sql.values
        
        list_from_array = race_column_array.tolist() #arrayからlistに変換
        
        race_name_list.append(list_from_array[0][0])

option = st.selectbox(
    'レース名を選んでください',
    (race_name_list) #データベースのレース名に複数個値が入ってるから先頭の１つの値だけ取得
)



if st.button('選択したレース結果を表示します。'):
    for index,j in enumerate(race_name_list):
        if j == option:
            race_all_sql = f'SELECT 着順,枠番,馬番,馬名,性齢,斤量,騎手,タイム,着差,単勝,人気,馬体重,調教師 FROM keiba_list{index}'
    
            with sqlite3.connect(db_name) as conn:
                df_all_sql = pd.read_sql(race_all_sql,conn)
        
            st.dataframe(df_all_sql)

