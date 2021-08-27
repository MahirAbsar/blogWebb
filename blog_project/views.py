from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from django.http import HttpResponse


def home(request):
    return HttpResponseRedirect(reverse('blog_app:blog_list'))
