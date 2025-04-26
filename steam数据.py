import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
from DrissionPage import ChromiumPage
import time
import random
import pandas as pd
import re
import os

file_path = "链接.txt"
#文本处理
fi = open("链接.txt",'r')
o_herf = fi.readlines()
list_data=[]
for i in o_herf:
    list_data.append(''.join(i.strip('\n')))
list_data = list_data[0:500]
name = []#名称
q_da = []#最近评测
number_1 = []
number_2 = []
d_da = []#全部评测
lv = []
math1 =[]
fa = []
xing = []
d = {}

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
        name.append(soup.find('div', {'id': 'appHubAppName'}).text)
        biao = soup.find('div', {'class': 'user_reviews'})
        if biao.find_all('div')[2].find_all('span')[0]==None:
            q_da.append('')
        else:
            q_da.append(biao.find_all('div')[2].find_all('span')[0].text)
        if biao.find_all('div')[3].find_all('span')[0]==None:
            d_da.append('')
        else:
            d_da.append(biao.find_all('div')[3].find_all('span')[0].text)
        number = ''
        if biao.find_all('div')[2].find_all('span')[1]==None:
            number_1.append('')
        else:
            for num in re.findall(r'\d+', biao.find_all('div')[2].find_all('span')[1].text):
                number += num
            number_1.append(int(number))
        if biao.find_all('div')[3].find_all('span')[1]==None:
            number_2.append('')
            nn = ''
            for num in re.findall(r'\d+', biao.find_all('div')[3].find_all('span')[1].text):
                nn += num
            number_2.append(int(nn))
        if biao.find('a', {'class': 'steamdb_rating steamdb_rating_good'})==None:
            lv.append('')
        else:
            lv.append(biao.find('a', {'class': 'steamdb_rating steamdb_rating_good'}))
        if soup.find('div', {'class': 'date'})==None:
            math1.append('')
        else:
            math1.append(soup.find('div', {'class': 'date'}).text)
        if soup.find_all('div', {'class': 'dev_row'})[0].find('a')==None:
            fa.append('')
        else:
            fa.append(soup.find_all('div', {'class': 'dev_row'})[0].find('a').text)
        if soup.find_all('div', {'class': 'dev_row'})[1].find('a')==None:
            xing.append('')
        else:
            xing.append(soup.find_all('div', {'class': 'dev_row'})[1].find('a').text)
        aa += 1
        print(aa)
    except Exception as e:
        continue

d = {
    '名称':name,
    '最近评测':q_da,
    '最近评测人数':number_1,
    '全部评测':d_da,
    '全部评测人数':number_2,
    '好评率':lv,
    '日期':math1,
    '开发商':fa,
    '发行商':xing
}
df = pd.DataFrame(d)
df.to_excel('steam数1.xlsx')


