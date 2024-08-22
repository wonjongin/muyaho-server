from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.db.models import Q
from user.models import Scrap
from notice.models import Notice
from django.views.decorators.csrf import csrf_exempt
import json
import datetime

#notificcation이랑 notice relation하기
@csrf_exempt
def notices(request):
    if request.method == "GET":
        notices = Notice.objects
        return JsonResponse({'notice_id': notices.notice.id, 'title': notices.notice.title})
    
@csrf_exempt
def notice(request, num):
    if request.method == "GET":
        thisuser = request.user
        notice = Notice.objects.get(id=num)
        is_scrapped = Scrap.objects.exists(id=num, user=thisuser)
        return JsonResponse({**notice, 'is_scrapped': is_scrapped}, safe=False)

@csrf_exempt
def notitypes(request, type):
    if request.method == "GET":
        notices = Notice.objects.filter(notitype=type)
        return JsonResponse({'notice_id': notices.notice.id, 'title': notices.notice.title})
    
@csrf_exempt
def searches(request, query):
    if request.method == "GET": 
        querys = query.split(" ")
        cont = Q()
        excl = Q()
        for q in querys:
            if q.startswith("-"):
                excl |= Q(tdindex = q)
            else:
                cont &= Q(tdindex = q)
            
        search = Notice.objects.filter(cont).exclude(excl).values('id', 'title', 'description', 'notitype')
         #제목이나 내용이 query를 가지고 있으며, ex_query를 가지고 있지 않다.
        return JsonResponse(list(search), safe=False)

@csrf_exempt
def dates(request, query, fromdate):
    if request.method == "GET":
        querys = query.split(" ")
        cont = Q()
        excl = Q()
        for q in querys:
            if q.startswith("-"):
                excl |= Q(tdindex = q)
            else:
                cont &= Q(tdindex = q)
        fromdate_list = list(fromdate.split('-'))
        notice = Notice.objects.filter(
            cont, 
            date__gte=datetime.date(
                fromdate_list[0], fromdate_list[1], fromdate_list[2])
            ).exclude(excl).values('id', 'title', 'description', 'notitype')
        return JsonResponse(list(notice), safe=False)


    