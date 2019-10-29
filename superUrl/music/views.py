import random

import redis
from django.http import JsonResponse
from django.shortcuts import render
from music.models import MusicInformation, MusicKeyword
import json
from history.views import save_history
from tools.sort import query_sort
from index.models import SpiderTask


# Create your views here.


def search_music(request):
    if request.method == 'GET':
        # todo 步骤1 查询redis
        # todo 步骤2 查询mysql 更新redis
        # todo 步骤3 交给爬虫 结束
        save_history(request, 'music')

        # print('进入get')
        keyword = request.GET.get('keyword')
        # print(keyword)

        r = redis.Redis(host='127.0.0.1', port=6379, db=2)

        if r.exists(keyword):
            keyword = "info:music:" + keyword
            res = r.get(keyword)
            res_list = json.loads(res.decode())

            res = {
                'code': 200,
                'data': [{'music:search': res_list}],
                'type': 'music',
            }

            return JsonResponse(res)

        else:
            try:
                # print('redis不存在')
                kw = MusicKeyword.objects.get(keyword=keyword)
                info_list = kw.musicinformation.all()
                all_list = []
                for item in info_list:
                    data_dict = {}
                    data_dict['name'] = item.name
                    data_dict['star'] = item.star
                    data_dict['download_count'] = item.download_count
                    data_dict['star_one'] = item.star_one
                    data_dict['star_two'] = item.star_two
                    data_dict['star_three'] = item.star_three
                    data_dict['star_four'] = item.star_four
                    data_dict['star_five'] = item.star_five
                    data_dict['star_avg'] = item.star_avg
                    data_dict['url'] = item.url
                    all_list.append(data_dict)

                high = len(all_list) - 1
                all_list = query_sort(all_list, 0, high)

                str_list = str(json.dumps(all_list))
                keyword = "info:music:" + keyword
                r.set(keyword, str_list)

                result = {
                    'code': 200,
                    'data': [{'music:search': all_list}],
                    'type': 'music'
                }

                return JsonResponse(result)



            except Exception as e:
                # print('都不存在')
                # print('----------------------------------------------')
                try:
                    task = SpiderTask.objects.filter(type='music', keyword=keyword)
                    # print('task: ', task)
                    # print('长度: ', len(task))
                    if not len(task):
                        # print('不存在关键字')
                        SpiderTask.objects.create(type='music', keyword=keyword)
                except Exception as e:
                    pass

                return JsonResponse({'code': 20000, 'eroor': '暂无资源'})

                # # todo 爬虫接口
                # # 爬虫存到数据库




