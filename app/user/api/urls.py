from django.urls import path
from user.api import views
from feed.api.views import PostListApiView

urlpatterns = [
    path('<str:username>/posts/', PostListApiView.as_view(), name='user-post-list'),
    path('users/', views.UserListAPIView.as_view(), name='user-list'),
    #path('create/', views.CreateUserView.as_view(), name='create'),
    #path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'),

]
