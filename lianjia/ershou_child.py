# -*- coding: utf-8 -*-
import requests
import time
from bs4 import BeautifulSoup


import pandas as pd

import matplotlib.pyplot as plt


url='https://bj.lianjia.com/ershoufang/yizhuangkaifaqu/'#area name

page=('pg')


headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
'Accept':'text/html;q=0.9,*/*;q=0.8',
'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
'Accept-Encoding':'gzip',
'Connection':'close',
'Referer':'http://www.baidu.com/link?url=_andhfsjjjKRgEWkj7i9cFmYYGsisrnm2A-TN3XZDQXxvGsM9k9ZZSnikW2Yds4s&amp;amp;wd=&amp;amp;eqid=c3435a7d00006bd600000003582bfd1f'
}

#page number
for i in range(1,21):
     if i == 1:
          i=str(i)
          a=(url+page+i+'/')
          r=requests.get(url=a,headers=headers)
          html=r.content
     else:
          i=str(i)
          a=(url+page+i+'/')
          r=requests.get(url=a,headers=headers)
          html2=r.content
          html = html + html2

     time.sleep(0.5)


lj=BeautifulSoup(html,'html.parser')


total_price=lj.find_all('div',attrs={'class':'totalPrice'})
#print(total_price)
tp=[]
for t in total_price:
    totalPrice=t.span.string
    tp.append(totalPrice)


unit_price=lj.find_all('div',attrs={'class':'unitPrice'})
up=[]
for u in unit_price:
    unitPrice=u.span.string
    up.append(unitPrice)


houseInfo = lj.find_all('div', attrs={'class': 'houseInfo'})
hi = []
for b in houseInfo:
    house = b.get_text()
    hi.append(house)


flood = lj.find_all('div', attrs={'class': 'flood'})
fl = []
for q in flood:
    fld = q.get_text()
    fl.append(fld)


followInfo = lj.find_all('div', attrs={'class': 'followInfo'})
fi = []
for c in followInfo:
    follow = c.get_text()
    fi.append(follow)


timeInfo = lj.find_all('div',attrs={'class':'timeInfo'})
print(timeInfo)
time=[]
for tm in timeInfo:
    tmInfo=tm.get_text()
    time.append(tmInfo)


Traffic = lj.find_all('div',attrs={'class':'tag'})
print(Traffic)
traffic=[]
for tf in Traffic:
    tfInfo=tf.get_text()
    traffic.append(tfInfo)
print(traffic)


pd.set_option('display.height',1000)
pd.set_option('display.max_rows',500)
pd.set_option('display.max_columns',500)
pd.set_option('display.width',1000)
house=pd.DataFrame({'totalprice':tp,'unitprice':up,'houseinfo':hi,'timeinfo':time,'flood':fl})

#print(house.head())



houseinfo_split = pd.DataFrame((x.split('/') for x in house.houseinfo),index=house.index,columns=[u'小区',u'户型',u'面积',u'朝向',u'装修',u'电梯'])
flood_split = pd.DataFrame((x.split('/') for x in house.flood),index=house.index,columns=[u'楼层',u'建筑年份',u'大区'])

#print(houseinfo_split.head())


house=pd.DataFrame({u'总价':tp,u'单价':up,u'发布时间':time})
house=pd.merge(house,houseinfo_split,right_index=True, left_index=True)
house=pd.merge(house,flood_split,right_index=True, left_index=True)
print(house.head())
house.to_excel('/Users/firmiana/desktop/lianjia_ershou_beijing_yizhuang')  #lianjia_ershou_beijing_xicheng.xlsx