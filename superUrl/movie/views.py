from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
import redis
from movie.models import MovieKeyword, MovieInfomation


def movie(request):
    if request.method=='GET':
        keyword=request.GET.get('keyword')
        r = redis.Redis('127.0.0.1', 6379, db=4)
        #如果没有输入关键字,返回榜单
        # if not keyword:
        #     result = {}
        #     return JsonResponse(result)

        #如果缓存有数据,返回data
        if r.exists(keyword):
            # 取出所有的数据,data_list=[]
            data_list=r.lrange(keyword,0,-1)
            all_list=[]
            for data in data_list:
                data=data.decode()
                data_dict = {}


                data_dict['name'] = name
                data_dict['director'] =director
                data_dict['actor'] = actor
                data_dict['download_count'] = download_count
                data_dict['star_one'] = star_one
                data_dict['star_two'] = star_two
                data_dict['star_three'] = star_three
                data_dict['star_four'] = star_four
                data_dict['star_five'] = star_five
                data_dict['star_avg'] = stat_avg
                data_dict['url'] = url

                all_list.append(data_dict)
            result = {
                'code':200,
                'data':all_list
            }
            return JsonResponse(result)
        else:
            #去数据库查找
            try:
                kw=MovieKeyword.objects.get(keyword=keyword).movieInfomation.all()
                print('qqqqqqqqqqqqqqqqqqqqqqqqqqqq')
                print('kw',kw)
                all_list = []
                for i in kw:
                    data_dict = {}
                    data_dict['name']=i.name
                    data_dict['director'] = director
                    data_dict['actor'] = actor
                    data_dict['download_count'] = download_count
                    data_dict['star_one'] = star_one
                    data_dict['star_two'] = star_two
                    data_dict['star_three'] = star_three
                    data_dict['star_four'] = star_four
                    data_dict['star_five'] = star_five
                    data_dict['star_avg'] = stat_avg
                    data_dict['url'] = url
                    #加近redis
                    pass
                    all_list.append(data_dict)


                #返回data
                result = {'code': 200, 'data':all_list}
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
        result={'code':40000,'error':'pls GET request'}
        return JsonResponse(result)









