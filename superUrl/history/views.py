from django.http import JsonResponse
from django.shortcuts import render

from tools.logincheck import get_user_by_request
from user.models import UserProfile
from history.models import History


# Create your views here.


def get_history(request):
    if request.method == 'GET':
        # phonenumber = nickname
        user = get_user_by_request(request)
        if not user:
            res = {
                'code': 20000,
                'error': 'no token'
            }
            return JsonResponse(res)

        history_list = user.history_set.all()
        res_list = []
        for item in history_list:
            res_list.append(item.keyword)

        res = {
            'code': 200,
            'data': res_list
        }
        return JsonResponse(res)
    return JsonResponse({'code': 20000, 'error': 'not get'})


def save_history(request, type):
    user = get_user_by_request(request)

    if not user:
        return None

    keyword = request.GET.get('keyword')

    history_list = user.history_set.all()  # jquery容器
    length = len(history_list)
    if length > 15:
        history_list = history_list[length - 15:]
    for item in history_list:
        if item.objects.keyword == keyword:
            item.delete()
            break
    history = History.objects.create(keyword=keyword, userprofile=user)
