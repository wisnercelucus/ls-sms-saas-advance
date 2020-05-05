from django.urls import path, include
from feed import views


app_name = 'feed'

urlpatterns = [

    path('', views.PostListView.as_view(), name='home'),
    path('api/', include(('feed.api.urls', 'feed-api'), namespace='feed-api')),
    path('comments/', include(('comments.urls', 'comments'), namespace='comments')),
    path('search/', views.PostListView.as_view(), name='search'),
    path('post/create/create_url', views.PostCreateView.as_view(), name='create_post'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='update_post'),
    path('post/delete/<int:pk>/', views.PostDeleteView.as_view(), name='delete_post'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='detail_post'),
    path('post/<int:pk>/share/', views.PostShareView.as_view(), name='post_share'),
    path('tags/<str:hashtag>/', views.HashTagView.as_view(), name='hashtag'),
]
