from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import CarDetail, CarOrder, User
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
     
def carlisting(request):
    items = CarDetail.objects.all()

    context = {
        'items': items,
    }

    return render(request, 'main/carlisting.html', context)

def orders(request):
    current_url = request.get_full_path()
    
    if request.method == 'POST':
      if request.user.is_authenticated:
        existing_order = CarOrder.objects.filter(rentee_email=request.user.email).first()
        if existing_order:
          messages.error(request, "You have already placed an order.")
          return redirect('orders')
          
        startdate = request.POST.get('bookingStartDate')
        enddate = request.POST.get('bookingEndDate')

        if not startdate or not enddate:
          messages.error(request, "Please provide both start date and end date.")
          return HttpResponseRedirect(current_url)
          
        renter_name = request.POST['renter_name']
        renter_contact = request.POST['renter_contact']
        car_model = request.POST['car_model']
        rentee_email = request.user.email

        product = CarDetail.objects.get(car_model=car_model, renter_name=renter_name, renter_contact=renter_contact)
                
        order = CarOrder.objects.create(product=product, start_date=startdate, end_date=enddate, rentee_email=rentee_email)

        messages.success(request, "Your booking has been created successfully")

        return redirect('orders')
      else:
        messages.error(request,"You must be logged in to book cars!!")
        return redirect('login')
    else:
        name = request.GET.get('renter_name')
        model = request.GET.get('car_model')

        details_queryset = CarDetail.objects.filter(renter_name=name, car_model=model)

        # Convert queryset to list of dictionaries with image URLs
        details_list = []
        for detail in details_queryset:
            detail_dict = {
                'id': detail.id,
                'renter_name': detail.renter_name,
                'renter_contact': detail.renter_contact,
                'car_type': detail.car_type,
                'car_model': detail.car_model,
                'price': detail.price,
                'availability': detail.availability,
                'image': detail.image.url
            }
            details_list.append(detail_dict)

        context = {
            'details': details_list,
        }
        return render(request, 'main/car_details.html', context)


# Create your views here.
def index(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST['password']

        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            auth_login(request, user)
            fname = user.first_name
            # messages.success(request, "Logged In Sucessfully!!")
            return render(request, "main/index.html")
            
        # If no user was authenticated, show error message
        else:
            messages.error(request, "Invalid email or password!")
            return redirect('index')
    else:
        return render(request, "main/index.html")
            

def about_us(request):
    return render(request, 'main/about.html')

def userprofile(request):
   return render(request, 'main/user_profile.html')

def distributorprofile(request):
  items = CarDetail.objects.all()

  context = {
    'items': items,
  }

  return render(request, 'main/distributor.html', context)

def adminprofile(request):
  users = User.objects.all()

  context = {
    'users': users,
  }

  return render(request, 'main/admin.html', context)

