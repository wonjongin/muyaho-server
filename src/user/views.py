from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from user.models import Keyword, Scrap, Notification, AlarmSettings
from notice.models import Notice
from django.views.decorators.csrf import csrf_exempt
import json

#notification이랑 notice relation하기

def test(request):
    return HttpResponse("Hello")

#info
@csrf_exempt
def myinfo(request):
    if request.method == "GET": 
        user = request.user
        return JsonResponse({'email': user.email, 'password': user.password})

    elif request.method == "PATCH":
        return HttpResponse("Hello")

#keyword
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
def edit_keywords(request,num):
    if request.method == "PATCH":
        thisuser = request.user
        data = json.loads(request.body)
        keyword = Keyword.objects.get(id = num)
        if keyword.user == thisuser:
            keyword.title = data.get('title', keyword.title)
            keyword.save()
            return JsonResponse({'mykeywords': keyword.title})
        else:
            return JsonResponse({"message": "Unauthorized"}, status=401)

@csrf_exempt
def delete_keywords(request, num):
    if request.method == "DELETE":
        thisuser = request.user
        keyword = Keyword.objects.get(id = num)
        if keyword.user == thisuser:
            keyword.delete()
            return JsonResponse({"message": "Success!"})
        else:
            return JsonResponse({"message": "Fail..."}, status=401)

#setting
@csrf_exempt
def my_alarmsettings(request): #설정한 알림의 목록
    if request.method == "GET":
        thisuser = request.user
        alarms = AlarmSettings.objects.filter(user=thisuser).values()
        return JsonResponse(list(alarms), safe=False)
        
@csrf_exempt
def my_alarmsetting(request, num):
    if request.method == "GET":
        thisuser = request.user
        alarms = AlarmSettings.objects.get(id=num, user=thisuser)
        return JsonResponse({
            'keyword': alarms.keyword,
            'alarm_date': alarms.alram_date.isoformat(),
            'alarm_days': alarms.alarm_days
        })

@csrf_exempt
def create_alarmsettings(request):
    if request.method == "POST":
        thisuser = request.user
        data = json.loads(request.body)
        alarms = AlarmSettings(
            keyword = data['keyword'],
            alarm_date = data['alarm_date'],
            alarm_days = data['alarm_days'],
            user = thisuser
        )
        alarms.save()
        return JsonResponse({
            'keyword': alarms.keyword,
            'alarm_date': alarms.alarm_date,
            'alarm_days': alarms.alarm_days
        })

@csrf_exempt
def edit_alarmsettings(request, num):
    if request.method == "PATCH":
        thisuser = request.user
        data = json.loads(request.body)
        alarms = AlarmSettings.objects.get(id=num)
        if  alarms.user == thisuser:
            alarms.keyword = data.get('keyword', alarms.keyword)
            alarms.alarm_date = data.get('alarm_date', alarms.alarm_date)
            alarms.alarm_days = data.get('remind_date', alarms.alarm_days)
            alarms.save()
            return JsonResponse({
                'keyword': alarms.keyword,
                'alarm_date': alarms.alarm_date,
                'alarm_days': alarms.alarm_days
            })
        else:
            return JsonResponse({"message": "Unauthorized"}, status=401)

@csrf_exempt
def delete_alarmsettings(request, num):
    if request.method == "DELETE":
        thisuser = request.user
        alarms = AlarmSettings.objects.get(id=num)
        if  alarms.user == thisuser:
            alarms.delete()
            return JsonResponse({"message": "Success!"})
        else:
            return JsonResponse({"message": "Fail..."}, status=401)

#notification  
@csrf_exempt
def my_notifications(request): #알림설정한 걸 통해서 온 알림의 목록
    if request.method == "GET":
        thisuser = request.user
        notifications = Notification.objects.filter(user=thisuser).values('id', 'keyword', 'title', 'description', 'remind_date')
        res = []
        for r in notifications:
            res.append({
                'title': r.title,
                'id': r.id,
                'keyword': r.keyword,
                'description': r.description,
                'remind_date': r.remind.date,
                'notice_id': r.notice.id
            })
        # notice = Notice.objects.filter(id=notifications.notice.id)
        return JsonResponse(res, safe=False)

@csrf_exempt
def my_notification(request):
    if request.method == "GET":
        thisuser = request.user
        alarms = Notification.objects.filter(user=thisuser).values()
        return JsonResponse(list(alarms), safe=False)

@csrf_exempt
def delete_notifications(request, num):
    if request.method == "DELETE":
        thisuser = request.user
        
#scrap
@csrf_exempt
def my_scraps(request):
    if request.method == "GET":
        thisuser = request.user
        scraps = Scrap.objects.filter(user=thisuser)
        # return JsonResponse(list(scrap), safe=False)
        res = []
        for scrap in scraps:
            res.append({
                'id': scrap.notice.id,
                'title':scrap.notice.title,
                'description': scrap.notice.description,
                'notitype': str(scrap.notice.notitype) ,
                'url': scrap.notice.url,
                'date': scrap.notice.date
                })
        return JsonResponse(res, safe=False)

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
