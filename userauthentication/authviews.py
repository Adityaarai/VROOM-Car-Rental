from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from vroom import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from django.contrib.auth import authenticate, login as auth_login, logout
from . tokens import generate_token
from django.utils.http import urlencode
import re #regular expression - pattern check
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from .forms import UserProfileForm 
from django.contrib.auth import update_session_auth_hash
from carlisting.models import CarDetail, CarOrder


# Create your views here.
# View for handling signup functionality
def signup(request):
    if request.method == "POST":
        email = request.POST['email']
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        pass1 = request.POST['password']
        pass2 = request.POST['confirm_password']

        if User.objects.filter(email=email):
            messages.error(request, "Email already registered!")
            check = False
            return redirect('signup')
        
        if User.objects.filter(username=username):  # Check if the username is already taken
            messages.error(request, "Username already taken!")
            check = False
            return redirect('signup')
        
        if len(email) > 100:
            check = False
            messages.error(request, "Email must be under 100 characters")
            return redirect('signup')

        if pass1 != pass2:
            check = False
            messages.error(request, "Passwords didn't match!")
            return redirect('signup')
        
        if not email:
            check = False
            messages.error(request, "Please provide an email address")
            return redirect('signup')
        
        # Check if the email contains "@gmail.com"
        if not re.match(r'.+@gmail\.com', email):
            check = False
            messages.error(request, "Only Gmail addresses are allowed")
            return redirect('signup')

        myuser = User.objects.create_user(username=username, email=email, password=pass1)

        myuser.first_name = firstname
        myuser.last_name = lastname
        myuser.save()
            
        messages.success(request, "Your account has been successfully created. Welcome!")

        # Welcome Email
        subject = "Welcome to VROOM-Car-Rental-Service!!"
        message = f"""Hello {myuser.first_name}!!

Welcome to VROOM-Car-Rental-Service!!

Thank you for visiting our website and joining the VROOM team!!

Best regards,
VROOM-Car-Rental-Service"""

        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True) 
        
        return redirect('login')
    
    return render(request, 'main/signup.html')

# View for handling login functionality
def login(request):
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
            return redirect('login')
    
    # Clear all messages before rendering the sign-in page
    setattr(request, 'messages', [])

    # If there's a username or email parameter in the URL, pre-fill the sign-in form
    username_or_email = request.GET.get('username_or_email', '')
    return render(request, 'main/login.html', {'username_or_email': username_or_email})

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        auth_login(request, myuser)
        messages.success(request, "Your Account has been activated!!")
        return redirect('index')
    else:
        return render(request, 'main/activation_failed.html')

# View for handling user profile
@login_required
def user_profile_view(request):
    user = request.user

    # Retrieve logged-in user's email
    user_email = request.user.email
    
    if request.method == 'POST':
        form = PasswordChangeForm(user, request.POST)

        if 'update_profile' in request.POST:  # Check if the profile update form is submitted
            profile_form = UserProfileForm(request.POST, instance=user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, "Profile information updated successfully.")
            else:
                messages.error(request, "Failed to update profile information. Please check the provided data.")

            # Update username if it's changed
            new_username = request.POST.get('username')
            if new_username != user.username:
                user.username = new_username
                user.save()

        elif 'change_password' in request.POST:  # Check if the change password form is submitted
            form = PasswordChangeForm(user, request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                messages.success(request, "Password updated successfully.")
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
    
    # Filter CarDetail objects based on renter_name matching the logged-in user's username
    cars = CarDetail.objects.filter(renter_name=user.username)

    # Filter bookings based on user's email and status ("Pending")
    pending_bookings = CarOrder.objects.filter(rentee_email=user_email, status='Pending')

    # Filter bookings based on user's email and status ("Approved")
    approved_bookings = CarOrder.objects.filter(rentee_email=user_email, status='Approved')

    # Filter bookings based on user's email and status ("Paid")
    paid_bookings = CarOrder.objects.filter(rentee_email=user_email, status='Paid')

    # Filter bookings based on user's email and status ("Completed")
    completed_bookings = CarOrder.objects.filter(rentee_email=user_email, status='Completed')

    if not cars:  # If no cars found for the user
        message = "You haven't added any cars yet."
        return render(request, 'main/user_profile.html', {'user': user, 'message': message})
    else:
        return render(request, 'main/user_profile.html', {'user': user, 'cars': cars, 
        'pending_bookings': pending_bookings,
        'approved_bookings': approved_bookings,
        'paid_bookings': paid_bookings,
        'completed_bookings': completed_bookings})

# View for logging out
@login_required
def logout_view(request):
    logout(request)
    return redirect('index')

# View for add cars
@login_required
def add_car(request):
    if request.method == 'POST':
        contact_number = request.POST.get('contactNumber')
        car_type = request.POST.get('car_type')
        model = request.POST.get('model')
        price = request.POST.get('price')
        car_image = request.FILES.get('carImage')

        # Assuming the user is authenticated
        user = request.user

        # Create and save the CarDetail object
        try:
            car = CarDetail.objects.create(
                renter_name=user.username,  # Set the renter_name field to the username of the logged-in user
                renter_contact=contact_number,
                car_type=car_type,
                car_model=model,
                price=price,
                image=car_image,
            )
            # Adding a success message
            messages.success(request, 'Car added successfully.')
        except Exception as e:
            # Adding an error message
            messages.error(request, f'Error adding car: {e}')
        
        return redirect('user_profile')  # Redirecting to user profile page
    
    return render(request, 'user_profile.html')

# View for removing cars
@login_required
def remove_car(request):
    if request.method == 'POST':
        car_id = request.POST.get('car_id')
        if car_id:
            try:
                car = get_object_or_404(CarDetail, id=car_id)
                car.delete()
                # Adding a success message
                messages.success(request, 'Car successfully removed.')
            except:
                # Adding an error message
                messages.error(request, 'Failed to remove car.')
    return redirect('user_profile')  # Redirecting to user profile page

# View for payment
def payment_view(request):
    return render(request, 'main/payment.html')

