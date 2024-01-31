from django.views.generic import DetailView
from django.contrib.auth.models import User
from feed.models import Post

# Create your views here.


class ProfileDetail(DetailView):
    http_method_names = ['get']
    template_name = 'profiles/detail.html'
    model = User
    context_object_name = 'user'

    slug_field = 'username'
    slug_url_kwarg = "username"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['total_posts'] = Post.objects.filter(author=user).count()
        return context