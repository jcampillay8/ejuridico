from django.urls import path
from . import views


urlpatterns = [
    path('', views.index ),
    path('lawsuit_detail/<int:id_lawsuit>',views.lawsuit_detail),
    path('lawsuit_detail/update_lawsuit_state/<int:id_lawsuit>',views.update_lawsuit_state),

]