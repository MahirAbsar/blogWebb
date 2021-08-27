from django.http import request
from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, ListView, TemplateView, UpdateView
from blog_app.models import Blog, Like
from blog_app.forms import CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import uuid
# Create your views here.


class MyBlogs(LoginRequiredMixin, TemplateView):
    template_name = "blog_app/my_blogs.html"


class CreateBlog(LoginRequiredMixin, CreateView):
    model = Blog
    template_name = 'blog_app/write_blog.html'
    fields = ("blog_title", "blog_content", "blog_image")

    def form_valid(self, form):
        # ID --- primary
        blog_obj = form.save(commit=False)
        blog_obj.user = self.request.user
        title = blog_obj.blog_title
        # Slug in the URL
        blog_obj.slug = title.replace(" ", "-")+"-" + str(uuid.uuid4())
        # print("Title : ", blog_obj.blog_title)
        blog_obj.save()
        return HttpResponseRedirect(reverse('home'))


class BlogList (ListView):
    context_object_name = "blogs"
    model = Blog
    template_name = "blog_app/blog_list.html"


@login_required
def blog_details(request, slug):
    blog = Blog.objects.get(slug=slug)
    commentForm = CommentForm()
    reacted_blog = Like.objects.filter(blog=blog, user=request.user)
    print(reacted_blog)
    if reacted_blog:
        liked = True
    else:
        liked = False
    if request.method == 'POST':
        commentForm = CommentForm(request.POST)
        if commentForm.is_valid():
            commentInfo = commentForm.save(commit=False)
            commentInfo.user = request.user
            commentInfo.blog = blog
            commentInfo.save()
            return HttpResponseRedirect(reverse('blog_app:blog_details', kwargs={'slug': slug}))
    return render(request, 'blog_app/blog_details.html', context={'blog': blog, 'form': commentForm, 'liked': liked})


@login_required
def liked_blog(request, pk):
    blog = Blog.objects.get(pk=pk)
    user = request.user
    already_liked = Like.objects.filter(blog=blog, user=user)
    if not already_liked:
        user_liked = Like(blog=blog, user=user)
        user_liked.save()

    return HttpResponseRedirect(reverse('blog_app:blog_details', kwargs={'slug': blog.slug}))


@login_required
def unlike_blog(request, pk):
    blog = Blog.objects.get(pk=pk)
    user = request.user
    user_disliked = Like.objects.filter(blog=blog, user=user)
    user_disliked.delete()
    return HttpResponseRedirect(reverse('blog_app:blog_details', kwargs={'slug': blog.slug}))


class UpdateBlogs(LoginRequiredMixin, UpdateView):
    model = Blog
    fields = ('blog_title', 'blog_content', 'blog_image')
    template_name = "blog_app/edit_blog.html"

    def get_success_url(self, **kwargs):
        return reverse_lazy('blog_app:blog_details', kwargs={'slug': self.object.slug})


def search(request):
    query = request.GET['query']
    blogs = Blog.objects.filter(blog_title__icontains=query)
    dict = {'blogs': blogs}
    return render(request, 'blog_app/search.html', context=dict)
