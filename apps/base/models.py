# from django.db import models
# from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
# from shortuuidfield import ShortUUIDField
# class UserManager(BaseUserManager):
#     def _create_user(self,std_id,username,password,**kwargs):
#         if not std_id:
#             raise ValueError('需要传入学号')
#         if not username:
#             raise ValueError('需要传入用户名')
#         if not password:
#             raise ValueError('需要传入密码')
#
#         user = self.model(std_id=std_id,username=username,**kwargs)
#         user.set_password(password)
#         user.save()
#         return user
#
#     def create_user(self,std_id,username,password,**kwargs):
#         # 创建普通用户
#         kwargs['is_superuser'] = False
#         return self._create_user(std_id,username,password,**kwargs)
#
#     def create_superuser(self,std_id,username,password,**kwargs):
#         kwargs['is_superuser'] = True
#         return self._create_user(std_id,username,password,**kwargs)
#
#
#
# class User(AbstractBaseUser,PermissionsMixin):
#     # 不使用默认增长主键
#     # 使用shortuuid
#     uid = ShortUUIDField(primary_key=True)
#     telephone = models.CharField(max_length=11,unique=True)
#     # password = models.CharField(max_length=200)
#     email = models.EmailField(unique=True)
#     username = models.CharField(max_length=100)
#     is_active = models.BooleanField(default=True)
#     # is_staff表示是否是员工 是否能登陆到后台管理系统
#     is_staff = models.BooleanField(default=False)
#     # 什么时候加入
#     date_joined = models.DateTimeField(auto_now_add=True)
#
#     ## 本次项目独有的字段
#     # 学号
#     std_id = models.CharField(max_length=13,unique=True)
#     # 学院
#     school = models.CharField(max_length=15)
#     # 积分
#     points = models.IntegerField(default=0)
#     ##
#     # 作为唯一字段进行验证，不设置的话默认是username
#     USERNAME_FIELD = 'std_id'
#     REQUIRED_FIELDS = ['username','telephone','email']
#     EMAIL_FIELD = 'email'
#
#     objects = UserManager()
#
#     def get_full_name(self):
#         return self.username
#
#     def get_short_name(self):
#         return self.username
