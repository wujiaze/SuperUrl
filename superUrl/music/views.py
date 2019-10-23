import redis
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.



def search_music(request):
    if request.method == 'GET':
        operation = request.GET.get('operation')
        keyword = request.GET.get('keyword')
        print(operation)
        print(keyword)
        if operation == 0:
            #todo 爬虫接口
            pass
        elif operation == 1:
            r = redis.Redis(host='127.0.0.1', port=6379, db=2)
            res = r.exists(keyword)
            if res == 1:
                data_list = r.lrange(keyword,0,-1)
                for data in data_list:
                    data = data.decode()
                    # name = data.split(',')[]
                    # download = data.split(',')[]
                    # name = data.split(',')[]
                    # name = data.split(',')[]
                    # name = data.split(',')[]
                    # name = data.split(',')[]
                    # name = data.split(',')[]
                    # name = data.split(',')[]
                    # name = data.split(',')[]
                    # name = data.split(',')[]

            elif res ==0:
                #todo 爬虫接口
                pass


            return JsonResponse({'code':200})



