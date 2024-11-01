
from django.shortcuts import redirect, render
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, user_passes_test

from accounts.forms import UserForm
from accounts.models import User
from accounts.utils import detectUser, send_password_reset_email, send_verification_email

from django.core.exceptions import PermissionDenied

from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
# Restrict the Vendor from accessing the customer page
def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied

# Restrict the Customer from accessing the vendor page
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied
    
def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")
        return redirect('myAccount')
    elif request.method == "POST":
        # print(request.POST)
        form = UserForm(request.POST)
        if form.is_valid():
            # print("Hiiiiiii")
            # Create user using the form
            password = form.cleaned_data["password"]
            user = form.save(commit=False)
            user.set_password(password)  #set_password() will set password to hashed format
            user.role = User.CUSTOMER
            user.save()
            
            # Send verification email
            send_verification_email(request, user)
            messages.success(request, "Account registered! Check your email to activate.")
            return redirect('registerUser')
        else:
            messages.error(request, "Please Try Again!!!")
            print(form.errors)
    else:
        form = UserForm()
    context = {"form":form,}
    return render(request, "accounts/registerUser.html", context)

def activate(request, uidb64, token):
    # Activate the user by setting the is_active status to True
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Congratulations! Your account is activated.")
        return redirect('myAccount')
    else:
        messages.error(request, "Invalid activation link")
        return redirect('myAccount')

def login(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")
        return redirect('myAccount')
    elif request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        user = auth.authenticate(email=email, password=password)
        print(user)
        if user is not None:
            auth.login(request, user)
            messages.success(request, "You are now logged in")
            return redirect('myAccount')
        else:
            messages.error(request, "Invalid login credentials")
            return redirect('login')
    return render(request, "accounts/login.html")

def logout(request):
    auth.logout(request)
    messages.info(request, "You are logged out")
    return redirect('login')

@login_required(login_url='login')
def myAccount(request):
    user = request.user
    redirectUrl = detectUser(user) 
    return redirect(redirectUrl)

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def custDashboard(request):
    return render(request, "accounts/custDashboard.html")

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    return render(request, "accounts/vendorDashboard.html")

def forgot_password(request):
    if request.method == "POST":    
        email = request.POST.get("email")
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)
            
            # send reset password email
            send_password_reset_email(request, user)
            
            messages.success(request, "Password reset link has been sent to your email")
            return redirect("login")
        else:
            messages.error(request, "Account does not exist")
            return redirect("forgot_password")
    return render(request, "accounts/forgot_password.html")

def reset_password_validate(request, uidb64, token):
    # Validate the user by decoding the token and user pk
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        
    if user is not None and default_token_generator.check_token(user, token):
        # Store uid in session so that we can use this in reset_password funtion to know which user to reset
        request.session['uid'] = uid
        messages.info(request, "Please reset your password")
        return redirect('reset_password')
    else:
        messages.error(request, "This link has been expired")
        return redirect('myAccount')

def reset_password(request):
    if request.method == "POST":
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        
        if password == confirm_password:
            # Pick user from session
            uid = request.session.get('uid')
            user = User.objects.get(pk=uid)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, "Password reset successful")
            return redirect('login')
        else:
            messages.error(request, "Passwords do not match")
            return redirect('reset_password')
    return render(request, "accounts/reset_password.html")