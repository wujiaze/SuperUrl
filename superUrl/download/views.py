from django.http import JsonResponse
from django.shortcuts import render
from music.models import MusicInformation
from movie.models import MovieInfomation
from django.db.models import F


# Create your views here.


def add_download(request):
    if request.method == 'POST':
        type = request.POST.get('type')
        url = request.POST.get('url')
    else:
        res = {
            'code': 20000,
            'error': '错误'
        }
        return JsonResponse(res)

    if type == 'music':
        try:
            item = MusicInformation.objects.filter(url=url).update(download_count=F('download_count') + 1)
        except Exception as e:
            res = {
                'code': 20000,
                'error': '错误'
            }
            return JsonResponse(res)
    elif type == 'movie':
        try:
            item = MovieInfomation.objects.filter(url=url).update(download_count=F('download_count') + 1)
        except Exception as e:
            res = {
                'code': 20000,
                'error': '错误'
            }
            return JsonResponse(res)
    else:
        res = {
            'code': 20000,
            'error': '错误'
        }
        return JsonResponse(res)

    count = item.download_count
    res = {
        'code': 200,
        'count': count
    }
    return JsonResponse(res)
