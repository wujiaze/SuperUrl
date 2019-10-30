import json

import redis
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from history.views import save_history
from index.models import SpiderTask
from picture.models import PictureKeyword, PictureInformation
from tools.sort import query_sort


def search_picture(request):
    if request.method == 'GET':
        # todo 步骤1 查询redis
        # todo 步骤2 查询mysql 更新redis
        # todo 步骤3 交给爬虫 结束
        save_history(request, 'picture')

        # print('进入get')
        keyword = request.GET.get('keyword')
        # print(keyword)

        r = redis.Redis(host='127.0.0.1', port=6379, db=2)

        if r.exists(keyword):
            keyword = "info:picture:" + keyword
            res = r.get(keyword)
            res_list = json.loads(res.decode())

            res = {
                'code': 200,
                'data': [{'picture:search':res_list}],
                'type':'picture',
            }

            return JsonResponse(res)

        else:
            try:
                # print('redis不存在')
                kw = PictureKeyword.objects.get(keyword=keyword)
                # print('kw',kw)
                info_list = kw.pictureinformation.order_by('-download_count')[:100]
                # print('info_list',info_list)
                all_list = []
                for item in info_list:
                    data_dict = {}
                    data_dict['describe'] = item.describe
                    data_dict['download_count'] = item.download_count
                    data_dict['url'] = item.url
                    # print(data_dict)
                    all_list.append(data_dict)
                high = len(all_list) - 1
                # all_list = query_sort(all_list, 0, high)
                # print(all_list)

                str_list = str(json.dumps(all_list))
                keyword = "info:picture:" + keyword
                r.set(keyword, str_list)

                result = {
                    'code': 200,
                    'data': [{'picture:search':all_list}],
                    'type':'picture'
                }

                return JsonResponse(result)



            except Exception as e:
                # print('都不存在')
                # print('----------------------------------------------')
                try:
                    task = SpiderTask.objects.filter(type='picture',keyword=keyword)
                    # print('task: ',task)
                    # print('长度: ',len(task))
                    if not len(task):
                        # print('不存在关键字')
                        SpiderTask.objects.create(type='picture', keyword=keyword)
                except Exception as e:
                    pass
                # print(task)
                # if not len(task):
                #     print('不存在关键字')
                #     SpiderTask.objects.create(type='picture', keyword=keyword)

                # todo 爬虫接口
                # 爬虫存到数据库
                return JsonResponse({'code': 20000, 'eroor': '暂无资源'})



