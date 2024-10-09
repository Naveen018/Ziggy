from django.shortcuts import redirect, render
from django.contrib import messages

from accounts.forms import UserForm
from accounts.models import User

# Create your views here.
def registerUser(request):
    if request.method == "POST":
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