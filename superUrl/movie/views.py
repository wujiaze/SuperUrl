import random

from django.http import JsonResponse
from django.shortcuts import render
import json
from history.views import save_history

# Create your views here.
import redis

from index.models import SpiderTask
from movie.models import MovieKeyword, MovieInfomation
from tools.sort import query_sort


def movie(request):
    if request.method == 'GET':
        # todo 步骤1 查询redis
        # todo 步骤2 查询mysql 更新redis
        # todo 步骤3 交给爬虫 结束


        print('进入get')
        keyword = request.GET.get('keyword')
        print(keyword)

        r = redis.Redis(host='127.0.0.1', port=6379, db=4)



        #如果没有输入关键字,返回榜单
        # if not keyword:
        #     result = {}
        #     return JsonResponse(result)

        #如果缓存有数据,返回data
        keyword_2 = keyword
        if r.exists(keyword):

            keyword = "info:movie:" + keyword
            res = r.get(keyword)
            res_list = json.loads(res.decode())

            res = {
                'code':200,
                'data':res_list
            }

            return JsonResponse(res)

        else:
            try:
                print('redis不存在')
                kw = MovieInfomation.objects.get(keyword=keyword)
                print(kw)
                info_list = kw.movieInfomation.all()
                all_list = []
                for item in info_list:
                    data_dict = {}
                    data_dict['name'] = item.name
                    data_dict['director'] = item.director
                    data_dict['actor'] = item.actor
                    data_dict['releasetime'] = item.releasetime
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
                r.set(keyword,str_list)

                result = {
                    'code': 200,
                    'data': all_list
                }

                return JsonResponse(result)


            except Exception as e:
                # print('都不存在')
                # print('----------------------------------------------')
                # SpiderTask.objects.create(type='movie', keyword=keyword)
                # # todo 爬虫接口
                # # 爬虫存到数据库
                # return JsonResponse({'code': 20000, 'eroor': '暂无资源'})


                data = [{'name':'aaa1','url':'xxx1'},
                        {'name':'aaa2','url':'xxx2'},
                        {'name':'aaa3','url':'xxx3'}]
                print('no redis , no mysql')
                print(keyword)
                try:
                    print('create keyword')
                    kw = MovieKeyword.objects.create(keyword=keyword)
                except Exception as e:
                    print('已经存在关键字')
                    return JsonResponse({'code':20000,'error':'稍后访问'})
                for i in data:
                    try:
                        movie = MovieInfomation.objects.create(name=i['name'],url=i['url'])
                    except Exception as e:
                        movie = MovieInfomation.objects.get(url=i['url'])
                    kw.movieInfomation.add(movie)

                # kw = MovieKeyword.objects.get(keyword=keyword)
                # info_list = kw.movieInfomation.all()
                # all_list = []
                # redis_list = []
                # for item in info_list:
                #     data_dict = {}
                #     data_dict['name'] = item.name
                #     data_dict['director'] = item.director
                #     data_dict['actor'] = item.actor
                #     data_dict['releasetime'] = item.releasetime
                #     data_dict['download_count'] = item.download_count
                #     data_dict['star_one'] = item.star_one
                #     data_dict['star_two'] = item.star_two
                #     data_dict['star_three'] = item.star_three
                #     data_dict['star_four'] = item.star_four
                #     data_dict['star_five'] = item.star_five
                #     data_dict['star_avg'] = item.star_avg
                #     data_dict['url'] = item.url
                #     all_list.append(data_dict)
                    # info = [str(item.name),
                    #         str(item.director),
                    #         str(item.actor),
                    #         str(item.releasetime),
                    #         str(item.download_count),
                    #         str(item.star_one),
                    #         str(item.star_two),
                    #         str(item.star_three),
                    #         str(item.star_four),
                    #         str(item.star_five),
                    #         str(item.star_avg),
                    #         str(item.url)]
                    # res = ','.join(info)
                    # redis_list.append(res)
                # keep_time = 60 * 60 *24
                # r.lpush(keyword, redis_list)
                # r.expire(keyword,random.randint(keep_time,2*keep_time))

                result = {
                    'code': 200,
                    'data': all_list
                }
                # result = {'code':20000,
                #           'error':'暂无资源'}

                return JsonResponse(result)











    # if request.method=='GET':
    #     keyword=request.GET.get('keyword')
    #     r = redis.Redis('127.0.0.1', 6379, db=4)
    #     #如果没有输入关键字,返回榜单
    #     # if not keyword:
    #     #     result = {}
    #     #     return JsonResponse(result)
    #
    #     #如果缓存有数据,返回data
    #     if r.exists(keyword):
    #         # 取出所有的数据,data_list=[]
    #         data_list=r.lrange(keyword,0,-1)
    #         all_list=[]
    #         for data in data_list:
    #             data=data.decode()
    #             data_dict = {}
    #             name=data.split(',')[1]
    #             director=data.split(',')[2]
    #             actor=data.split(',')[3]
    #             download_count = data.split(',')[4]
    #             star_one = data.split(',')[5]
    #             star_two = data.split(',')[6]
    #             star_three = data.split(',')[7]
    #             star_four = data.split(',')[8]
    #             star_five = data.split(',')[9]
    #             stat_avg = data.split(',')[10]
    #             url = data.split(',')[11]
    #
    #             data_dict['name'] = name
    #             data_dict['director'] =director
    #             data_dict['actor'] = actor
    #             data_dict['download_count'] = download_count
    #             data_dict['star_one'] = star_one
    #             data_dict['star_two'] = star_two
    #             data_dict['star_three'] = star_three
    #             data_dict['star_four'] = star_four
    #             data_dict['star_five'] = star_five
    #             data_dict['star_avg'] = stat_avg
    #             data_dict['url'] = url
    #
    #             all_list.append(data_dict)
    #         result = {
    #             'code':200,
    #             'data':all_list
    #         }
    #         return JsonResponse(result)
    #     else:
    #         #去数据库查找
    #         try:
    #             kw=MovieKeyword.objects.get(keyword=keyword).movieInfomation.all()
    #             print('qqqqqqqqqqqqqqqqqqqqqqqqqqqq')
    #             print('kw',kw)
    #             all_list = []
    #             redis_list=[]
    #             for i in kw:
    #                 data_dict = {}
    #                 data_dict['name']=i.name
    #                 data_dict['director'] = i.director
    #                 data_dict['actor'] = i.actor
    #                 data_dict['download_count'] = i.download_count
    #                 data_dict['star_one'] = i.star_one
    #                 data_dict['star_two'] = i.star_two
    #                 data_dict['star_three'] = i.star_three
    #                 data_dict['star_four'] = i.star_four
    #                 data_dict['star_five'] = i.star_five
    #                 data_dict['star_avg'] = i.stat_avg
    #                 data_dict['url'] = i.url
    #
    #                 all_list.append(data_dict)
    #                 # 加近redis
    #                 info=[
    #                     str(i.name),
    #                     str(i.director),
    #                     str(i.actor),
    #                     str(i.download_count),
    #                     str(i.star_one),
    #                     str(i.star_two),
    #                     str(i.star_three),
    #                     str(i.star_four),
    #                     str(i.star_five),
    #                     str(i.stat_avg),
    #                     str(i.url)]
    #                 res=','.join(info)
    #                 redis_list.append(res)
    #             r.lpush(keyword,redis_list)
    #
    #             #返回data
    #             result = {'code': 200, 'data':all_list}
    #             return JsonResponse(result)








            # except Exception as e:
            #     print('关键字表没有字段')
            #     #交给爬虫借口,爬到数据多对多加载到数据库中
            #     data={}
            #     #data=['','','']
            #     kw = MovieKeyword.objects.create(keyword=keyword)
            #     for i in data['data']:
            #
            #         movie=MovieInfomation.objects.create(name=i.split(','))
            #         print(keyword)
            #         kw.movieInfomation.add(movie)
            #     result={'code':200,'data':{'a':'q'}}
            #     return JsonResponse(result)




#     else:
#         result={'code':40000,'error':'pls GET request'}
#         return JsonResponse(result)
#
# #爬虫返回数据（没点搜索）
# def get_keylist():
#     pass






