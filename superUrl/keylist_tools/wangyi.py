import random
import requests
from urllib import parse
import json
from keylist_tools.random_useragents import ua_list


class QQYinyueSpider:
    def __init__(self):
        self.url = 'https://c.y.qq.com/splcloud/fcgi-bin/smartbox_new.fcg?key={}'

    def get_html(self,url):
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Cookie": "wluuid=WLGEUST-E0BBE2B7-F2BC-921A-82EF-3D69B10628A5; ssoflag=0; _ga=GA1.3.1336097348.1571143961; _gid=GA1.3.1343561331.1571143961; accessId=e7dfc0b0-b3b6-11e7-b58e-df773034efe4; weilisessionid3=3fdbe23f5edb67f7166e6fb1e126e4ca; wlsource=extbaidukey2; webp_enabled=0; qimo_seosource_e7dfc0b0-b3b6-11e7-b58e-df773034efe4=%E7%99%BE%E5%BA%A6%E6%90%9C%E7%B4%A2; qimo_seokeywords_e7dfc0b0-b3b6-11e7-b58e-df773034efe4=%25E5%259B%25BE%25E8%2599%25AB%25E5%259B%25BE%25E7%2589%2587; href=https%3A%2F%2Fstock.tuchong.com%2F%3Fsource%3Dextbaidukey2%26utm_source%3Dextbaidukey2; pageViewNum=2",
            "Host": "stock.tuchong.com",
            "Referer": "https://stock.tuchong.com/?source=extbaidukey2&utm_source=extbaidukey2",
            "User-Agent": random.choice(ua_list),
            "X-Requested-With": "XMLHttpRequest",
        }
        html = requests.get(url=url,headers=headers).json()
        res = html['data']['song']['itemlist']
        res_list = []
        for item in res:
            # print(item)
            res_list.append(item['name'])
        return res_list



    def run(self,word):

        word = parse.quote(word)
        print(word)
        url = self.url.format(word)
        print(url)
        res = self.get_html(url)
        print(res)
        return res

if __name__ == '__main__':
    spider = QQYinyueSpider()
    result = spider.run('人')
    # print(result)