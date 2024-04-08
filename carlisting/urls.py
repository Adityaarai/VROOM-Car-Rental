from django.urls import path
from . import views

#urlpatterns
urlpatterns = [
    path('', views.index, name='index'),
    path('carlisting/', views.carlisting, name = 'carlisting'),
    path('about-us/', views.about_us, name = 'about_us'),

    #change after creating signin sinup page
   # path('signup/', views.signup, name = 'signup'),
    # path('login/', views.login, name = 'login'),
]