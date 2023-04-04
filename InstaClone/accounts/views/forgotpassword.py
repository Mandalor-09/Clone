from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from accounts.models.user import User
from accounts.models.profile import Profile
from django.core.mail import send_mail
from uuid import uuid4
from django.conf import settings
from django.contrib import messages

def SendMailForgotPassword(email,from_email,reset_password):
    subject = f'Hello {email} we got a request for Forgot Password'
    message = f'Click on the link to verify Your Account http://127.0.0.1:8000/resetpassword/{email}/{reset_password}'

    from_email= from_email
    recipient_list = [email]
                
    send_mail(subject=subject,message=message,from_email=from_email,recipient_list=recipient_list,fail_silently=False)


class ForgotPasswordView(View):
    def get(self, request, *args, **kwargs):
        return render(request,'accounts/forgotpassword.html')

    def post(self, request, *args, **kwargs):
        from_email = settings.EMAIL_HOST_USER
        email = request.POST.get('email')
        profile = Profile.objects.filter(email=email).exists()
        if profile:
            profile = Profile.objects.get(email = email)
            reset_password = str(uuid4())
            profile.reset_password=reset_password
            profile.save()
            SendMailForgotPassword(email = email,from_email=from_email,reset_password=reset_password)
            messages.success(request,'Check Your Email to Reset your Password')
            return JsonResponse({'status':'success','message':'Check Your Email to Reset your Password'})
        else:
            messages.warning(request,'No Such User')
            return JsonResponse({'status':'error','message':'No Such User'})


