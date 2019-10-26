import json

import redis
from django.http import JsonResponse
from django.shortcuts import render


# Create your views here.

def get_keylist(request):
    type_search = request.GET.get('type')
    keyword = request.GET.get('kw')

    r = redis.Redis(host='127.0.0.1', port=6379, db=1)
    keyword = type_search + ':keylist:' + keyword

    if r.exists(keyword):
        res = r.get(keyword)
        print(type(res.decode()))
        res_list = json.loads(res.decode())

        res = {
            'code': 200,
            'data': res_list
        }

        return JsonResponse(res)
    else:
        # todo 爬虫爬取keylist 存储到redis
        # keylist = run(type,kw)
        res = {
            'code': 20000,
            'error': '暂无数据'
        }
        return JsonResponse(res)


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
    else:
        res = {
            'code': 20000,
            'error': '类型错误'
        }
        return JsonResponse(res)
