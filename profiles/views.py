from django.views.generic import DetailView, View, FormView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import JsonResponse, HttpResponseBadRequest
from django.contrib import messages
from django.urls import reverse_lazy

from followers.models import Followers
from feed.models import Post
from .forms import PostForm, SkillForm
from .models import Profiles, Skill

class ProfileDetail(DetailView):
    http_method_names = ['get']
    template_name = 'profiles/detail.html'
    model = User
    context_object_name = 'user'

    slug_field = 'username'
    slug_url_kwarg = "username"
    
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['total_posts'] = Post.objects.filter(author=user).count()
        context['total_followers'] = Followers.objects.filter(following=user).count()
        if self.request.user.is_authenticated:
            context['you_follow'] = Followers.objects.filter(following=user,followed_by=self.request.user).exists()
        
        return context
    
class FollowView(LoginRequiredMixin, View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        
        if "action" not in data or "username" not in data: 
            return HttpResponseBadRequest("Missing Data")
        
        try:
            other_user = User.objects.get(username=data["username"])
        except User.DoesNotExist:
            return HttpResponseBadRequest("Missing User")
            
        if data["action"]=="follow":
            follower, created = Followers.objects.get_or_create(
                followed_by=request.user,
                following=other_user
            )
        else:
            try:
                follower = Followers.objects.get(
                    followed_by=request.user,
                    following=other_user
                )
            except Followers.DoesNotExist:
                follower = None
            
            if follower:
                follower.delete()

        return JsonResponse({
            'success': True, 
            'wording': 'Unfollow' if data["action"]=="follow" else "Follow" })


class AddImage(FormView):
    template_name = 'profiles/add_image.html'
    form_class = PostForm
    success_url = '/'


    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super().dispatch(request, *args, **kwargs)
    

    def form_valid(self, form):
        profile, created = Profiles.objects.get_or_create(user=self.request.user)
        profile.profile_pic = form.cleaned_data['profile_pic']
        profile.save()

        messages.success(self.request, "Profile Picture Successfully Added!")

        return super().form_valid(form)
    

class SkillListView(FormView):
    template_name = 'profiles/skills.html'
    form_class = SkillForm
    
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        new_skill_name = form.cleaned_data.get('new_skill')
        existing_skills = form.cleaned_data.get('skill')

        if new_skill_name:
            new_skill, created = Skill.objects.get_or_create(skill=new_skill_name)
            self.request.user.profile.user_skills.add(new_skill)

        for skill in existing_skills:
            self.request.user.profile.user_skills.add(skill)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['skills'] = Skill.objects.all()
        return context

    def get_success_url(self):
        return f"/profile/{self.request.user.username}/"