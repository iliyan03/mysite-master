from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from . import models

class SignUpForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = {'username', 'password1', 'password2'}

class PostModelForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = (
            'description',
            'image',
        )

class UserModelForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = (
            'username',
            'bio',
            'profile_pic',
        )