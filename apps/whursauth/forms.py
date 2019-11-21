from django import forms
from apps.forms import FormMixin


class LoginForm(forms.Form,FormMixin):
    std_id = forms.CharField(max_length=13)
    password = forms.CharField(max_length=20,min_length=6)
    remember = forms.IntegerField(required=False)

