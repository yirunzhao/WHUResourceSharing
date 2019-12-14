from django import forms
from apps.forms import FormMixin

class LoginForm(forms.Form,FormMixin):
    std_id = forms.CharField(max_length=13)
    password = forms.CharField(max_length=20,min_length=6)
    remember = forms.IntegerField(required=False)

class RegisterForm(forms.Form,FormMixin):
    std_id = forms.CharField(max_length=13)
    username = forms.CharField(max_length=20)
    telephone = forms.CharField(max_length=11,min_length=11)
    password = forms.CharField(max_length=20, min_length=6)
    email = forms.EmailField()

class UserForm(forms.Form,FormMixin):
    portrait = forms.ImageField()
