from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import CarDetail, CarOrder, User
from userauthentication.models import Profile
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from django.db import IntegrityError
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.conf import settings
     
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
            rentee = Profile.objects.get(user=request.user)
            existing_order = CarOrder.objects.filter(rentee=rentee, status='Pending').first()
            if existing_order:
                messages.error(request, "You have already placed an order.")
                return redirect('orders')

            startdate = request.POST.get('bookingStartDate')
            enddate = request.POST.get('bookingEndDate')

            if not startdate or not enddate:
                messages.error(request, "Please provide both start date and end date.")
                return HttpResponseRedirect(current_url)

            try:
                start_date_obj = datetime.strptime(startdate, '%Y-%m-%d').date()
                end_date_obj = datetime.strptime(enddate, '%Y-%m-%d').date()
            except ValueError:
                messages.error(request, "Invalid date format. Please use YYYY-MM-DD.")
                return HttpResponseRedirect(current_url)

            if start_date_obj < timezone.now().date():
                messages.error(request, "Cannot book cars in the past.")
                return HttpResponseRedirect(current_url)

            renter_name = request.POST['renter_name']
            renter_contact = request.POST['renter_contact']
            car_model = request.POST['car_model']

            try:
                product = CarDetail.objects.get(car_model=car_model, renter_name=renter_name, renter_contact=renter_contact)
            except CarDetail.DoesNotExist:
                messages.error(request, "Car details not found.")
                return HttpResponseRedirect(current_url)

            if product.availability == 'Booked':
              car_order = CarOrder.objects.filter(product=product).order_by('-end_date').first()
              if car_order and start_date_obj <= car_order.end_date.date():  # Convert to date for comparison
                messages.error(request, f"It is available only after {car_order.end_date.date()}.")  # Convert to date for message
                return HttpResponseRedirect(current_url)

            if start_date_obj > end_date_obj:
                messages.error(request, "Start date must be before end date.")
                return HttpResponseRedirect(current_url)

            price = product.price
            duration = (end_date_obj - start_date_obj).days
            total_price = price * duration

            order = CarOrder.objects.create(
                product=product,
                start_date=start_date_obj,
                end_date=end_date_obj,
                rentee=rentee,
                total_price=total_price
            )
            messages.success(request, "Your booking has been created successfully")
            return redirect('orders')
        else:
            messages.error(request, "You must be logged in to book cars!")
            return redirect('login')
    else:
        name = request.GET.get('renter_name')
        model = request.GET.get('car_model')
        details_queryset = CarDetail.objects.filter(renter_name=name, car_model=model)

        details_list = []
        for detail in details_queryset:
            car_order = CarOrder.objects.filter(product=detail).order_by('-end_date').first()
            detail_dict = {
                'renter_name': detail.renter_name,
                'renter_contact': detail.renter_contact,
                'car_type': detail.car_type,
                'car_model': detail.car_model,
                'price': detail.price,
                'availability': detail.availability,
                'image': detail.image.url,
                'end_date': car_order.end_date if car_order else None,
            }
            details_list.append(detail_dict)
        context = {
            'details': details_list,
        }
        return render(request, 'main/car_details.html', context)

# Create your views here.
def index(request):
    current_url = request.get_full_path()
    if request.method == 'POST':
      username_or_email = request.POST.get('username_or_email')
      password = request.POST['password']

      # Try to authenticate user by username
      user = authenticate(request, username=username_or_email, password=password)
        
      # If username authentication fails, try email authentication
      if user is None:
        user = User.objects.filter(email=username_or_email).first()
        if user:
          user = authenticate(request, username=user.username, password=password)
        
      if user is not None:
        auth_login(request, user)
        fname = user.first_name
        # messages.success(request, "Logged In Successfully!!")
        if user.is_staff and user.is_superuser:
          return redirect('admin_profile')
        elif user.is_staff:
          return redirect('distributor_profile')
        else:
          return redirect('index')
      else:
        messages.error(request, "Invalid username/email or password!")
        return HttpResponseRedirect(current_url)
    else:
      return render(request,'main/index.html')
            

def about_us(request):
    return render(request, 'main/about.html')

def learnmore(request):
   return render(request, "main/learnmore.html")

def userprofile(request):
   return render(request, 'main/user_profile.html')

