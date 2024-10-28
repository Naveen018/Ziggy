from django.shortcuts import redirect, render
from django.contrib import messages
from accounts.forms import UserForm
from accounts.models import User, UserProfile
from vendor.forms import VendorForm

# Create your views here.
def registerVendor(request):
    if request.method == "POST":
        # print(request.POST)
        form = UserForm(request.POST)
        vendor_form = VendorForm(request.POST, request.FILES)
        if form.is_valid() and vendor_form.is_valid():
            # print("Hiiiiiii")
            # Create user using the form
            password = form.cleaned_data["password"]
            user = form.save(commit=False)
            user.set_password(password)  #set_password() will set password to hashed format
            user.role = User.RESTAURANT
            user.save()

            vendor = vendor_form.save(commit=False)
            vendor.user = user
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            # vendor_name = vendor_form.cleaned_data["vendor_name"]
            vendor.save()
            
            messages.success(request, "Your account has been registered successfully!! Please wait for the approval")
            return redirect('registerVendor')
        else:
            messages.error(request, "Invalid Form!!")
            print(form.errors)
    else:
        form = UserForm()
        vendor_form = VendorForm()
    
    context = {
        "form": form,
        "vendor_form": vendor_form,
    }
    return render(request, "accounts/registerVendor.html", context)