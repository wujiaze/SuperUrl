from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from index.models import Finger
import hashlib
import random

import redis


from music.models import MusicKeyword, MusicInformation

# 模拟爬虫 关键字得到的具体信息，放入mysql，建立关联
def pushMysql(request,keyword):
    data = [
        {'name': '彩虹',
         'star': "周杰伦",
         'download_count': '100',
         "star_one": "6",
         "star_two": "3",
         "star_three": "4",
         "star_four": "10",
         "star_five": "1",
         "time": "04:00",
         "star_avg": (6 * 1 + 3 * 2 + 4 * 3 + 10 * 4 + 1 * 5 + 100 * 3) / (100 + 6 + 3 + 4 + 10 + 1),
         'url': 'http://www.baidu.com'
         },
        {'name': '双节棍',
         'star': "周杰伦",
         'download_count': '50',
         "star_one": "2",
         "star_two": "6",
         "star_three": "10",
         "star_four": "6",
         "star_five": "9",
         "time": "04:18",
         "star_avg": (2 * 1 + 6 * 2 + 10 * 3 + 6 * 4 + 9 * 5 + 50 * 3) / (2 + 6 + 10 + 6 + 9 + 50),
         'url': 'http://www.baidu.com'
         },
        {'name': '爱你一万年',
         'star': "xxxx",
         'download_count': '189',
         "star_one": "14",
         "star_two": "17",
         "star_three": "4",
         "star_four": "19",
         "star_five": "29",
         "time": "05:18",
         "star_avg": (14 * 1 + 17 * 2 + 4 * 3 + 19 * 4 + 29 * 5 + 189 * 3) / (14 + 17 + 4 + 19 + 29 + 189),
         'url': 'http://www.baidu.com'
         }
    ]


    try:
        kw = MusicKeyword.objects.get(keyword=keyword)
    except:
        kw = MusicKeyword.objects.create(keyword=keyword)

    # finger 判断
    for item in data:
        m = hashlib.md5()
        m.update(item['url'].encode())
        url_m = m.hexdigest()
        result = Finger.objects.filter(url=url_m)
        if not result:
            # 添加
            music = MusicInformation.objects.create(**item)
            kw.musicinformation.add(music)
            Finger.objects.create(url=url_m)
        else:
            #
            if result[0].is_active:
                music = MusicInformation.objects.get(url=item['url'])
                kw.musicinformation.add(music)
    return JsonResponse({"code":200})