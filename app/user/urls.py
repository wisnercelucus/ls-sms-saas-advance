from django.contrib import admin
from django.urls import path, include
from user import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

app_name = 'user'

urlpatterns = [

    path('profile/<str:username>/', views.UserDetailView.as_view(), name='profile'),
    path('profile/<str:username>/follow/', views.UserFollowView.as_view(), name='follow'),
    path('api/', include(('user.api.urls', 'user-api'), namespace='user-api')),

    path('login/', auth_views.LoginView.as_view(
    		template_name='user/login.html',
    		), 
    		name = 'login'),

    path('logout/', views.logoutUser, 
    		name = 'logout'),

	path('change-password/', views.password_change,
		 	name='change_password'),

	path('password_reset', auth_views.PasswordResetView.as_view(
			template_name='user/reset_password.html', 
			email_template_name='user/reset_password_email.html',
			success_url=reverse_lazy('user:password_reset_done')), 
        	name='reset_password'
        	),
    
	path('password_reset/done/', auth_views.PasswordResetDoneView.as_view( 
		 	template_name='user/reset_password_done.html'),
		 	name='password_reset_done'
		 	),
    		
    
	path('reset/<uidb64>/<token>/', 
			auth_views.PasswordResetConfirmView.as_view(
			template_name='user/reset_password_confirm.html',
			success_url=reverse_lazy('user:password_reset_complete')),
    		name='password_reset_confirm'),

	path('password_reset/complete/', 
			auth_views.PasswordResetCompleteView.as_view(
    		template_name='user/reset_password_complete.html'),	
    		name='password_reset_complete'),
]
