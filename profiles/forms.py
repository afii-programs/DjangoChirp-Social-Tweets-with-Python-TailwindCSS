# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User

# class CustomUserCreationForm(UserCreationForm):
#     profile_pic = forms.ImageField(required=True)

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'profile_pic']
from django import forms

class PostForm(forms.Form):
    profile_pic = forms.ImageField()