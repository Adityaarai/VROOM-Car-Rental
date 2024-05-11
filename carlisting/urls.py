from django.urls import path
from . import views

#urlpatterns
urlpatterns = [
    path('', views.index, name='index'),
    path('carlisting/', views.carlisting, name = 'carlisting'),
    path('about-us/', views.about_us, name = 'about_us'),
    path('user-profile/', views.userprofile, name = 'user_profile'),
    path('distributor-profile/', views.distributorprofile, name = 'distributor_profile'),
    path('admin-profile/', views.adminprofile, name = 'admin_profile'),
    path('orders/', views.orders, name = 'orders'),
]


