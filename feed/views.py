from django.views.generic import ListView, DetailView, CreateView, TemplateView
from .models import Post
from django.shortcuts import render
from followers.models import Followers
from django.contrib.auth.mixins import LoginRequiredMixin

class HomePage(ListView):
    http_method_names = ['get']
    template_name = 'homepage.html'
    model = Post
    context_object_name = 'posts'
    queryset = Post.objects.all().order_by('-id')[0:30]


class FollowingFeed(TemplateView):
    http_method_names = ["get"]
    template_name = "homepage.html"

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        following = list(
            Followers.objects.filter(followed_by=self.request.user).values_list('following', flat=True)
        )
        if not following:
            posts = None
        else:
            posts = Post.objects.filter(author__in=following).order_by('-id')[0:60]
        context['posts'] = posts
        return context



class PostDetailPage(DetailView):
    http_method_names = ['get']
    template_name = 'detail.html'
    model = Post
    context_object_name = 'post'

class CreatePostPage(LoginRequiredMixin, CreateView):
    template_name = 'create.html'
    model = Post
    fields = ['text']
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.save()
        return super().form_valid(form)


    def post(self, request, *args, **kwargs):

        post = Post.objects.create(
            text=request.POST.get("text"),
            author=request.user,
        )

        return render(
            request,
            "includes/post.html",
            {
                "post": post,
                "detail_on": True,
            },
            content_type="application/html"
        )