from django.shortcuts import redirect, render
from django.views import View
from accounts.models.profile import Profile
from accounts.models.user import User
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse

class ResetView(View):
    def get(self, request, email, reset_password, *args, **kwargs):
        print(request.GET,'<<<<<<<<<>>>>>>>>>>>>>>>><<<<<<<<<<',email,reset_password,'<<<<<>')
        profile = Profile.objects.get(email=email, reset_password=reset_password)
        context = {
            'profile': profile,
        }
        return render(request, 'accounts/resetpasword.html', context)


    def post(self , request,email,reset_password, *args, **kwargs):
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')


        if email and reset_password:
            profile = Profile.objects.get(email = email,reset_password=reset_password)
            user = profile.user

            if not email or not password1 or not password2 or not (email or password1 or password2 ==""):
                messages.warning(request,'Crediential Required')
                return HttpResponseRedirect(request.path_info)
            if password1 != password2:
                messages.warning(request,'Password Mismatched')
                return HttpResponseRedirect(request.path_info)
            else:
                user.set_password(raw_password=password1)
                user.save()
                messages.success(request,'Password Changer Succesfully')
                return redirect('login')

                
    
    # def get(self, request, *args, **kwargs):
    #     email = kwargs.get('email')
    #     reset_password = kwargs.get('reset_password')
    #     context = {
    #         'mail':email,
    #         'reset_password':reset_password,
    #     }
    #     return render(request,'accounts/resetpassword.html',context)
    