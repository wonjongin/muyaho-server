from django.urls import path, include
from . import views

urlpatterns = [
    path('test/', views.test),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls'))
]
