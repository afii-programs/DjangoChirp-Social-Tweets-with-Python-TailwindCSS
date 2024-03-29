from django.urls import path
from . import views

app_name = 'feed'

urlpatterns = [
    path('', views.HomePage.as_view(), name='index'),
    path('following/', views.FollowingFeed.as_view(), name='following'),
    path('<int:pk>/', views.PostDetailPage.as_view(), name='detail'),
    path('new/', views.CreatePostPage.as_view(), name='create'),
]