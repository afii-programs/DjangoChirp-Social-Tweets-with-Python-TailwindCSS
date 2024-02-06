# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User

# class CustomUserCreationForm(UserCreationForm):
#     profile_pic = forms.ImageField(required=True)

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'profile_pic']
from django import forms
from allauth.account.forms import SignupForm,LoginForm
from til.utils import DivErrorList

class PostForm(forms.Form):
    profile_pic = forms.ImageField()


class CustomSignUpForm(SignupForm):
    def __init__(self, *args, **kwargs):
      super(CustomSignUpForm, self).__init__(*args, **kwargs)
      self.error_class = DivErrorList

class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)  
        self.error_class = DivErrorList

