from django import forms
from django.contrib import auth
from django.shortcuts import redirect
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=30,
        min_length=3,
        required=True,
        label="用户名",
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '请输入用户名'},
        ),
        error_messages={
            'required': '账号不能为空',
            'max_length': '账号不能多于15位',
            'min_length': '账号不能低于5位'
        }
    )
    password = forms.CharField(
        min_length=6,
        required=True,
        label="密码",
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': '请输入密码'}
        ),
        error_messages={
            'required': '密码不能为空',
            'max_length': '密码不能多于15位',
            'min_length': '密码不能低于5位'
        }
    )

    def clean(self):
        # username = self.cleaned_data['username']
        # password = self.cleaned_data['password']
        # print(username, password)
        # user = auth.authenticate(username=username, password=password)
        # if user is None:
        #     raise forms.ValidationError('用户名或者密码不正确')
        # else:
        #     self.cleaned_data['user'] = user
        return self.cleaned_data


class RegForm(forms.Form):
    username = forms.CharField(
        max_length=30,
        min_length=3,
        required=True,
        label="用户名",
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '请输入用户名'},
        ),
        error_messages={
            'required': '账号不能为空',
            'max_length': '账号不能多于30位',
            'min_length': '账号不能低于3位'
        }
    )
    email = forms.EmailField(
        required=True,
        label="邮箱",
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': '请输入邮箱'}
        ),
        error_messages={
            'required': '邮箱不能为空',
        }
    )
    password = forms.CharField(
        min_length=6,
        required=True,
        label="密码",
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': '请输入密码'}
        ),
        error_messages={
            'required': '密码不能为空',
            'min_length': '密码不能低于6位'
        }
    )

    password_again = forms.CharField(
        min_length=6,
        required=True,
        label="密码",
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': '请再次输入一次密码'}
        ),
        error_messages={
            'required': '密码不能为空',
            'min_length': '密码不能低于6位'
        }
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("用户名已存在")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("邮箱已存在")
        return email

    def clean_password_again(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        email = self.cleaned_data['email']
        if password != password_again:
            raise forms.ValidationError('两次输入的密码不一致')
        return password_again
