from django.urls import path
from feed.api import views


urlpatterns = [
    path('posts/', views.PostListApiView.as_view(), name='list'),
    path('post/create/create_url', views.PostCreateApiView.as_view(), name='create_post'),
    path('post/<int:pk>/share/', views.PostShareApiView.as_view(), name='share_post'),
    path('post/<int:pk>/like/', views.LikeToggleAPIView.as_view(), name='like_post'),
]
