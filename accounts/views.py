
from django.shortcuts import redirect, render
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, user_passes_test

from accounts.forms import UserForm
from accounts.models import User
from accounts.utils import detectUser

from django.core.exceptions import PermissionDenied
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
            messages.success(request, "Your account has been registered successfully!!")
            return redirect('registerUser')
        else:
            messages.error(request, "Please Try Again!!!")
            print(form.errors)
    else:
        form = UserForm()
    context = {"form":form,}
    return render(request, "accounts/registerUser.html", context)


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