from django.shortcuts import redirect
from accounts.models.profile import Profile
from django.views import View
from django.http import HttpResponse
from django.contrib import messages

class ActivationView(View):
    def get(self, request,email_token, *args, **kwargs):
        profile = Profile.objects.get(email_token = email_token)
        if profile:
            profile.emailVerified=True
            profile.save()
            messages.success(request,'Account Successfully Verified')
            return redirect('home')
        return HttpResponse('Something Went Wromg')