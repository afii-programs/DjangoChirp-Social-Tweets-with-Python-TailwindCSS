from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path("<str:username>/", views.ProfileDetail.as_view(), name="detail"),
    path("<str:username>/add_image/", views.AddImage.as_view(), name="add_image"),
    path("<str:username>/follow/", views.FollowView.as_view(), name="follow"),
]
