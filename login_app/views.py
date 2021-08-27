from typing import Counter
from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect, HttpResponse
from .forms import SignUpForm, UserInfoChange, ProfilePicForm
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import re

# Create your views here.


def home(request):
    return render(request, 'blog_app/blog_list.html', context={})


def signUp(request):
    registered = False
    if request.method == "POST":
        signup = SignUpForm(data=request.POST)
        email_string = str(request.POST['email'])
        pattern = re.compile(r"^[a-z]*\.[a-z]*[0-9]*@northsouth.edu")
        matches = pattern.findall(email_string)
        if len(matches) == 0 or matches[0] == ".":
            messages.error(request, "Sorry, You cannot Use this Service")
            return render(request, 'login_app/error.html')
        else:
            if signup.is_valid():
                signup.save()
                registered = True
                messages.success(request, "Registration successful")
                return HttpResponseRedirect(reverse('login_app:signin'))
    else:
        signup = SignUpForm()

    dict = {'form': signup, 'registered': registered}
    return render(request, 'login_app/register.html', context=dict)


def signIn(request):
    success = False
    if request.method == "POST":
        signin = AuthenticationForm(data=request.POST)
        if signin.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                success = True
                messages.success(request, "You are logged in")
                return HttpResponseRedirect(reverse('blog_app:blog_list'))
            else:

                return render(request, 'login_app/error.html', context={"success": False})
        else:
            active = False
            return render(request, 'login_app/error.html', context={'success': False, 'active': False})

    else:

        signin = AuthenticationForm()

    dict = {'form': signin, 'success': success}
    return render(request, 'login_app/login.html', context=dict)


@login_required
def signOut(request):
    logout(request)
    messages.error(request, "You are Logged Out")
    # return render(request, 'blog_app/blog_list.html')
    return HttpResponseRedirect(reverse('blog_app:blog_list'))


def user_profile(request):
    current_user = request.user
    return render(request, 'login_app/profile.html')


@login_required
def user_info_change(request):
    current_user = request.user
    form = UserInfoChange(instance=current_user)
    if request.method == "POST":
        print("IN It")
        form = UserInfoChange(request.POST, instance=current_user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('login_app:profile'))
    return render(request, 'login_app/info_change.html', context={'form': form})


@login_required
def pass_change(request):
    current_user = request.user
    form = PasswordChangeForm(current_user)
    if request.method == "POST":
        form = PasswordChangeForm(current_user, request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('login_app:signin'))
    return render(request, 'login_app/pass_change.html', context={'form': form})


@login_required
def add_pro_pic(request):
    form = ProfilePicForm()
    if request.method == "POST":
        form = ProfilePicForm(request.POST, request.FILES)
        if form.is_valid():
            user_info = form.save(commit=False)
            user_info.user = request.user
            user_info.save()
            return HttpResponseRedirect(reverse('login_app:profile'))
    return render(request, 'login_app/add_pro_pic.html', context={'form': form})


@login_required
def change_pro_pic(request):
    form = ProfilePicForm(instance=request.user.user_profile)
    if request.method == "POST":
        form = ProfilePicForm(request.POST, request.FILES,
                              instance=request.user.user_profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('login_app:profile'))
    return render(request, 'login_app/add_pro_pic.html', context={'form': form})
