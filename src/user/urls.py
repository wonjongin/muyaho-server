from django.urls import path, include
from . import views

urlpatterns = [
    path('test/', views.test),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('myInfo/', views.myinfo),
    path('myKeywords/', views.my_keywords),
    path('myScraps/', views.my_scraps),
    path('addScrap/', views.add_scrap),
    path('deleteScrap/<int:num>', views.delete_scrap)
]
