from django.urls import path, include
from . import views

urlpatterns = [
    path('notices/', views.notices),
    path('notice/<int:num>', views.notice),
    path('notices/notitype/<type>', views.notitypes),
    path('notices/search/<query>', views.searches),
    path('notices/<query>/<type>', views.s_type),
    path('notices/date/<query>/<int:fromdate>', views.dates),
]
