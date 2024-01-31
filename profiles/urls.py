from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path("<str:username>/", views.ProfileDetail.as_view(), name="detail"),
]
