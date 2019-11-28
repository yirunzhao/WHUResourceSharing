from django.urls import path,include
from . import views

app_name = 'base'
urlpatterns = [
    path('login/',views.LoginView.as_view(),name='base_login'),
    path('register/',views.RegisterView.as_view(),name='base_register')
    # path('login_in/',views.login_view,name='login')
]