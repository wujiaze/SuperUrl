from django.shortcuts import render
from django.db.models import F
from comment.models import Comment
from movie.models import MovieInfomation
from tools.logincheck import login_check
from django.http import JsonResponse
import json

# Create your views here.
from user.models import UserProfile


@login_check('POST')
def get_comment(request):
    #提交评论
    if request.method=='POST':
        # 在token中获取phonenumber
        user = request.user
        if not user:
            result = {'code':20000,'data':'error'}
            return JsonResponse(result)


        json_str=request.body
        if not json_str:
            result = {'code':20000,'data':'error'}
            return JsonResponse(result)

        json_obj=json.loads(json_str)
        url=json_obj.get('url','')
        if not url:
            result = {'code':20000,'data':'error'}
            return JsonResponse(result)

        content=json_obj.get('content','')
        if not content:
            result = {'code':20000,'data':'error'}
            return JsonResponse(result)



        # 获取评论星级　如果低于某值　则删除资源，　高于则继续插入
        star_val = json_obj.get('num', '')
        star_val = int(star_val)
        if not star_val:
            result = {'code': 20000, 'data': 'error'}
            return JsonResponse(result)
        try:
            movie = MovieInfomation.objects.get(url=url)
            if star_val == 1:
                movie.update(star_one=F('movie.star_one') + 1)
                movie.save()
            elif star_val == 2:
                movie.update(star_two=F('movie.star_two') + 1)
                movie.save()
            elif star_val == 3:
                movie.update(star_three=F('movie.star_three') + 1)
                movie.save()
            elif star_val == 4:
                movie.update(star_four=F('movie.star_four') + 1)
                movie.save()
            elif star_val == 5:
                movie.update(star_five=F('movie.star_five') + 1)
                movie.save()

            all_star = movie.star_one + movie.star_two + movie.star_three + movie.star_four + movie.star_five
            avg_star = all_star / 5


            # 判断平均星数
            if avg_star < 1.5:
                #删除表记录
                try:
                    movie.delete()
                except Exception as e:
                    print(e)
                    result = {'code': 20000, 'data': 'error'}
                    return JsonResponse(result)



            #修改平均星值
            movie.avg_star=avg_star
            movie.save()


        except Exception as e:
            print('没找到字段')
            result = {'code': 20000, 'data': 'error'}
            return JsonResponse(result)


        #插入评论表
        try:

            Comment.objects.create(url=url,content=content,username=user.phonenumber)
            #返回content和create
            comment=Comment.objects.all(url=url)
            lis=[]
            for i in comment:
                dic = {}
                phonenumber=i.phonenumber
                phone=UserProfile.objects.get(phonenumber=phonenumber)
                print('phone对象是',phone)
                dic['nickname'] = phone.nickname
                dic['avatar'] = phone.avatar
                dic['content']=i.content
                dic['createtime']=i.createtime
                lis.append(dic)

            result = {'code': 200, 'data':lis}
            return JsonResponse(result)


        except Exception as e:
            print(e)
            result = {'code':20000,'data':'error'}
            return JsonResponse(result)

    #获取所有评论内容
    elif request.method=='GET':
        url=request.get('url')
        try:
            l_com=Comment.objects.all(url=url)
            lis=[]
            for com in l_com:
                print('com对象是',com)
                dic = {}
                phonenumber=com.phonenumber
                phone = UserProfile.objects.get(phonenumber=phonenumber)
                dic['nickname'] = phone.nickname
                dic['avatar'] = phone.avatar
                dic['content']=com.content
                dic['createtime']=com.createtime
                lis.append(dic)

            result = {'code': 200, 'data': lis}
            return JsonResponse(result)

        except Exception as e:
            print(e)
            result = {'code':20000,'data':'error'}
            return JsonResponse(result)


