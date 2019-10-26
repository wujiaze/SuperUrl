import hashlib
import json

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from btoken.views import make_token
from tools import mysettings
from tools.logincheck import login_check, get_user_by_request
from user.models import UserProfile


@login_check('POST')
def avatar(request, username):
    if request.method != 'POST':
        code = 10203
        error = '请求方式不对'
        return JsonResponse({'code': code, 'error': error})
    if request.method == "POST":
        # user 由装饰器提供
        user = request.user
        if user.username != username:
            code = 10205
            error = '不可修改他人用户名'
            return JsonResponse({'code': code, 'error': error})
        try:
            # <class 'django.core.files.uploadedfile.InMemoryUploadedFile'>
            avatar = request.FILES['avatar']
        except Exception as e:
            code = 10206
            error = 'no avatar'
            return JsonResponse({'code': code, 'error': error})

        # <class 'django.db.models.fields.files.ImageFieldFile'>
        # InMemoryUploadedFile 可以赋给 ImageFieldFile
        user.avatar = avatar
        user.save()
        code = 200
        return JsonResponse({'code': code, 'username': username})


def register(request):
    if request.method == 'GET':
        return render(request, 'user/register.html')
    if request.method == 'POST':
        # 创建资源 创建用户
        # 注册成功/直接登录  签发token[1天]
        # 用户模块状态吗 10100 开始 / 200为正常响应
        # {'code':200/101xx,'data':xxx,'error':xxx}
        print(request.body)
        try:
            json_obj = json.loads(request.body.decode())
            # 校验数据
            phonenumber = json_obj['phonenumber']
            nickname = json_obj['nickname']
            password = json_obj['password']
            authcode = json_obj['authcode']
        except Exception as e:
            print("user/POST/try1/", e)
            code = 10100
            error = "注册数据有问题"
            return JsonResponse({'code': code, 'error': error})

        if not phonenumber:
            code = 10101
            error = "请输入手机号"
            return JsonResponse({'code': code, 'error': error})
        if not nickname:
            code = 10102
            error = "请输入昵称"
            return JsonResponse({'code': code, 'error': error})
        if not password:
            code = 205
            error = "请输入密码"
            return JsonResponse({'code': code, 'error': error})
        if len(phonenumber) != 11:
            code = 208
            error = "请输入正确的手机号"
            return JsonResponse({'code': code, 'error': error})

        older_user = UserProfile.objects.filter(phonenumber=phonenumber)
        if older_user:
            code = 207
            error = "用户名已存在"
            return JsonResponse({'code': code, 'error': error})

        p_m = hashlib.md5(mysettings.Token_key)
        p_m.update(password.encode())
        try:
            new_user = UserProfile.objects.create(phonenumber=phonenumber, nickname=nickname,
                                                  password=p_m.hexdigest())
        except Exception as e:
            print("user/POST/create/", e)
            code = 207
            error = "用户名已存在"
            return JsonResponse({'code': code, 'error': error})

        token = make_token(new_user)
        code = 200
        data = {"token": token}
        return JsonResponse({'code': code, 'phonenumber': phonenumber, 'data': data})


def login(request):
    if request.method == 'GET':
        return render(request, 'user/login.html')
    elif request.method == 'POST':
        if not request.body:
            code = 202
            error = '请求为空'
            return JsonResponse({'code': code, 'error': error})
        try:
            json_obj = json.loads(request.body.decode())
        except Exception as e:
            code = ''
            error = ''
            return JsonResponse({'code': code, 'error': error})
        try:
            phonenumber = json_obj['phonenumber']
            password = json_obj['password']
            checked = json_obj.get('checked')
        except Exception as e:
            code = 210
            error = '请求关键字缺失'
            return JsonResponse({'code': code, 'error': error})

        if not phonenumber:
            code = 203
            error = '请求中未提交用户名'
            return JsonResponse({'code': code, 'error': error})
        if not password:
            code = 205
            error = '请求中未提交密码'
            return JsonResponse({'code': code, 'error': error})

        old_user = UserProfile.objects.filter(phonenumber=phonenumber)
        if not old_user:
            code = 208
            error = '用户名不存在'
            return JsonResponse({'code': code, 'error': error})

        p_m = hashlib.md5(mysettings.Token_key)
        p_m.update(password.encode())

        if old_user[0].password != p_m.hexdigest():
            code = 209
            error = '提交的密码不正确'
            return JsonResponse({'code': code, 'error': error})

        # 登录成功
        expire = 7 * 3600 * 24 if checked else 3600 * 24
        token = make_token(old_user[0], expire)
        code = 200
        data = {"token": token}
        return JsonResponse({'code': code, 'phonenumber': old_user[0].phonenumber, 'data': data})


def information(request):
    if request.method == "GET":
        # 软性判断是否登录
        user = get_user_by_request(request)
        if not user:
            return JsonResponse({'code': 1, 'error': "没有登录"})
        code = 200
        data = {
            'nickname': user.nickname,
            'avatar': user.avatar.name,
        }
        return JsonResponse({'code': code, 'phonenumber': user.phonenumber, 'data': data})
