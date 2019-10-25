import datetime
import time

import jwt
from django.http import JsonResponse
from jwt import DecodeError, ExpiredSignatureError

from tools import mysettings
from user.models import UserProfile


# 强硬的登录检测
# 没有就重新登录
def login_check(*methods):
    def warpper1(func):
        def warpper2(request, *args, **kwargs):
            if not methods or request.method not in methods:
                return func(request, *args, **kwargs)
            if request.method in methods:
                # 验证token
                # HTTP_AUTHORIZATION 对应前端的 authorization
                token = request.META.get('HTTP_AUTHORIZATION')
                if not token or token == "null":
                    code = 10206
                    error = 'no token'
                    return JsonResponse({'code': code, 'error': error})
                try:
                    payload = jwt.decode(token, mysettings.Token_key, algorithms='HS256')
                except DecodeError as e:
                    # token出错
                    print(e)
                    code = 10207
                    error = 'Please Login'
                    return JsonResponse({'code': code, 'error': error})
                except ExpiredSignatureError as e:
                    # token时间过期
                    print(e)
                    code = 10217
                    error = 'Please Login'
                    return JsonResponse({'code': code, 'error': error})
                try:
                    # 用token的数据比较安全
                    phonenumber = payload['phonenumber']
                    user = UserProfile.objects.get(phonenumber=phonenumber)
                except Exception as e:
                    print(e)
                    code = 10208
                    error = '用户丢失,重新登录'
                    return JsonResponse({'code': code, 'error': error})

                # 判断是否同一个地方登录
                try:
                    # token中登录时间
                    login_time = payload['login_time']
                except Exception as e:
                    return JsonResponse({'code': 10209, 'error': '没有登录时间'})

                # 判断数据库时间和token登录时间
                now_t = time.mktime(user.login_time.timetuple())
                if now_t != login_time:
                    return JsonResponse({'code': 10210, 'error': '已在其他地方登录'})

                # 覆盖了django自身的user
                # 没有问题，只需要确保后面不使用django的验证即可
                request.user = user
                return func(request, *args, **kwargs)

        return warpper2

    return warpper1


# 不是那么强硬
# 有   返回user  用户
# 没有 返回None  访客
def get_user_by_request(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if not token:
        return None
    try:
        payload = jwt.decode(jwt=token, key=mysettings.Token_key, algorithms='HS256')
    except Exception as e:
        return None

    phonenumber = payload['phonenumber']

    try:
        user = UserProfile.objects.get(phonenumber=phonenumber)
    except Exception as e:
        return None

    return user