def distributorprofile(request):
  try:
    if request.method == 'POST':
      renter_name = request.POST.get('renter_name')
      car_model = request.POST.get('car_model')
      
      car_detail = CarDetail.objects.filter(renter_name=renter_name, car_model=car_model).first()
   
      if car_detail:
        if 'changeUnlisted' in request.POST:
          car_detail.availability = "Unlisted"
          car_detail.save()
          messages.success(request, "Car status updated to Unlisted successfully")
        elif 'changeAvailable' in request.POST:
          car_detail.availability = "Available"
          car_detail.save()
          messages.success(request, "Car status updated to Available successfully")
        elif 'deleteCarDetails' in request.POST:
          car_detail.delete()
          messages.success(request, "Car deleted successfully")       
        else:
          messages.error(request, "Invalid action")
      else:
        order_id = request.POST.get('order_id')
        print(order_id)
        car_order = CarOrder.objects.filter(order_id=order_id).first()
        print(car_order)

        if 'approve' in request.POST:
          car_order.status = "Approved"
          car_order.save()
          
         # Welcome Email
          subject = "Your Order has been Approved!"
          message = f"""Hello {car_order.rentee.user.username}:,

We are excited to inform you that your order has been successfully approved!
Please proceed with the payment to fully complete this booking request. After payment the car will be delivered according to your needs.

Thank you for choosing VROOM-Car-Rental-Service. We are delighted to have you as a valued customer and look forward to providing you with an exceptional car rental experience.

If you have any questions or need further assistance, please don't hesitate to reach out to our support team.

Best regards,
The VROOM-Car-Rental-Service Team
"""

        from_email = settings.EMAIL_HOST_USER
        to_list = [car_order.rentee.user.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        messages.success(request, "Order  approved successfully")     
  except Exception as e:
    messages.error(request, f"Error: {str(e)}")


  items = CarDetail.objects.all()
  orders = CarOrder.objects.all()

  recent_orders = CarOrder.objects.all()[:5]

  context = {
    'items': items,
    'orders': orders,
    'recent_orders': recent_orders,
  }

  return render(request, 'main/distributor.html', context)

def adminprofile(request):
  try:
    if request.method == 'POST':
      if 'deleteUser' in request.POST:
        email = request.POST.get('email')
        myuser = User.objects.get(email=email)
        profile = Profile.objects.get(user=myuser)

        CarOrder.objects.filter(rentee=profile).delete()

        myuser.delete()
        messages.success(request, "User deleted successfully")
      elif 'editUser' in request.POST or 'editDistributor' in request.POST:
        email = request.POST.get('email')
        print(email)
        myuser = User.objects.get(email=email)
        if myuser:
            myuser.first_name = request.POST.get('FirstName')
            myuser.last_name = request.POST.get('LastName')
            myuser.email = request.POST.get('email')
            myuser.save()

            profile, created = Profile.objects.get_or_create(user=myuser)
            profile.address = request.POST.get('location')
            profile.contact = request.POST.get('contactNumber')

            if 'editDistributor' in request.POST:
                profile.save()
            else:
                profile.license_number = request.POST.get('license_number')
                profile.save()
      else:  
        username = request.POST.get('username')
        if User.objects.filter(username=username).exists():
            # Username already exists, handle the error gracefully
            messages.error(request, "Username already exists.")
        else:
            # Proceed with creating the user
            if 'addDistributor' in request.POST:
              license_number = None
            else:
              license_number = request.POST.get('license_number')
            
            first_name = request.POST.get('FirstName')
            last_name = request.POST.get('LastName')
            email = request.POST.get('email')
            location = request.POST.get('location')
            password = request.POST.get('password')
            contact = request.POST.get('contactNumber')

            myuser = User.objects.create(username=username, email=email, password=password)
            myuser.first_name = first_name
            myuser.last_name = last_name
            if 'addDistributor' in request.POST:
              myuser.is_staff = True
              
              # Get permissions for CarDetail model
              car_detail_content_type = ContentType.objects.get_for_model(CarDetail)
              car_detail_permissions = Permission.objects.filter(content_type=car_detail_content_type)

              # Get permissions for CarOrder model
              car_order_content_type = ContentType.objects.get_for_model(CarOrder)
              car_order_permissions = Permission.objects.filter(content_type=car_order_content_type)

              # Combine permissions from all models
              all_permissions = car_detail_permissions | car_order_permissions

              # Assign permissions to the user
              myuser.user_permissions.add(*all_permissions)
            else:
              myuser.is_staff = False
              
            myuser.save()
            
            try:
                # Assuming Profile is your Profile model
                profile, created = Profile.objects.get_or_create(user=myuser)
                profile.address = location
                profile.contact = contact
                profile.license_number = license_number
                profile.save()
                messages.success(request, "User added successfully!!")
            except IntegrityError:
                # Handle the case where the username was created by another request between the exists() check and this block
                messages.error(request, "An error occurred while creating the user.")
  except ObjectDoesNotExist:
    messages.error(request, "User does not exist")

  user_details = Profile.objects.all()

  recent_users = Profile.objects.select_related('user').order_by('-user__date_joined')[:5]

  context = {
    'user_details': user_details,
    'recent_users': recent_users,
  }
  return render(request, 'main/admin.html', context)




