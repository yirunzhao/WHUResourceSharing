from django.urls import path,include
from . import views

app_name = 'base'
urlpatterns = [
    path('login/',views.LoginView.as_view(),name='base_login'),
    path('register/',views.RegisterView.as_view(),name='base_register'),
    path('user/<user_id>/',views.user_page,name='base_user'),
    path('',views.index,name='base_index'),
    path('test/',views.reveive_protrait,name='receive_portrait')
]