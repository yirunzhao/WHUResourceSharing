from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse,FileResponse,StreamingHttpResponse
from django.utils.encoding import escape_uri_path

from django.contrib.auth import login,logout,authenticate
from django.views.decorators.http import require_POST
from .forms import LoginForm,RegisterForm,UserForm
from django.http import JsonResponse
from django.views import View
from apps.whursauth.models import User
# DJC
from shortuuidfield import ShortUUIDField
from apps.whursauth.models import User,Resource



rank_list = ['编译原理','算法','计算机组成原理','微机接口','模式识别','machine learning']
persons = {
    'hjw': {'image': 'image/hjw.jpg', 'text': '11111111'},
    'zyr': {'image': 'image/zyr.jpg', 'text': '22222222'},
    'djc': {'image': 'image/djc.jpg', 'text': '33333333'},
    'xzy': {'image': 'image/xzy.jpg', 'text': '44444444'},
}
context = {
    'rank_list': rank_list,
    'persons': persons
}
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
                    request.session['std_id'] = std_id
                    if remember:
                        request.session.set_expiry(None)
                    else:
                        # 立刻过期
                        request.session.set_expiry(0)
                    # 关于返回值，和前端人员约定好，看p245
                    # return render(request,'base/index.html',context=context)
                    return redirect(reverse('base:base_index'))
                else:
                    # return JsonResponse({'code': 405, 'message': '账号不是active', 'data': {}})
                    return HttpResponse('账号未激活')
            else:
                # return JsonResponse({'code': 400, 'message': '学号或者密码错误', 'data': {}})
                return HttpResponse('学号密码错误')
        else:
            errors = form.get_errors()
            return JsonResponse({'code': 400, 'message': '', 'data': errors})


class RegisterView(View):
    def get(self,request):
        return render(request,'base/signup.html')

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


def index(request):
	res = Resource.objects.all().order_by('-download_count')
	users = list(User.objects.all())
	users.sort(key=lambda x:len(x.upload_history))
	download_stars = users[0:3]

	context['res'] = res
	context['stars'] = download_stars
	return render(request,'base/index.html',context=context)


# def user_page(request,user_id):
# 	user = User.objects.get(std_id = user_id)
# 	print(user.email)
#
# 	#get upload history
#
#
# 	return render(request, 'base/user.html', context={)


def reveive_protrait(request):
	form = UserForm(request.POST,request.FILES)
	if form.is_valid():
		portrait = form.cleaned_data.get('portrait')
		user = User.objects.get(std_id='2017301110017')
		user.portrait = portrait
		user.save()
		return HttpResponse(str(user.portrait))
	else:
		return HttpResponse('不行')

def download_file(request, user, uid):
	#此处用的绝对路径，以后改成相对路径好了
	res = Resource.objects.get(uid = uid)
	res.download_count += 1
	res.save()
	path = str(res.file)

	userobj = User.objects.get(std_id=user)
	if uid not in userobj.download_history:
		if len(userobj.download_history) >= 400:
			download_history_s = userobj.download_history.split(",")
			print(download_history_s[1])
			del download_history_s[1]
			print(download_history_s)
			download_history_s.append(uid)
			userobj.download_history = ",".join(download_history_s)
		else:
			userobj.download_history = userobj.download_history + ',' + uid
	userobj.save()

	file = open('D:/documents/WHUResourceSharing/front/src/image/' + path, 'rb')
	response = StreamingHttpResponse(file)
	response['Content-Type'] = 'application/octet-stream'
	name = path.split('/')[-1]
	print(name)
	response['Content-Disposition'] = 'attachment;filename='+'"'+escape_uri_path(name)+'"'
	return response

def user_page(request,std_id):
	try:
		user = User.objects.get(std_id=std_id)
	except:
		return HttpResponse("没这人")
	# 验证是否是cookie存储了信息的用户
	else:
		session_id = request.session.get('std_id')

		# DJC added 在context里面包含用户的各种信息
		if user.std_id == session_id:
			#显示信息
			print(user.upload_history)
			upload_uid = user.upload_history.split(",")
			print(upload_uid)
			if len(upload_uid) >= 4:
				length = 3
			else:
				length = len(upload_uid)-1
			if upload_uid[0] == '' and len(upload_uid) == 1:
				length = 0
			ufiles = []
			uusers = []
			for i in range(length):
				ufiles.append(Resource.objects.get(uid=upload_uid[-(i+1)]))
				uusers.append(Resource.objects.get(uid=upload_uid[-(i+1)]).upload_user)

			# get download history
			download = user.download_history.split(",")
			if len(download) >= 4:
				length = 3
			else:
				length = len(download)-1

			if download[0] == '' and len(download) == 1:
				length = 0
			dfiles = []
			dusers = []
			for i in range(length):
				dfiles.append(Resource.objects.get(uid=download[-(i+1)]))
				dusers.append(Resource.objects.get(uid=download[-(i+1)]).upload_user)
			context = {
			'user' : user,
			'ufiles': ufiles,
			'dfiles': dfiles,
				'uusers':uusers,
				'dusers':dusers
			}

			return render(request,'base/user.html',context=context)

		else:
			return HttpResponse('无权访问他人主页')


def reveive_protrait(request):
    form = UserForm(request.POST,request.FILES)
    if form.is_valid():
        portrait = form.cleaned_data.get('portrait')
        std_id = request.session.get('std_id')
        user = User.objects.get(std_id=std_id)
        user.portrait = portrait
        user.save()
        return HttpResponse(str(user.portrait))
    else:
        return HttpResponse('不行')


def user_logout(request):
    logout(request)
    return redirect(reverse('base:base_index'))

# DJC

# MEDIA_ROOT = "D:\media"  # 后面再改

@require_POST
def upload_view(request, user_id):
	# print(request.FILES['upload_file'])
	user = User.objects.get(std_id = user_id)
	file = request.FILES.get('upload_file')
	print(file)
	filename = request.POST.get('filename')
	print(request.POST.get('year'))
	year = int(request.POST.get('year'))
	department = request.POST.get('dept')

		# fileurl = MEDIA_ROOT+filename.split(".")[-1]
		# f = open(fileurl, 'wb')
		# for i in file.chunks():
		# 	f.write(i)
	resource = Resource.objects.create(title= filename, is_valid=True, year = year,
								   department = department,file=file, upload_user = user)  # 不知道怎么获取当前用户
	print(resource.uid)
	if len(user.upload_history) >= 800:
		uh = user.upload_history.split(",")
		del uh[1]
		print(uh)
		uh.append(resource.uid)
		user.upload_history = ",".join(uh)
	else:
		user.upload_history = user.upload_history + ',' + resource.uid
	user.save()
	resource.save() # 再把该文件的tag和resource连接起来

	return HttpResponse('上传成功!')
	# else:
	# 	return HttpResponse('Not valid')

# def link(fuid, *taglist):
# 	for tag in taglist:
# 		try:
# 			tag_obj = TagList.objects.get(tag_name=tag)
# 			rs_obj = Resource.objects.get(uid=fuid)
# 		except:
# 			print("Not found")
# 		else:
# 			link = TagResourceLink.create(tag_obj, rs_obj)
# 			tag_obj.link_count += 1
# 			link.save()
