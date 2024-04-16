from django.urls import path
from . import views

#urlpatterns
urlpatterns = [
    path('', views.index, name='index'),
    path('carlisting/', views.carlisting, name = 'carlisting'),
    path('about-us/', views.about_us, name = 'about_us'),
    path('user-profile/', views.userprofile, name = 'user_profile'),
    path('staff-profile/', views.staffprofile, name = 'staff_profile'),
    path('orders/', views.orders, name = 'orders'),
]