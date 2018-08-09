#coding=utf-8
from bs4 import BeautifulSoup
import re
import requests
from parsel import Selector
import pandas as pd
import time

# 进行网络请求的浏览器头部
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 BIDUBrowser/8.7 Safari/537.36'}
# pages是不同页码的网址列表
pages = ['https://bj.lianjia.com/ershoufang/xicheng/pg{}/'.format(x) for x in range(1, 2)]  #page number

lj_beijing = pd.DataFrame(columns=['房源编号', '交通'])
count = 0

def l_par_html(url):
    # 这个函数是用来获取链家网北京二手房的信息
    wr = requests.get(url, headers=headers, stream=True)
    sel = Selector(wr.text)
    # describ用来获取房源的文字信息
    describ = sel.xpath('//li[@class="clear"]//text()').extract()
    new_information = ([x for x in describ if x != '关注' and x != '加入对比'])
    sep_infor = ' '.join(new_information).split(r'/平米')[:-1]
    #print(sep_infor)
    #p= re.compile(r'((?:\s)距离(\S)+)')
    Subway=[]
    for i in sep_infor:
        sub=re.findall('距离(.*?)米',i)
        #sub='距离'+sub+'米'
        Subway.append(sub)
        #Subway=''.join(i)[:-1]
    #print(Subway)
    # hou_code用来获取房源的编号
    hou_code = sel.xpath('//li[@class="clear"]/a/@data-housecode').extract()
    # hou_image用来获取房源的图片
    #hou_image = sel.xpath('//li[@class="clear"]/a/img/@data-original').extract()
    # 将信息形成表格全部写到一起
    pages_info = pd.DataFrame(list(zip(hou_code, Subway)), columns=['房源编号', '交通'])
    return pages_info


for page in pages:
    a = l_par_html(page)
    count = count + 1
    print('the ' + str(count) + ' page is sucessful')
    time.sleep(5)
    lj_beijing = pd.concat([lj_beijing, a], ignore_index=True)

# 将表格数据输出到excel文件
lj_beijing.to_excel('d:\\lianjia_ershou_beijing_100.xlsx')