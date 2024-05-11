from django.contrib import admin
from django.urls import path, include
from . import authviews
from django.contrib.auth import views as auth_views  # Import Django's built-in views

urlpatterns = [
    path('signup/', authviews.signup, name='signup'),
    path('login/', authviews.login, name='login'),  
    path('activate/<uidb64>/<token>/', authviews.activate, name='activate'),
    path('user/profile/', authviews.user_profile_view, name='user_profile'),
    path('staff/profile/', authviews.staff_profile_view, name='staff_profile'),
    path('logout/', authviews.logout_view, name='logout'),

    # URLs for password reset using Django's built-in views
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="main/reset_password.html"), 
         name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="main/reset_password_sent.html"), 
         name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="main/reset.html"), 
         name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="main/reset_password_complete.html"), 
         name="password_reset_complete"),
    
    path('add_car/', authviews.add_car, name='add_car'),
]
