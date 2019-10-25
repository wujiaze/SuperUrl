from django.shortcuts import render

from comment.models import Comment
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




                # result={'code':200,'data':'type错误'}
                # return JsonResponse(result)


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

