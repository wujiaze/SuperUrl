from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.



def movie(request):
    if request.method=='GET':
        pass












    else:
        result={'code':40000,'error':'pls GET request'}
        return JsonResponse(result)









