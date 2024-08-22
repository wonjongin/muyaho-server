from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from user.models import Keyword, Scrap, Notification, AlarmSettings
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

@csrf_exempt
def setting_notifications(request): #설정한 알림의 목록
    if request.method == "GET":
        thisuser = request.user
        notifications = AlarmSettings.objects.filter(user=thisuser).values()
        return JsonResponse(list(notifications), safe=False)
    
@csrf_exempt
def my_notifications(request): #알림설정한 걸 통해서 온 알림의 목롬
    if request.method == "GET":
        thisuser = request.user
        notifications = Notification.objects.filter(user=thisuser).values()
        return JsonResponse(list(notifications), safe=False)
        #notice랑 연결
        

@csrf_exempt
def my_notification(request, num):
    if request.method == "GET":
        thisuser = request.user
        notification = Notification.objects.get(id=num, user=thisuser)
        return JsonResponse({
            'title': notification.title,
            'description': notification.description,
            'remind_date': notification.remind_date.isoformat()
        })
@csrf_exempt
def create_notification(request):
    if request.method == "POST":
        thisuser = request.user
        data = json.loads(request.body)
        notification = Notification(
            title = data['title'],
            description = data['description'],
            remind_date = data['remind_date'],
            user = thisuser
        )
        notification.save()
        return JsonResponse({
            'title': notification.title,
            'description': notification.description,
            'remind_date': notification.remind_date
        })

@csrf_exempt
def edit_notification(request, num):
    if request.method == "PATCH":
        thisuser = request.user
        data = json.loads(request.body)
        notification = Notification.objects.get(id=num)
        if notification.user == thisuser:
            notification.title = data.get('title', notification.title)
            notification.description = data.get('description', notification.description)
            notification.remind_date = data.get('remind_date', notification.remind_date)
            notification.save()
            return JsonResponse({
                'title': notification.title,
                'description': notification.description,
                'remind_date': notification.remind_date
            })
        else:
            return JsonResponse({"message": "Unauthorized"}, status=401)

@csrf_exempt
def delete_notification(request, num):
    if request.method == "DELETE":
        thisuser = request.user
        notification = Notification.objects.get(id=num)
        if notification.user == thisuser:
            notification.delete()
            return JsonResponse({"message": "Success!"})
        else:
            return JsonResponse({"message": "Fail..."}, status=401)

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
