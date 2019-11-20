from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from shortuuidfield import ShortUUIDField


class User(AbstractBaseUser,PermissionsMixin):
    # 不使用默认增长主键
    # 使用shortuuid
    uid = ShortUUIDField(primary_key=True)
    telephone = models.CharField(max_length=11)
    # password = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    # is_staff表示是否是员工
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'telephone'
    REQUIRED_FIELDS = ['username']
    EMAIL_FIELD = 'email'
