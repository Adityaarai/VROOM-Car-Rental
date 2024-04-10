from django.shortcuts import render
from .models import CarDetails

# Create your views here.
def index(request):
    return render(request, 'main/index.html')
        
def carlisting(request):
    items = CarDetails.objects.all()

    context = {
        'items': items,
    }

    return render(request, 'main/carlisting.html', context)

def about_us(request):
    return render(request, 'main/about.html')

def userprofile(request):
   return render(request, 'main/user_profile.html')

def staffprofile(request):
   return render(request, 'main/staff_profile.html')

