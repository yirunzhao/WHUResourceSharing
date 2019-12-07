from django.shortcuts import render
from django.http import HttpResponse

def download(request):
    return render(request, 'download/findresource.html')



def download_detail(request,catagory,file_id):
    return HttpResponse(str(catagory)+'#'*10+str(file_id))