from django.urls import path

from . import views
urlpatterns = [
    path('',views.download,name='download'),
    path('<catagory>/<file_id>/',views.download_detail,name='download_detail'),
    path('test/',views.add_file)
]