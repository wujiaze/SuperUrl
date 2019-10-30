from django.shortcuts import render
from django.db.models import F
from comment.models import Comment
from movie.models import MovieInfomation
from music.models import MusicInformation
from tools.logincheck import login_check
from django.http import JsonResponse
import json

# Create your views here.
from user.models import UserProfile


@login_check('POST')
def get_comment(request):
    # 提交评论
    if request.method == 'POST':
        # 在token中获取phonenumber
        user = request.user
        if not user:
            result = {'code': 20000, 'data': 'error'}
            return JsonResponse(result)

        json_str = request.body
        if not json_str:
            result = {'code': 20000, 'data': 'error'}
            return JsonResponse(result)

        print(json_str)

        json_obj = json.loads(json_str)

        url = json_obj.get('url', '')
        if not url:
            result = {'code': 20000, 'data': 'error'}
            return JsonResponse(result)

        content = json_obj.get('content', '')
        if not content:
            result = {'code': 20000, 'data': 'error'}
            return JsonResponse(result)

        type = json_obj.get('type', '')
        if not type:
            result = {'code': 20000, 'data': 'error'}
            return JsonResponse(result)

        # 获取评论星级　如果低于某值　则删除资源，　高于则继续插入
        star_val = json_obj.get('num', '')
        star_val = int(star_val)
        if not star_val:
            result = {'code': 20000, 'data': 'error'}
            return JsonResponse(result)

        if type == "music":
            try:
                music = MusicInformation.objects.filter(url=url)
                print(music)
                if star_val == 1:
                    music.update(star_one=F('star_one') + 1)
                elif star_val == 2:
                    music.update(star_two=F('star_two') + 1)
                elif star_val == 3:
                    music.update(star_three=F('star_three') + 1)
                elif star_val == 4:
                    music.update(star_four=F('star_four') + 1)
                elif star_val == 5:
                    music.update(star_five=F('star_five') + 1)

                music = music[0]
                all_star = music.star_one * 1 + \
                           music.star_two * 2 + \
                           music.star_three * 3 + \
                           music.star_four * 4 + \
                           music.star_five * 5 + \
                           music.download_count * 3.5
                all_count = music.star_one + \
                            music.star_two + \
                            music.star_three + \
                            music.star_four + \
                            music.star_five + \
                            music.download_count
                avg_star = all_star / all_count

                # 判断平均星数
                if avg_star < 1.5:
                    # 删除表记录
                    try:
                        music.delete()
                    except Exception as e:
                        print(e)
                        result = {'code': 20000, 'data': 'error'}
                        return JsonResponse(result)
                # 修改平均星值
                music.avg_star = avg_star
                music.save()
            except Exception as e:
                print('没找到字段')
                result = {'code': 20000, 'data': 'error'}
                return JsonResponse(result)

            # 插入评论表
            try:

                Comment.objects.create(url=url, content=content, phonenumber=user.phonenumber)
                # 返回content和create
            except Exception as e:
                print("评论表插入失败")
                pass
            try:
                l_com = Comment.objects.filter(url=url)
                lis = []
                for com in l_com:
                    print('com对象是', com)
                    dic = {}
                    phonenumber = com.phonenumber
                    phone = UserProfile.objects.get(phonenumber=phonenumber)
                    dic['nickname'] = phone.nickname
                    dic['avatar'] = "" if not phone.avatar.name else "/media/" + phone.avatar.name
                    dic['content'] = com.content
                    dic['createtime'] = com.createtime.strftime("%Y-%m-%d %H:%M")
                    lis.append(dic)
                lis.reverse()
                # TODO 查询信息
                if type == "music":
                    try:
                        info = MusicInformation.objects.filter(url=url)[0]
                        print(info)
                    except Exception as e:
                        return JsonResponse({"code": 20000})

                    data = {
                        'code': 200,
                        "messages_count": len(lis),
                        "star_one": info.star_one,
                        "star_two": info.star_two,
                        "star_three": info.star_three,
                        "star_four": info.star_four,
                        "star_five": info.star_five,
                        "star_avg":info.star_avg,
                        "data": lis,
                    }
                    return JsonResponse(data)
                elif type == "movie":
                    pass
                elif type == "picture":
                    pass
            except Exception as e:
                print(e)
                result = {'code': 20000, 'data': 'error'}
                return JsonResponse(result)


    # 获取所有评论内容
    elif request.method == 'GET':
        url = request.GET.get('url')
        type = request.GET.get('type')
        try:
            l_com = Comment.objects.filter(url=url)
            lis = []
            for com in l_com:
                print('com对象是', com)
                dic = {}
                phonenumber = com.phonenumber
                phone = UserProfile.objects.get(phonenumber=phonenumber)
                dic['nickname'] = phone.nickname
                dic['avatar'] = "" if not phone.avatar.name else "/media/" + phone.avatar.name
                dic['content'] = com.content
                dic['createtime'] = com.createtime.strftime("%Y-%m-%d  %H:%M")
                lis.append(dic)
            lis.reverse()
            # TODO 查询信息
            if type == "music":
                try:
                    info = MusicInformation.objects.filter(url=url)[0]
                    print(info)
                except Exception as e:
                    return JsonResponse({"code": 20000})

                data = {
                    'code': 200,
                    "messages_count": len(lis),
                    "star_one": info.star_one,
                    "star_two": info.star_two,
                    "star_three": info.star_three,
                    "star_four": info.star_four,
                    "star_five": info.star_five,
                    "star_avg": info.star_avg,
                    "data": lis,
                }
                return JsonResponse(data)
            elif type == "movie":
                pass
            elif type == "picture":
                pass
        except Exception as e:
            print(e)
            result = {'code': 20000, 'data': 'error'}
            return JsonResponse(result)
