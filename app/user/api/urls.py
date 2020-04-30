from django.urls import path
from user.api import views
from feed.api.views import PostListApiView

urlpatterns = [
    path('<str:username>/posts/', PostListApiView.as_view(), name='user-post-list'),

]
