
from django.contrib import admin
from django.urls import path,include
from accounts.views.register import RegisterView
from accounts.views.login import LoginView
from accounts.views.forgotpassword import ForgotPasswordView
from accounts.views.reset_password import ResetView
from accounts.views.activation import ActivationView
from accounts.views.addpost import AddPost

urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('register/',RegisterView.as_view(),name="register"),
    path('',LoginView.as_view(),name='login'),
    path('activation/<email_token>/',ActivationView.as_view(),name='activation'),
    path('forgotpassword/',ForgotPasswordView.as_view(),name='forgotpassword'),
    path('resetpassword/<email>/<reset_password>/',ResetView.as_view(),name='reset'),
    path('addpost/',AddPost.as_view(),name='addpost'),
    
]