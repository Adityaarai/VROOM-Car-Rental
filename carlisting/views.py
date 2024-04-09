from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'main/index.html')
        
def carlisting(request):
    return render(request, 'main/carlisting.html')

def about_us(request):
    return render(request, 'main/about.html')

def userprofile(request):
   return render(request, 'main/user_profile.html')

def staffprofile(request):
   return render(request, 'main/staff_profile.html')

