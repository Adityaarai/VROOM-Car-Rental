from django.contrib import admin
from django.urls import path, include
from . import authviews

urlpatterns = [
    path('signup/', authviews.signup, name = 'signup'),
    path('login/', authviews.login, name = 'login'),  
    path('activate/<uidb64>/<token>', authviews.activate, name='activate'),
    path('dashboard/', authviews.dashboard_view, name='dashboard'),
    path('user/profile/', authviews.user_profile_view, name='user_profile'),
    path('staff/profile/', authviews.staff_profile_view, name='staff_profile'),
    path('logout/', authviews.logout_view, name='logout'),
]