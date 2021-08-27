from django.conf.urls import url
from django.urls import path
from . import views
app_name = "login_app"

urlpatterns = [
    path('', views.home, name="home"),
    path('signup/', views.signUp, name="signup"),
    path('signin/', views.signIn, name="signin"),
    path('signout/', views.signOut, name='signout'),
    path('profile/', views.user_profile, name="profile"),
    path('change_info/', views.user_info_change, name="change_info"),
    path("password/", views.pass_change, name="pass_change"),
    path("add_pic/", views.add_pro_pic, name="add_pic"),
    path("change_pic/", views.change_pro_pic, name="change_pic"),

]
