# -*- coding: utf-8 -*-

from captcha.fields import ReCaptchaField
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from post.models import Post, Tag, Category


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, label='Kullanıcı Adı')
    password = forms.CharField(max_length=100, label='Parola', widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('Kullanıcı adı vaya parolayı yanlış irdiniz !')
            return super(LoginForm, self).clean()


class RegisterForm(forms.ModelForm):
    username = forms.CharField(max_length=100, label='Kullanıcı Adı')
    password1 = forms.CharField(max_length=100, label='Parola', widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=100, label='Parola Doğrulama', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'username',
            'password1',
            'password2',
        ]

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Parolalar eşleşmiyor")
        return password2


class ContactForm(forms.Form):
    email = forms.EmailField(required=True)
    konu = forms.CharField(required=True)
    mesaj = forms.CharField(widget=forms.Textarea, required=True)

    captcha = ReCaptchaField()


class PostForm(forms.ModelForm):
    captcha = ReCaptchaField()

    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'image',
            'category',
            'tag',
        ]


class CategoryForm(forms.ModelForm):
    captcha = ReCaptchaField()

    class Meta:
        model = Category
        fields = [
            'title',
        ]


class TagForm(forms.ModelForm):
    captcha = ReCaptchaField()

    class Meta:
        model = Tag
        fields = [
            'title',
        ]