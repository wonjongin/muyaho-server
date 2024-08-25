from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.db.models import Q
from user.models import Scrap
from notice.models import Notice
from django.views.decorators.csrf import csrf_exempt
import json
import datetime

@csrf_exempt
def notices(request):
    if request.method == "GET":
        notices = Notice.objects.all().values('id', 'title')
        return JsonResponse(list(notices), safe=False)
    
@csrf_exempt
def notice(request, num):
    if request.method == "GET":
        thisuser = request.user
        notice = Notice.objects.get(id=num)
        is_scrapped = Scrap.objects.filter(notice=notice, user=thisuser).exists()
        return JsonResponse({ 
            'id': notice.id ,
            'title': notice.title,
            'description': notice.description,
            'notitype': notice.notitype,
            'date': notice.date,
            'tdindex': notice.tdindex,
            'notice_id': notice.notice_id,
            'is_scrapped': is_scrapped,
            }, safe=False)
        # return JsonResponse(notice, safe=False)
@csrf_exempt
def notitypes(request, type):
    if request.method == "GET":
        notices = Notice.objects.filter(notitype=type).values('id', 'title')
        return JsonResponse(list(notices), safe=False)
    
@csrf_exempt
def searches(request, query):
    if request.method == "GET": 
        querys = query.split(" ")
        print(querys)
        cont = Q()
        excl = Q()
        for q in querys:
            if q.startswith("-"):
                new_q = q[1:]
                excl |= Q(tdindex__contains = new_q)
            else:
                cont &= Q(tdindex__contains = q)
            
        search = Notice.objects.filter(cont).exclude(excl).values('id', 'title', 'description', 'notitype')

        # search = Notice.objects.filter(tdindex__in=querys).values('id', 'title', 'description', 'notitype')
        #제목이나 내용이 query를 가지고 있으며, ex_query를 가지고 있지 않다.
        return JsonResponse(list(search), safe=False)

@csrf_exempt
def s_type(request, query, type):
    if request.method == "GET":
        querys = query.split(" ")
        cont = Q()
        excl = Q()
        for q in querys:
            if q.startswith("-"):
                new_q = q[1:]
                excl |= Q(tdindex__contains = new_q)
            else:
                cont &= Q(tdindex__contains = q)

        notices = Notice.objects.filter(cont, notitype=type).exclude(excl).values('id', 'title', 'description', 'notitype')
        return JsonResponse(list(notices), safe=False)

@csrf_exempt
def dates(request, query, fromdate):
    if request.method == "GET":
        querys = query.split(" ")
        cont = Q()
        excl = Q()
        for q in querys:
            if q.startswith("-"):
                new_q = q[1:]
                excl |= Q(tdindex__contains = new_q)
            else:
                cont &= Q(tdindex__contains = q)
        fromdate_list = list(fromdate.split('-'))
        notice = Notice.objects.filter(
            cont, 
            date__gte=datetime.date(
                int(fromdate_list[0]), int(fromdate_list[1]), int(fromdate_list[2]))
            ).exclude(excl).values('id', 'title', 'description', 'notitype')
        return JsonResponse(list(notice), safe=False)


    