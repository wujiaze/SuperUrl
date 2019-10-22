import datetime
import hashlib
import json
import time

import jwt
from django.http import *

# Create your views here.
from tools import mysettings
from user.models import UserProfile


# 登录
def tokens(request):
    if request.method != 'POST':
        code = 201
        error = '请求方式并非 POST'
        return JsonResponse({'code': code, 'error': error})
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
        username = json_obj['username']
        password = json_obj['password']
    except Exception as e:
        code = 210
        error = '请求关键字缺失'
        return JsonResponse({'code': code, 'error': error})

    if not username:
        code = 203
        error = '请求中未提交用户名'
        return JsonResponse({'code': code, 'error': error})
    if not password:
        code = 205
        error = '请求中未提交密码'
        return JsonResponse({'code': code, 'error': error})

    old_user = UserProfile.objects.filter(username=username)
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
    token = make_token(old_user[0])
    code = 200
    data = {"token": token}
    return JsonResponse({'code': code, 'username': username, 'data': data})


def make_token(user: UserProfile, expire=3600 * 24):
    login_datetime = datetime.datetime.now()
    # 修改token
    login_time = time.mktime(login_datetime.timetuple())
    # 修改数据库
    user.login_time = login_datetime
    user.save()
    # 一般使用 用户名/登录时间 来生成token,用来校对
    payload = {'username': user.username, 'exp': login_time + expire, 'login_time': login_time}
    return jwt.encode(payload, mysettings.Token_key, algorithm='HS256').decode()
