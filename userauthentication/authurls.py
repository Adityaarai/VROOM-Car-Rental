from django.contrib import admin
from django.urls import path, include
from . import authviews
from django.contrib.auth import views as auth_views  # Import Django's built-in views

urlpatterns = [
    path('signup/', authviews.signup, name='signup'),
    path('login/', authviews.login, name='login'),  
    path('activate/<uidb64>/<token>/', authviews.activate, name='activate'),
    path('user/profile/', authviews.user_profile_view, name='user_profile'),
    path('logout/', authviews.logout_view, name='logout'),

    path('staff/profile/', authviews.staff_profile_view, name='staff_profile'),
    
    # URLs for password reset using Django's built-in views
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
]
