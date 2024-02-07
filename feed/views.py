from django.views.generic import ListView, DetailView, CreateView, TemplateView
from .models import Post
from followers.models import Followers
from django.shortcuts import render
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.core.paginator import Paginator


class HomePage(ListView):
    template_name = 'homepage.html'
    model = Post
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.all().order_by('-id')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_number = self.request.GET.get('page', 1)
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page_obj = paginator.get_page(page_number)
        context['posts'] = page_obj 
        return context

class FollowingFeed(TemplateView):
    template_name = "homepage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        following = list(
            Followers.objects.filter(followed_by=self.request.user).values_list('following', flat=True)
        )
        if not following:
            posts = None
            context['posts'] = posts
        else:
            posts = Post.objects.filter(author__in=following).order_by('-id')
            paginator = Paginator(posts, 10)
            page_number = self.request.GET.get('page', 1)
            page_obj = paginator.get_page(page_number)
            context['posts'] = page_obj 


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
        
        # Render the post detail template
        post_detail_html = render_to_string(
            "includes/post.html",
            {
                "post": obj,
                "detail_on": True,
            }
        )
        
        # Return an HTTP response with JavaScript for redirection
        return HttpResponse(
            f"""
            <script>
                setTimeout(function() {{
                    window.location.href = '{self.success_url}';
                }}, 100);  // Redirect after 3 seconds
            </script>
            {post_detail_html}
            """,
            content_type="text/html"
        )