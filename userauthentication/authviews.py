from django.shortcuts import render, redirect
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
from django.contrib.auth import authenticate, login, logout
from . tokens import generate_token
from django.utils.http import urlencode
import re 


# Create your views here.
def signup(request):
    if request.method == "POST":
        email = request.POST['email']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        pass1 = request.POST['password']
        pass2 = request.POST['confirm_password']
        
        if User.objects.filter(email=email):
            messages.error(request, "Email already registered!")
            return redirect('signup')
        
        if len(email) > 100:
            messages.error(request, "Email must be under 100 characters")

        if pass1 != pass2:
            messages.error(request, "Passwords didn't match!")
        
        if not email:
            messages.error(request, "Please provide an email address")
            return redirect('signup')
        
        # Check if the email contains "@gmail.com"
        if not re.match(r'.+@gmail\.com', email):
            messages.error(request, "Only Gmail addresses are allowed")
            return redirect('signup')

        myuser = User.objects.create_user(email=email, password=pass1, username=email)  # Set email as username
        myuser.first_name = firstname
        myuser.last_name = lastname
        myuser.is_active = False

        myuser.save()

        messages.success(request, "Your account has been successfully created. We have sent you a confirmation email, please confirm your email in order to activate your account.")

        # Welcome Email
        subject = "Welcome to VROOM-Car-Rental-Service Login!!"
        message = "Hello " + myuser.first_name + "!! \n" + "Welcome to VROOM-Car-Rental-Service!! \nThank you for visiting our website. \nWe have also sent you a confirmation email, please confirm your email address in order to activate your account. \n\nThanking You \n VROOM Car Rental Service"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        # Email address confirmation Email

        current_site = get_current_site(request)
        email_subject = "Confirm your Email @ VROOM-Car-Rental-Service Login!!"
        message2 = render_to_string('main/email_confirmation.html',{
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })

        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        email.fail_silently = True
        email.send()


        # Redirect to the sign-in page with the username pre-filled
        login_url = redirect('login').url
        return redirect(f'{login_url}?{urlencode({"email": email})}')  

    return render(request, 'main/signup.html')

def login(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST['password']

        # First, attempt to authenticate against the default User model using email
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return render(request, "main/index.html")
    
        # If no user was authenticated, show error message
        messages.error(request, "Invalid email or password!")
        return redirect('login')
    
    # Clear all messages before rendering the sign-in page
    setattr(request, 'messages', [])

     # If there's a username parameter in the URL, pre-fill the sign-in form
    email = request.GET.get('email', '')
    return render(request, 'main/login.html', {'email': email})

#def signout(request):
 #   logout(request)
 #   messages.success(request, "Logged Out Successfully!")
 #   return redirect('index')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None
    
    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        return redirect('index')
    else:
        return render(request, 'main/activation_failed.html')
