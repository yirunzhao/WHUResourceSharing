from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def base_login_view(request):
    return render(request,'base/login.html')
