# -*- coding: utf-8 -*-
# 作者:shihan
# 利用cookies登陆豆瓣
import requests
from bs4 import BeautifulSoup
from faker import Factory
import pymongo

f = Factory.create()
# 链接MongoDB数据库
MONGO_URL = 'localhost'
MONGO_DB = 'douban'
MONGO_TABLE = 'diary'
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

headers = {'User-Agent': f.user_agent()}
cookies = {
    'Cookie': 'll="118159"; bid=vtxN91Haz2A; __utmc=30149280; _ga=GA1.2.743719855.1520321188; _gid=GA1.2.1766216780.1520321190; __yadk_uid=skyCSDdu8oUopaypRrfMUuTdozY2B3n4; push_doumail_num=0; ap=1; ps=y; ct=y; ue="mingmenyun@163.com"; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1520391796%2C%22https%3A%2F%2Faccounts.douban.com%2Flogin%3Falias%3Dhaxidata%2540163.com%26redir%3Dhttps%253A%252F%252Fwww.douban.com%26source%3DNone%26error%3D1015%22%5D; _pk_ses.100001.8cb4=*; __utma=30149280.743719855.1520321188.1520386981.1520391797.9; __utmz=30149280.1520391797.9.5.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/login; __utmv=30149280.15758; dbcl2="157585308:TEN6XCUKvFs"; ck=Eki-; _pk_id.100001.8cb4=1d1413d996ad30a4.1520321180.9.1520391859.1520387028.; __utmb=30149280.5.10.1520391797; push_noty_num=1'}
url = 'http://www.douban.com'
response = requests.get(url, cookies=cookies, headers=headers)
soup = BeautifulSoup(response.text, 'lxml')
results = soup.findAll('div', attrs={"class": "new-status"})

item = {}
for result in results:
    img_ele = result.find('div', attrs={'class': "pic-wrap"})
    content_ele = result.find('div', attrs={'class': 'content'})
    if content_ele is not None:
        title = content_ele.find('a').get_text()
        summary = content_ele.find('p').get_text()
        if img_ele is not None:
            img_url = img_ele.find('img')['src']
            item['title'] = title
            item['img_url'] = img_url
            item['summary'] = summary
            try:
                if db[MONGO_TABLE].insert(item):
                    print('存储到MONGODB成功', item)
            except Exception:
                print('存储到MONGODB失败', item)

print(response.text)

