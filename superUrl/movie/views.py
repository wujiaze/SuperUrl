from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
import redis

from movie.models import MovieKeyword, MovieInfomation


def movie(request):
    if request.method=='GET':
        operation=request.GET.get('operation')
        keyword=request.GET.get('keyword')
        r = redis.Redis('127.0.0.1', 6379, db=4)

        if int(operation)==1:
            if not keyword:
                result = {}
                return JsonResponse(result)
            #如果缓存有数据,返回data
            if r.exists(keyword):
                # 取出所有的数据
                pass
                result = {}
                return JsonResponse(result)
            else:
                #去数据库查找
                try:
                    print(keyword)
                    kw=MovieKeyword.objects.get(keyword=keyword).movieInfomation.all()
                    print('qqqqqqqqqqqqqqqqqqqqqqqqqqqq')
                    print('kw',kw)

                    #返回data
                    data=['aaa','bbb']
                    result = {'code': 200, 'data': [{"":"",'':""},{},{}]}
                    return JsonResponse(result)

                except Exception as e:
                    print('关键字表没有字段')
                    #交给爬虫借口,爬到数据多对多加载到数据库中

                    data=[{'name':'霸王别姬','director':'xx','actor':'张国荣','url':'www.xxx.com','releasetime':'1999-10-10'},
                          {'name':'霸王别姬2','director':'xx','actor':'张国荣','url':'www.xxx.com','releasetime':'1999-10-10'},
                          {'name':'霸王别姬3','director':'xx','actor':'张国荣','url':'www.xxx.com','releasetime':'1999-10-10'}]
                    kw = MovieKeyword.objects.create(keyword=keyword)
                    for i in data:
                        movie=MovieInfomation.objects.create(name=i['name'],director=i['director'],actor=i['actor'],
                                                             url=i['url'])
                        print(keyword)
                        kw.movieInfomation.add(movie)
                    result={'code':200,'data':{'a':'q'}}
                    return JsonResponse(result)


        else:
            pass


    else:
        result={'code':40000,'error':'pls GET request'}
        return JsonResponse(result)









