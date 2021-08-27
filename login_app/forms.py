from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth.models import User
from .import models


class SignUpForm(UserCreationForm):
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'placeholder': 'abc@northsouth.edu'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username',
                  'email', 'password1', 'password2',)


class UserInfoChange(UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')


class ProfilePicForm(forms.ModelForm):
    class Meta:
        model = models.userInfo
        fields = ('profile_pic',)
