from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from user.models import Keyword, Search, Scrap
from notice.models import Notice
from django.views.decorators.csrf import csrf_exempt
import json


def test(request):
    return HttpResponse("Hello")

@csrf_exempt
def myinfo(request):
    if request.method == "GET":
        user = request.user
        return JsonResponse({'email': user.email, 'password': user.password})

    elif request.method == "PATCH":
        return HttpResponse("Hello")
    
@csrf_exempt
def my_keywords(request):
    if request.method == "GET":
        thisuser = request.user
        keywords = Keyword.objects.filter(user = thisuser).values()
        # res_json = serializers.serialize('json', keywords)
        return JsonResponse(list(keywords), safe=False)
    elif request.method == "POST":
        thisuser = request.user
        data = json.loads(request.body)
        keyword = Keyword(title= data['title'], user= thisuser)
        keyword.save()
        return JsonResponse({'title': keyword.title, 'user_id': keyword.user.id})
    
@csrf_exempt
def my_scraps(request):
    if request.method == "GET":
        thisuser = request.user
        scrap = scrap.object.filter(user=thisuser).values()
        return JsonResponse(list(scrap), safe=False)

@csrf_exempt
def add_scrap(request):
    if request.method == "POST":
        thisuser = request.user
        data = json.loads(request.body)
        notice = Notice.objects.get(id = data['notice_id'])
        scrap = Scrap(notice=notice, user=thisuser)
        scrap.save()
        return JsonResponse({'notice_id': scrap.notice.id, 'title': scrap.notice.title})

@csrf_exempt
def delete_scrap(request, num):
    if request.method == "DELETE":
        thisuser = request.user
        scrap = Scrap.objects.get(id = num)
        if scrap.user == thisuser:
            scrap.delete()
            return JsonResponse({"message": "Success!"})
        else:
            return JsonResponse({"message": "Fail..."}, status=401) 
        
