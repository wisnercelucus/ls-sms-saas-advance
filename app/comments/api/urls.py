from django.urls import path
from comments.api import views as api_views

urlpatterns = [
	path('', api_views.CommentListApiView.as_view(), name='comment_list_api'),

	path('<int:pk>/', api_views.CommentDetailApiView.as_view(), name='comment_thread'),
	path('<int:pk>/manage', api_views.CommentManagementApiView.as_view(), name='comment_manage'),
	path('create/', api_views.CommentCreateApiView.as_view(), name='comment_create'),
	path('<int:pk>/like/', api_views.LikeToggleAPIView.as_view(), name='like_comment'),
]
