from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from index.models import Finger
import hashlib
import random

import redis

from music.models import MusicKeyword, MusicInformation

# 模拟爬虫 关键字得到的具体信息，放入mysql，建立关联
from picture.models import PictureKeyword, PictureInformation


def pushMysql(request, keyword):
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
        try:
            kw = MusicKeyword.objects.create(keyword=keyword)
        except Exception as e:
            print('sssssss',e)
            return
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
    return JsonResponse({"code": 200})


def pushPicture(request, keyword):
    data = []
    for i in range(100):
        data.append({'describe': '万圣节',
                     'url': 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1572960314&di=eccb6a44d73beb4bf609ce1d7dd3bce0&imgtype=jpg&er=1&src=http%3A%2F%2Fpic26.nipic.com%2F20121230%2F9034633_172138299000_2.jpg'
                     })
    print('no redis , no mysql')
    print(keyword)
    try:
        print('create keyword')
        kw = PictureKeyword.objects.create(keyword=keyword)
    except Exception as e:
        print('已经存在关键字')
        kw = PictureKeyword.objects.get(keyword=keyword)
    for i in data:
        try:
            picture = PictureInformation.objects.create(describe=i['describe'], url=i['url'])
        except Exception as e:
            picture = PictureInformation.objects.get(url=i['url'])
        kw.pictureinformation.add(picture)
    #
    # kw = MusicKeyword.objects.get(keyword=keyword)
    # info_list = kw.musicinformation.all()
    # all_list = []
    # redis_list = []
    # for item in info_list:
    #     data_dict = {}
    #     data_dict['describe'] = item.describe
    #     data_dict['download_count'] = item.download_count
    #     data_dict['url'] = item.url
    #     all_list.append(data_dict)
    #     info = [str(item.describe),
    #             str(item.download_count),
    #             str(item.url)]
    #     res = ','.join(info)
    #     redis_list.append(res)
    # keep_time = 60 * 60 * 24
    # r.lpush(keyword, redis_list)
    # r.expire(keyword, random.randint(keep_time, 2 * keep_time))

    # print(data)
    # result = {
    #     'code': 200,
    #     'data': [{'search:picture': data}]
    # }
    # result = {'code': 20000,
    #           'error': '暂无资源'}
    #
    # return JsonResponse(result)
