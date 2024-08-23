from django.urls import path, include
from . import views

urlpatterns = [
    path('test/', views.test),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('myInfo/', views.myinfo),
    path('myKeywords/', views.my_keywords),
    path('editKeywords/<int:num>', views.edit_keywords),
    path('deleteKeywords/<int:num>', views.delete_keywords),
    path('myNotifications/', views.my_notifications),
    path('myAlarmSettings/', views.my_alarmsettings),
    path('myAlarmsetting/<int:num>', views.my_alarmsetting),
    path('createAlarmsettings/', views.create_alarmsettings),
    path('editAlarmsettings/<int:num>', views.edit_alarmsettings),
    path('deleteAlarmsettings/<int:num>', views.delete_alarmsettings),
    path('myScraps/', views.my_scraps),
    path('addScrap/', views.add_scrap),
    path('deleteScrap/<int:num>', views.delete_scrap)
]
