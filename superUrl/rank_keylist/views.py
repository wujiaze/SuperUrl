import json
import random

import redis
from django.http import JsonResponse
from django.shortcuts import render
from keylist_tools.tuchong import TuChongSpider
from keylist_tools.wangyi import QQYinyueSpider
from keylist_tools.maoyan import MaoyanSpider
from keylist_tools.duyyy_movie import DutttSpider


# Create your views here.

def get_keylist(request):
    type_search = request.GET.get('type')
    # print(type_search)
    keyword = request.GET.get('kw')
    # print(keyword)
    keyword_2 = keyword
    r = redis.Redis(host='127.0.0.1', port=6379, db=1)
    keyword = type_search + ':keylist:' + keyword
    keep_time = 60 * 60 * 24
    if r.exists(keyword):
        res = r.get(keyword)
        # print(type(res.decode()))
        res_list = json.loads(res.decode())

        res = {
            'code': 200,
            'data': res_list
        }

        return JsonResponse(res)
    else:
        # todo 爬虫爬取keylist 存储到redis
        # keylist = run(type,kw)

        if type_search == 'picture':
            keylist = TuChongSpider().run(keyword_2)
            if keylist:
                keylist = list(set(keylist))
        elif type_search == 'music':
            # print(keyword)
            keylist = QQYinyueSpider().run(keyword_2)
            if keylist:
                keylist = list(set(keylist))
            # print(keylist)
        elif type_search == 'movie':
            # print('join get music')
            # keylist = MaoyanSpider().run(keyword_2)
            keylist = MaoyanSpider().run(keyword_2)
            if keylist:
                keylist = list(set(keylist))

        else:
            res = {
                'code': 20000,
                'error': '暂无数据'
            }
            return JsonResponse(res)

        if not keylist:
            res = {
                'code': 20000,
                'error': '暂无数据'
            }
            return JsonResponse(res)

        res = json.dumps(keylist)
        r.set(keyword, res)
        r.expire(keyword, random.randint(3 * 60 * 60, 6 * 60 * 60))

        if keyword:
            res = {
                'code': 200,
                'data': keylist
            }
            return JsonResponse(res)
        else:
            res = {
                'code': 20000,
                'error': '暂无数据'
            }
            return JsonResponse(res)


# rank 返回形式
"""
{
    code:
    data:[
        { "music:hot" : 
            [
                {具体信息},
                {具体信息}
            ]
        },
        { "music:new" : 
            [
                {具体信息},
                {具体信息}
            ]
        }
    ]
}
{
    code:
    data:[
        { "music:search" : 
            [
                {具体信息},
                {具体信息}
            ]
        }
    ]
}
"""


def get_rank(requesst):
    type = requesst.GET.get('type')
    r = redis.Redis(host='127.0.0.1', port=6379, db=1)
    res_list = []
    # print(type)
    if type == 'music':
        if r.exists('music:new'):
            new_list = json.loads(r.get('music:new').decode())  # [{},{},{}]
            res_list.append({'music:new': new_list})
        if r.exists('music:hot'):
            hot_list = json.loads(r.get('music:hot').decode())  # [{},{},{}]
            res_list.append({'music:hot': hot_list})
        # print(res_list)
        if res_list:
            result = {
                'code': 200,
                'type': type,
                'data': res_list
            }
        else:
            result = {
                'code': 20000,
                'error': '暂无榜单'
            }
        return JsonResponse(result)
    elif type == 'movie':
        if r.exists('movie:new'):
            new_list = json.loads(r.get('movie:new').decode())  # [{},{},{}]
            res_list.append({'movie:new': new_list})
        if r.exists('movie:hot'):
            hot_list = json.loads(r.get('movie:hot').decode())  # [{},{},{}]
            res_list.append({'movie:hot': hot_list})
        if res_list:
            result = {
                'code': 200,
                'type': type,
                'data': res_list
            }
        else:
            result = {
                'code': 20000,
                'error': '暂无榜单'
            }
        return JsonResponse(result)
    elif type == 'picture':
        if r.exists('picture:search'):
            new_list = json.loads(r.get('picture:search').decode())  # [{},{},{}]
            res_list.append({'picture:search': new_list})
        if res_list:
            result = {
                'code': 200,
                'type': type,
                'data': res_list
            }
        else:
            result = {
                'code': 20000,
                'error': '暂无榜单'
            }
        return JsonResponse(result)
    else:
        res = {
            'code': 20000,
            'error': '类型错误'
        }
        return JsonResponse(res)
