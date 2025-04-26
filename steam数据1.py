import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
from DrissionPage import ChromiumPage
import time
import random
import pandas as pd
import re
import os
import mysql.connector
from datetime import datetime
file_path = "链接.txt"
#文本处理
#数据库链接
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="123456",
)
cursor = conn.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS steamdb")
cursor.execute("USE steamdb")
# 创建表 steamDate
cursor.execute('''
CREATE TABLE IF NOT EXISTS steamDate (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,         
    q_da TEXT,                       
    number_1 INT,                      
    d_da TEXT,                    
    math1 TEXT,                        
    fa TEXT,                           
    xing TEXT                         
)
''')
conn.commit()
print("Table 'steamDate' created successfully.")
fi = open("链接.txt",'r')
o_herf = fi.readlines()
list_data=[]
for i in o_herf:
    list_data.append(''.join(i.strip('\n')))
list_data = list_data[1400:2100]
data_list=[]

if os.path.exists(file_path):
    print(f"{file_path}存在")


else:
    url = 'https://store.steampowered.com/search/?sort_by=_ASC&ignore_preferences=1&filter=globaltopsellers'
    dp = ChromiumPage()
    dp.get(url)
    h = open('链接.txt', 'a', encoding='utf-8')


    def pa():
        next_page()
        soup = BeautifulSoup(dp.html, 'html.parser')
        div = soup.find('div', {'id': 'search_resultsRows'})
        for href in div.find_all('a'):
            h.write(href.get('href') + '\n')


    # 自动滑动，滑动次数为3000/50，150次，需要将网页链接保存到本地，避免多次爬取
    def next_page():
        for i in range(151):
            random_time = random.uniform(0.5, 1.5)
            time.sleep(random_time)
            dp.scroll.to_bottom()
    pa()
aa = 1
for i in list_data:
    try:
        if 'Steam_Deck' in i:
            continue

        url_y = requests.get(i)
        soup = BeautifulSoup(url_y.text, 'html.parser')
        name=soup.find('div', {'id': 'appHubAppName'}).text
        biao = soup.find('div', {'class': 'user_reviews'})
        if biao.find_all('div')[2].find_all('span')[0]==None:
            q_da=''
        else:
            q_da=biao.find_all('div')[2].find_all('span')[0].text
        if biao.find_all('div')[3].find_all('span')[0]==None:
            d_da=''
        else:
            d_da=biao.find_all('div')[3].find_all('span')[0].text
        number = ''
        if biao.find_all('div')[2].find_all('span')[1]==None:
            number_1=''
        else:
            for num in re.findall(r'\d+', biao.find_all('div')[2].find_all('span')[1].text):
                number += num
            number_1=int(number)
        number_2=' '
        if biao.find_all('div')[3].find_all('span')[1]==None:
            nn = ''
            for num in re.findall(r'\d+', biao.find_all('div')[3].find_all('span')[1].text):
                nn += num
            number_2=int(nn)
        print(biao.find('a', {'class': 'steamdb_rating steamdb_rating_good'}))
        if biao.find('a', {'class': 'steamdb_rating steamdb_rating_good'})==None:

            lv=' '
        else:
            lv=biao.find('a', {'class': 'steamdb_rating steamdb_rating_good'}).text
        if soup.find('div', {'class': 'date'})==None:
            math1=''
        else:
            math1=soup.find('div', {'class': 'date'}).text
        if soup.find_all('div', {'class': 'dev_row'})[0].find('a')==None:
            fa=''
        else:
            fa=soup.find_all('div', {'class': 'dev_row'})[0].find('a').text
        if soup.find_all('div', {'class': 'dev_row'})[1].find('a')==None:
            xing=''
        else:
            xing=soup.find_all('div', {'class': 'dev_row'})[1].find('a').text
        d = {
            '名称': name,
            '最近评测': q_da,
            '最近评测人数': number_1,
            '全部评测': d_da,
            # '全部评测人数':number_2,
            # '好评率':lv,
            '日期': math1,
            '开发商': fa,
            '发行商': xing
        }
        data_list.append(d)
        aa += 1
        print(aa)
    except Exception as e:
        continue

# 插入数据的函数
def insert_data(name, q_da, number_1, d_da, math1, fa, xing):
    cursor.execute('''
    INSERT INTO steamDate (name, q_da, number_1, d_da, math1, fa, xing)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ''', (name, q_da, number_1, d_da, math1, fa, xing))
    conn.commit()
    print(f"Inserted data for game: {name}")



# 循环插入数据
for data in data_list:
    # print(data)
    try:
        insert_data(
            name=data["名称"],
            q_da=data["最近评测"],
            number_1=data["最近评测人数"],
            d_da=data["全部评测"],
            math1=data["日期"],
            fa=data["开发商"],
            xing=data["发行商"]
        )
    except Exception as e:
        continue

# 关闭连接
cursor.close()
conn.close()


