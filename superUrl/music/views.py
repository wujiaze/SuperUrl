import redis
from django.http import JsonResponse
from django.shortcuts import render
from music.models import MusicInformation,MusicKeyword
# Create your views here.



def search_music(request):
    if request.method == 'GET':
        print('进入get')
        keyword = request.GET.get('keyword')
        print(keyword)

        r = redis.Redis(host='127.0.0.1', port=6379, db=2)

        if r.exists(keyword):
            data_list = r.lrange(keyword,0,-1)
            all_list = []
            for data in data_list:
                data_dict = {}
                data = data.decode()
                name = data.split(',')[1]
                download_count = data.split(',')[2]
                star_one = data.split(',')[3]
                star_two = data.split(',')[4]
                star_three = data.split(',')[5]
                star_four = data.split(',')[6]
                star_five = data.split(',')[7]
                stat_avg = data.split(',')[8]
                url = data.split(',')[9]
                data_dict['name'] = name
                data_dict['download_count'] = download_count
                data_dict['star_one'] = star_one
                data_dict['star_two'] = star_two
                data_dict['star_three'] = star_three
                data_dict['star_four'] = star_four
                data_dict['star_five'] = star_five
                data_dict['star_avg'] = stat_avg
                data_dict['url'] = url
                data_list.append(data_dict)

            res = {
                'code':200,
                'data':all_list
            }

            return JsonResponse(res)


        else:
            try:
                kw = MusicKeyword.objects.get(keyword=keyword)
                info_list = kw.musicinformation.all()
                all_list = []
                redis_list = []
                for item in info_list:
                    data_dict = {}
                    data_dict['name'] = item.name
                    data_dict['download_count'] = item.download_count
                    data_dict['star_one'] = item.star_one
                    data_dict['star_two'] = item.star_two
                    data_dict['star_three'] = item.star_three
                    data_dict['star_four'] = item.star_four
                    data_dict['star_five'] = item.star_five
                    data_dict['star_avg'] = item.stat_avg
                    data_dict['url'] = item.url
                    all_list.append(data_dict)
                    info = [str(item.name),
                            str(item.download_count),
                            str(item.star_one),
                            str(item.star_two),
                            str(item.star_three),
                            str(item.star_four),
                            str(item.star_five),
                            str(item.stat_avg),
                            str(item.url)]
                    res = ','.join(info)
                    redis_list.append(res)
                r.lpush(keyword,redis_list)

                #res = r.lrange(keyword,0,-1)  ->  [b"['aaaa', 'bbbbbb', 'cccccccc']"]
                #type(res)  -> list
                #res[0].decode()   ->    str

                result = {
                    'code': 200,
                    'data': all_list
                }

                return JsonResponse(result)



            except Exception as e:
                pass
            #todo 爬虫接口
            #  得到　　data

                data = {}
                try:
                    kw = MusicKeyword.objects.create(keyword=keyword)
                except Exception as e:
                    print('已经存在关键字')
                    return JsonResponse({'code':20000,'error':'稍后访问'})
                for i in data:
                    try:
                        movie = MusicInformation.objects.create(name=i['name'],url=i['url'])
                    except Exception as e:
                        movie = MusicInformation.objects.get(url=i['url'])
                    kw.musicinformation.add(movie)

                kw = MusicKeyword.objects.get(keyword=keyword)
                info_list = kw.musicinformation.all()
                all_list = []
                redis_list = []
                for item in info_list:
                    data_dict = {}
                    data_dict['name'] = item.name
                    data_dict['download_count'] = item.download_count
                    data_dict['star_one'] = item.star_one
                    data_dict['star_two'] = item.star_two
                    data_dict['star_three'] = item.star_three
                    data_dict['star_four'] = item.star_four
                    data_dict['star_five'] = item.star_five
                    data_dict['star_avg'] = item.stat_avg
                    data_dict['url'] = item.url
                    all_list.append(data_dict)
                    info = [str(item.name),
                            str(item.download_count),
                            str(item.star_one),
                            str(item.star_two),
                            str(item.star_three),
                            str(item.star_four),
                            str(item.star_five),
                            str(item.stat_avg),
                            str(item.url)]
                    res = ','.join(info)
                    redis_list.append(res)
                r.lpush(keyword, redis_list)

                result = {
                    'code': 200,
                    'data': all_list
                }

                return JsonResponse(result)






def get_history(request):
    pass




def add_download(request):
    pass




def get_rank(request):
    pass



def get_keylist(request):

    # todo 爬虫接口
    # 调用爬虫接口获取实时keylist

    pass



