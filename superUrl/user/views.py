import hashlib
import json

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from btoken.views import make_token
from tools import mysettings
from tools.logincheck import login_check
from user.models import UserProfile


@login_check('PUT')
def users(request, username=None):
    if request.method == 'GET':
        if username:
            # http://127.0.0.1:8000/v1/users/username
            try:
                user = UserProfile.objects.get(username=username)
            except Exception as e:
                code = 208
                error = '用户名不存在'
                return JsonResponse({'code': code, 'error': error})
            if not request.GET.keys():
                # 没有查询字符串,全量查询
                code = 200
                data = {
                    'username': user.username,
                    'nickname': user.nickname,
                    'email': user.email,
                    'sign': user.sign,
                    'info': user.info,
                    'avatar': user.avatar.name,
                }
                return JsonResponse({'code': code, 'username': username, 'data': data})
            else:
                data = {}
                # 有查询字符串
                for key in request.GET.keys():
                    if key in ['password']:
                        continue
                    if hasattr(user, key):
                        value = getattr(user, key)
                        # value = eval('user.%s' % key) # 这个也是可以的
                        data[key] = value
                code = 200
                return JsonResponse({'code': code, 'username': username, 'data': data})
        else:
            print('------全量------')
            # http://127.0.0.1:8000/v1/users
            all_user = UserProfile.objects.all()
            all_data = []
            for u in all_user:
                temp = {'nickname': u.nickname,
                        'email': u.email,
                        'sign': u.sign,
                        'info': u.sign}
                all_data.append(temp)
            code = 200
            return JsonResponse({'code': code, 'username': username, 'data': all_data})
    elif request.method == 'POST':
        # 创建资源 创建用户
        # 注册成功  签发token[1天]
        # 用户模块状态吗 10100 开始 / 200为正常响应
        # {'code':200/101xx,'data':xxx,'error':xxx}
        print(request.body)
        try:
            json_obj = json.loads(request.body.decode())
            # 校验数据
            username = json_obj['username']
            password_1 = json_obj['password_1']
            password_2 = json_obj['password_2']
            email = json_obj['email']
        except Exception as e:
            print("user/POST/try1/", e)
            code = 10100
            error = "json数据有问题"
            return JsonResponse({'code': code, 'error': error})

        if not username:
            code = 10101
            error = "请输入用户名"
            return JsonResponse({'code': code, 'error': error})
        if not email:
            code = 10102
            error = "请求中未提交邮箱"
            return JsonResponse({'code': code, 'error': error})
        if not password_1 or not password_2:
            code = 205
            error = "请求中未提交密码"
            return JsonResponse({'code': code, 'error': error})
        if password_1 != password_2:
            code = 206
            error = "两次提交的密码不一致"
            return JsonResponse({'code': code, 'error': error})
        if len(username) > 11:
            code = 208
            error = "用户名不能超过11位"
            return JsonResponse({'code': code, 'error': error})

        older_user = UserProfile.objects.filter(username=username)
        if older_user:
            code = 207
            error = "用户名已存在"
            return JsonResponse({'code': code, 'error': error})

        p_m = hashlib.md5(mysettings.Token_key)
        p_m.update(password_1.encode())
        try:
            new_user = UserProfile.objects.create(username=username, nickname=username, email=email,
                                                  password=p_m.hexdigest())
        except Exception as e:
            print("user/POST/create/", e)
            code = 207
            error = "用户名已存在"
            return JsonResponse({'code': code, 'error': error})

        token = make_token(new_user)
        code = 200
        data = {"token": token}
        return JsonResponse({'code': code, 'username': username, 'data': data})
    elif request.method == 'PUT':
        # user 由装饰器提供
        user = request.user
        if user.username != username:
            code = 10205
            error = '不可修改他人用户名'
            return JsonResponse({'code': code, 'error': error})
        # 更新资源,需要token
        try:
            json_obj = json.loads(request.body.decode())
        except Exception as e:
            print(e)
            code = 10202
            error = 'Json出错'
            return JsonResponse({'code': code, 'error': error})
        try:
            sign = json_obj['sign']
            info = json_obj['info']
            nickname = json_obj['nickname']
        except Exception as e:
            print(e)
            code = 10203
            error = '空提交'
            return JsonResponse({'code': code, 'error': error})

        # 是否要更新
        if not (user.sign == sign and user.info == info and user.nickname == nickname):
            user.sign = sign
            user.info = info
            user.nickname = nickname
            user.save()
        code = 200
        return JsonResponse({'code': code, 'username': username})


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
