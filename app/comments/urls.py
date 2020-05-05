from django.urls import path, include
from comments import views

app_name = 'comments'

urlpatterns = [
	path('<int:pk>/', views.comment_thread, name='comment_thread'),
    #path('comment/delete/<int:pk>/', views.delete_comment, name='delete_comment'),
]
