from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('create_lawsuit',views.create_lawsuit),
    path('delete_lawsuit/<int:id_lawsuit>',views.delete_lawsuit),
    path('lawsuit_detail/<int:id_lawsuit>',views.lawsuit_detail),
    path('lawsuit_detail/re_make_lawsuitpdf/<int:id_lawsuit>',views.re_make_lawsuitpdf),
    path('lawsuit_detail/update_lawsuit_state/<int:id_lawsuit>',views.update_lawsuit_state),
    path('lawsuit_detail/update_lawsuit_court/<int:id_lawsuit>',views.update_lawsuit_court),
]