from django.test import TestCase
import hashlib
import random

import redis

from index.models import Finger
from music.models import MusicKeyword, MusicInformation

r = redis.Redis(db=1)
# Create your tests here.
# 模拟爬虫 关键字得到的具体信息，放入mysql，建立关联
def pushMysql(keyword):
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
        m.update(item['url'])
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

    # kw = MusicKeyword.objects.get(keyword=keyword)
    # info_list = kw.musicinformation.all()
    # all_list = []
    # redis_list = []
    # for item in info_list:
    #     data_dict = {}
    #     data_dict['name'] = item.name
    #     data_dict['download_count'] = item.download_count
    #     data_dict['star_one'] = item.star_one
    #     data_dict['star_two'] = item.star_two
    #     data_dict['star_three'] = item.star_three
    #     data_dict['star_four'] = item.star_four
    #     data_dict['star_five'] = item.star_five
    #     data_dict['star_avg'] = item.star_avg
    #     data_dict['url'] = item.url
    #     all_list.append(data_dict)
    #     info = [str(item.name),
    #             str(item.download_count),
    #             str(item.star_one),
    #             str(item.star_two),
    #             str(item.star_three),
    #             str(item.star_four),
    #             str(item.star_five),
    #             str(item.star_avg),
    #             str(item.url)]
    #     res = ','.join(info)
    #     redis_list.append(res)
    # keep_time = 60 * 60 * 24
    # r.lpush(keyword, redis_list)
    # r.expire(keyword, random.randint(keep_time, 2 * keep_time))
    # return


# 模拟爬虫 定时更新,获取新歌，放入mysql，建立关联，放入redis，将热歌从信息库中放入redis

# redis 中 新歌，热歌，搜索结果 的 存储形式 和返回形式


pushMysql("周杰伦")
