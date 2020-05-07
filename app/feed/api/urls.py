from django.urls import path
from feed.api import views

app_name ='feed-api'

urlpatterns = [
    path('posts/', views.PostListApiView.as_view(), name='list'),
    path('post/<int:pk>/', views.PostDetailApiView.as_view(), name='detail_post'),
    path('post/create/create_url', views.PostCreateApiView.as_view(), name='create_post'),
    path('post/<int:pk>/share/', views.PostShareApiView.as_view(), name='share_post'),
    path('post/<int:pk>/like/', views.LikeToggleAPIView.as_view(), name='like_post'),
    path('post/<int:pk>/update/', views.PostUpdateApiView.as_view(), name='update_post'),
    path('post/<int:pk>/delete/', views.PostDeleteApiView.as_view(), name='delete_post'),
]
