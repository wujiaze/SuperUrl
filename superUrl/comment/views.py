from django.shortcuts import render

from comment.models import Comment
from tools.logincheck import login_check
from django.http import JsonResponse
import json
# Create your views here.

@login_check('POST')
def get_comment(request):
    if request.method=='POST':
        json_str=request.body
        if not json_str:
            result={}
            return JsonResponse(result)

        json_obj=json.loads(json_str)
        url=json_obj.get('url','')
        if not url:
            result = {}
            return JsonResponse(result)

        content=json_obj.get('content','')
        if not content:
            result = {}
            return JsonResponse(result)

        username=json_obj.get('username')
        if not username:
            result = {}
            return JsonResponse(result)
        try:
            Comment.objects.create(url=url,content=content,username=username)
            result={'code':200}
            return JsonResponse(result)
        except Exception as e:
            print(e)
            result = {}
            return JsonResponse(result)


    elif request.method=='GET':
        url=request.get('url')
        try:
            l_com=Comment.objects.all(url=url)
            dic = {}
            for com in l_com:
                dic['content']=com.content
                dic['username']=com.username
                dic['createtime']=com.createtime

            result = {'code': 200, 'data': dic}
            return JsonResponse(result)

        except Exception as e:
            print(e)
            result = {}
            return JsonResponse(result)

