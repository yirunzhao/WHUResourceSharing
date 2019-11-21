from django.shortcuts import render

# Create your views here.
from django.contrib.auth import login,logout,authenticate
from django.views.decorators.http import require_POST
from .forms import LoginForm
from django.http import JsonResponse


@require_POST
def login_view(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        std_id = form.cleaned_data.get('std_id')
        password = form.cleaned_data.get('password')
        # 这里可以添加remember，是否记住我
        remember = form.cleaned_data.get('remember')
        user = authenticate(request,username=std_id,password=password)
        if user:
            if user.is_active:
                login(request,user)
                if remember:
                    request.session.set_expiry(None)
                else:
                    # 立刻过期
                    request.session.set_expiry(0)
                # 关于返回值，和前端人员约定好，看p245
                return JsonResponse({'code':200,'message':'','data':{}})
            else:
                return JsonResponse({'code':405,'message':'账号不是active','data':{}})
        else:
            return JsonResponse({'code':400,'message':'学号或者密码错误','data':{}})
    else:
        errors = form.get_errors()
        return JsonResponse({'code':400,'message':'','data':errors})
