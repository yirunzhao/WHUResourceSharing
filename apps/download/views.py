from django.shortcuts import render
from django.http import HttpResponse
from apps.whursauth.models import Resource


def download(request):
    return render(request, 'download/findresource.html')

def download_detail(request,catagory,file_id):
    return HttpResponse(str(catagory)+'#'*10+str(file_id))

def add_file(request):
    res = Resource(title='sdfsdg',
                   description='dhfdfhdfgsfffqe',
                   download_count=1424,
                   upload_user_id='9Kv24L4VqS7EQiJ6L5J37Z',
                   abs_url='123')
    res.save()
    return HttpResponse('ok')