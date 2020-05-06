from django.urls import path
from comments.api import views as api_views

urlpatterns = [
	path('', api_views.CommentListApiView.as_view(), name='comment_list_api'),
	path('<int:pk>/', api_views.CommentDetailApiView.as_view(), name='comment_thread'),
	path('create/', api_views.CommentCreateApiView.as_view(), name='comment_create'),
    #path('comment/delete/<int:pk>/', views.delete_comment, name='delete_comment'),
]
