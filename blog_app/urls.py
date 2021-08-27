from django.urls import path
from . import views

app_name = "blog_app"

urlpatterns = [

    path('write/', views.CreateBlog.as_view(), name="write"),
    path('blog_list/', views.BlogList.as_view(), name="blog_list"),
    path('blog_details/<slug:slug>', views.blog_details, name="blog_details"),
    path('liked/<int:pk>', views.liked_blog, name="like"),
    path('unliked/<int:pk>', views.unlike_blog, name="unlike"),
    path('my_blogs/', views.MyBlogs.as_view(), name="my_blogs"),
    path('edit_blogs/<int:pk>', views.UpdateBlogs.as_view(), name="edit_blogs"),
    path("search/", views.search, name="search")

]
