from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'main/index.html')
        
def carlisting(request):
    return render(request, 'main/carlisting.html')

def about_us(request):
    return render(request, 'main/about.html')

#def login(request):
 #   return render(request, 'main/login.html')

#def signup(request):
 #   return render(request, 'main/signup.html')

