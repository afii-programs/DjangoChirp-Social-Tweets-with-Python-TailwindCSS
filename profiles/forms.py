from django import forms
from allauth.account.forms import SignupForm,LoginForm
from til.utils import DivErrorList
from .models import Skill

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

class SkillForm(forms.Form):
    new_skill = forms.CharField(max_length=100, required=False, label='New Skill')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['skill'] = forms.ModelMultipleChoiceField(
            queryset=Skill.objects.all(),
            widget=forms.CheckboxSelectMultiple(),
            required=False,
            label='Existing Skills'
        )

    def clean_new_skill(self):
        new_skill = self.cleaned_data['new_skill']
        if new_skill and Skill.objects.filter(skill=new_skill).exists():
            raise forms.ValidationError("This skill already exists.")
        return new_skill