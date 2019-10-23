from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.



def search_music(request):
    if request.method == 'GET':
        operation = request.GET.get('operation')
        keyword = request.GET.get('keyword')
        print(operation)
        print(keyword)
        if operation == 0:
            #todo 爬虫接口
            pass
        elif operation == 1:




            return JsonResponse({'code':200})



