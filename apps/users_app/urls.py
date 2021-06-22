from django.urls import path
from . import views


urlpatterns = [
    path('', views.index ),
    path('make_administrator', views.make_administrator ),
    path('login_administrator', views.login_administrator ),
    path('login_user', views.login_user ),
    path('makedata', views.makedata ),
    path('logout', views.logout ),



]