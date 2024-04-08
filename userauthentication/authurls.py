from django.contrib import admin
from django.urls import path, include
from . import authviews

urlpatterns = [
    path('signup/', authviews.signup, name = 'signup'),
    path('login/', authviews.login, name = 'login'),  
    path('activate/<uidb64>/<token>', authviews.activate, name='activate'),
]