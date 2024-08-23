from django.urls import path, include
from . import views

urlpatterns = [
    path('test/', views.test),
    path('myInfo/', views.myinfo),
    path('myKeywords/', views.my_keywords),
    path('editKeywords/<int:num>', views.edit_keywords),
    path('deleteKeywords/<int:num>', views.delete_keywords)
]
