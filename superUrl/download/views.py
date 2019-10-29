from django.http import JsonResponse
from django.shortcuts import render
from music.models import MusicInformation
from movie.models import MovieInfomation
from django.db.models import F


# Create your views here.
from picture.models import PictureInformation


def add_download(request):
    if request.method == 'GET':
        type = request.GET.get('type')
        url = request.GET.get('url')

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
        try:
            res = MusicInformation.objects.get(url=url)
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
        try:
            res = MovieInfomation.objects.get(url=url)
        except Exception as e:
            res = {
                'code': 20000,
                'error': '错误'
            }
            return JsonResponse(res)
    elif type == 'picture':
        try:
            item = PictureInformation.objects.filter(url=url).update(download_count=F('download_count')+1)
        except Exception as e:
            res = {
                'code':20000,
                'error':'错误'
            }
            return JsonResponse(res)
        try:
            res = PictureInformation.objects.get(url=url)
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

    count = res.download_count
    res = {
        'code': 200,
        'count': count
    }
    return JsonResponse(res)
