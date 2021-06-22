from django.urls import path
from . import views


urlpatterns = [
    path('', views.administrator_dashbord ),
    path('new_user', views.new_user),
    path('delete_user/<int:user_id>', views.delete_user),



]