from django.urls import path, include
from comments import views

app_name = 'comments'

urlpatterns = [
	path('api/', include(('comments.api.urls', 'comments-api'), namespace='comments-api')),
	path('<int:pk>/', views.comment_thread, name='comment_thread'),
	path('<int:pk>/comment', views.comment, name='comment'),
    #path('comment/delete/<int:pk>/', views.delete_comment, name='delete_comment'),
]
