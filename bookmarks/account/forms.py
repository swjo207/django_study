#-*- coding: utf-8 -*-
from django import forms

# 사용자로부터의 로그인 입력 폼
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

