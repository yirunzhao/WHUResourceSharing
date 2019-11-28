from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.auth import login,logout,authenticate
from django.views.decorators.http import require_POST
from .forms import LoginForm,RegisterForm
from django.http import JsonResponse
from django.views import View
from apps.whursauth.models import User


# login的视图类
class LoginView(View):
    # get方式访问直接返回渲染的模板
    def get(self,request):
        return render(request,'base/login.html')

    # post方法就是提交表单，对表单进行相应的处理
    def post(self,request):
        form = LoginForm(request.POST)
        if form.is_valid():
            std_id = form.cleaned_data.get('std_id')
            password = form.cleaned_data.get('password')
            # 这里可以添加remember，是否记住我
            remember = form.cleaned_data.get('remember')
            user = authenticate(request, username=std_id, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    if remember:
                        request.session.set_expiry(None)
                    else:
                        # 立刻过期
                        request.session.set_expiry(0)
                    # 关于返回值，和前端人员约定好，看p245
                    return JsonResponse({'code': 200, 'message': '', 'data': {}})
                else:
                    return JsonResponse({'code': 405, 'message': '账号不是active', 'data': {}})
            else:
                return JsonResponse({'code': 400, 'message': '学号或者密码错误', 'data': {}})
        else:
            errors = form.get_errors()
            return JsonResponse({'code': 400, 'message': '', 'data': errors})


class RegisterView(View):
    def get(self,request):
        return HttpResponse('这里是注册页面')

    def post(self,request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            std_id = form.cleaned_data.get('std_id')
            username = form.cleaned_data.get('username')
            telephone = form.cleaned_data.get('telephone')
            password = form.cleaned_data.get('password')

            # 创建用户
            User.objects.create_user(std_id,username,password)
            return HttpResponse('创建成功')
        else:
            errors = form.get_errors()
            return JsonResponse({'code':499,'message':'','data':errors})