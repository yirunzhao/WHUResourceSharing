from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.auth import login,logout,authenticate
from django.views.decorators.http import require_POST
from .forms import LoginForm,RegisterForm
from django.http import JsonResponse
from django.views import View
from apps.whursauth.models import User
# DJC
from shortuuidfield import ShortUUIDField
from apps.whursauth.models import TagList, TagResourceLink, Resource

# DJC
MEDIA_ROOT = "D:\media"  # 后面再改


@require_POST
def upload_view(request):
	file = request.FILES.get('file')
	filename = request.POST.get('filename')
	fuid = ShortUUIDField()
	f = open(MEDIA_ROOT, 'wb')
	for i in file.chunks():
		f.write(i)
	resource = Resource.create(uid=fuid, title= filename, is_valid=True)  # 不知道怎么获取当前用户
	resource.save()
	link(fuid)  # 再把该文件的tag和resource连接起来

	return HttpResponse('上传成功!')

def link(fuid, *taglist):
	for tag in taglist:
		try:
			tag_obj = TagList.objects.get(tag_name=tag)
			rs_obj = Resource.objects.get(uid=fuid)
		except:
			print("Not found")
		else:
			link = TagResourceLink.create(tag_obj, rs_obj)
			tag_obj.link_count += 1
			link.save()


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
        return render(request,'base/resiger.html')

    def post(self,request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            std_id = form.cleaned_data.get('std_id')
            username = form.cleaned_data.get('username')
            telephone = form.cleaned_data.get('telephone')
            email = form.cleaned_data.get('email')
            print(email)
            password = form.cleaned_data.get('password')
            print(password)
            # 创建用户
            User.objects.create_user(std_id,username,password,telephone=telephone,email=email)
            return HttpResponse('创建成功')
        else:
            errors = form.get_errors()
            return JsonResponse({'code':499,'message':'','data':errors})

