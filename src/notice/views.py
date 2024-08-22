from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from user.models import Search
from notice.models import Notice
from django.views.decorators.csrf import csrf_exempt
import json
import datetime

#search, 스크랩 인지 아닌지 다 들고오기, notificcation이랑 notice relation하기
@csrf_exempt
def notices(request):
    if request.method == "GET":
        notices = Notice.objects
        return JsonResponse(list(notices), safe=False)
    
@csrf_exempt
def notice(request, num):
    if request.method == "GET":
        notice = Notice.objects.get(id=num)
        return JsonResponse(list(notice), safe=False)

@csrf_exempt
def notitypes(request, type):
    if request.method == "GET":
        notices = Notice.objects.filter(notitype=type)
        return JsonResponse(list(notices), safe=False)

@csrf_exempt
def notitype(request, type, num):
    if request.method == "GET":
        notice = Notice.objects.filter(notitype=type, notice_id=num)
        return JsonResponse(list(notice), safe=False)
    
@csrf_exempt
def searches(request):
    if request.method == "GET":
        searcj = Search.object.get(user=thisuser).values()
        return JsonResponse(list(scrap), safe=False)

@csrf_exempt
def search(request):
    if request.method == "GET":
        thisuser = request.user
        data = json.loads(request.body)
        notice = Notice.objects.get(id = data['notice_id'])
        scrap = Scrap(notice=notice, user=thisuser)
        scrap.save()
        return JsonResponse({'notice_id': scrap.notice.id, 'title': scrap.notice.title})

@csrf_exempt
def dates(request, fromdate):
    if request.method == "GET":
        fromdate_list = list(fromdate.split('-'))
        notice = Notice.objects.filter(date__gt=datetime.date(fromdate_list[0], fromdate_list[1], fromdate_list[2]))
        return JsonResponse(list(notice), safe=False)

@csrf_exempt
def date(request, fromdate, num):
    if request.method == "GET":
        fromdate_list = list(fromdate.split('-'))
        notice = Notice.objects.get(date__gt=datetime.date(fromdate_list[0], fromdate_list[1], fromdate_list[2]), id=num)
        return JsonResponse(list(notice), safe=False)
