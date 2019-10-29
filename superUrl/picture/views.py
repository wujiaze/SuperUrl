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

        print('进入get')
        keyword = request.GET.get('keyword')
        print(keyword)

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
                print('redis不存在')
                kw = PictureKeyword.objects.get(keyword=keyword)
                print('kw',kw)
                info_list = kw.pictureinformation.order_by('-download_count')[:100]
                print('info_list',info_list)
                all_list = []
                for item in info_list:
                    data_dict = {}
                    data_dict['describe'] = item.describe
                    data_dict['download_count'] = item.download_count
                    data_dict['url'] = item.url
                    print(data_dict)
                    all_list.append(data_dict)
                high = len(all_list) - 1
                # all_list = query_sort(all_list, 0, high)
                print(all_list)

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
                # SpiderTask.objects.create(type='picture', keyword=keyword)
                # # todo 爬虫接口
                # # 爬虫存到数据库
                # return JsonResponse({'code': 20000, 'eroor': '暂无资源'})


                data = [{'describe':'万圣节','url':'https://stock.tuchong.com/image?imageId=462030668900860178&term=&requestId=&searchId='},
                        {'describe':'万圣节','url':'https://stock.tuchong.com/image?imageId=400180227832283149&term=&requestId=&searchId='},
                        {'describe':'万圣节','url':'https://stock.tuchong.com/image?imageId=455008010808066106&term=&requestId=&searchId='}]
                # print('no redis , no mysql')
                # print(keyword)
                try:
                    print('create keyword')
                    kw = PictureKeyword.objects.create(keyword=keyword)
                except Exception as e:
                    print('已经存在关键字')
                    return JsonResponse({'code':20000,'error':'稍后访问'})
                for i in data:
                    try:
                        picture = PictureInformation.objects.create(describe=i['describe'],url=i['url'])
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
                # keep_time = 60 * 60 *24
                # r.lpush(keyword, redis_list)
                # r.expire(keyword,random.randint(keep_time,2*keep_time))
                #
                print(data)
                result = {
                    'code': 200,
                    'data': [{'search:picture':data}]
                }
                # result = {'code':20000,
                #           'error':'暂无资源'}

                return JsonResponse(result)
