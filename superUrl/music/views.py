from django.shortcuts import render

# Create your views here.



def search_music(request):
    if request.method == 'GET':
        operation = request.GET.get('operation')
        keyword = request.GET.get('keyword')
        



