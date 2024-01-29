from django.views.generic import ListView, DetailView, CreateView
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin

class HomePage(ListView):
    http_method_names = ['get']
    template_name = 'homepage.html'
    model = Post
    context_object_name = 'posts'
    queryset = Post.objects.all().order_by('-id')[0:30]


class PostDetailPage(DetailView):
    http_method_names = ['get']
    template_name = 'detail.html'
    model = Post
    context_object_name = 'post'

class CreatePostPage(LoginRequiredMixin, CreateView):
    template_name = 'create.html'
    model = Post
    fields = ['text']