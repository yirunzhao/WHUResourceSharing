from django.urls import path

from . import views

# app_name = 'download'
urlpatterns = [
    # path('', views.download_main, name='download'),
    path('<std_id>/',views.download_user, name = 'download_user'),
    # path('<user>/<uid>',views.download,name = "dld"),
    path('<catagory>/<file_id>/',views.download_detail,name='download_detail'),
    path('test/',views.add_file)
]