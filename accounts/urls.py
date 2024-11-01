from django.urls import path

from accounts import views

urlpatterns = [
    path("registerUser/", views.registerUser, name="registerUser"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("myAccount/", views.myAccount, name="myAccount"),
    path("custDashboard/", views.custDashboard, name="custDashboard"),
    path("vendorDashboard/", views.vendorDashboard, name="vendorDashboard"),
    path("activate/<str:uidb64>/<str:token>/", views.activate, name="activate"),
    
    path("forgot_password/", views.forgot_password, name="forgot_password"),
    path("reset_password_validate/<str:uidb64>/<str:token>/", views.reset_password_validate, name="reset_password_validate"),
    path("reset_password/", views.reset_password, name="reset_password"),
]