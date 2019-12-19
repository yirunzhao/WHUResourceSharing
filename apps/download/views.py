from django.shortcuts import render
from django.http import HttpResponse
from apps.whursauth.models import Resource, User


# def download_main(request):
#     return render(request, 'download/findresource.html')

def download_user(request,std_id):
    resSet = Resource.objects.all()
    resSider = resSet.order_by('-download_count')[0:7]
    if request.method == 'GET':
        context = {
            'main_res':list(resSet),
            'resSider':resSider,
            'std_id':std_id,
            'search':False
        }
        return render(request, 'download/findresource.html',context = context)
    elif request.method == 'POST':
        year = request.POST.get('year')
        dept = request.POST.get('dept')
        if year is None:
            searchSet = Resource.objects.filter(department = dept)
        elif dept is None:
            searchSet = Resource.objects.filter(year = year)
        else:
            searchSet = Resource.objects.filter(year = year, department = dept)
        context = {
            'main_res': searchSet,
            'resSider': resSider,
            'std_id': std_id,
            'search': True
        }
        return render(request, 'download/findresource.html', context=context)


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