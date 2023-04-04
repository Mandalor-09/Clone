from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib import messages
from accounts.models.user import User
from accounts.backend import SettingsBackend
from django.contrib.auth import login


class LoginView(View):

    def post(self, request, *args, **kwargs):
        print(request.POST,'<<<<<<<<<<<<<>>>>>>>>>>>>>>')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.filter(email = email)

        if not email or not password or not (email or password ==""):
            messages.warning(request,'Crediential Required')
            return JsonResponse({'status':'error','message':'Crediential Required'})
        
        if not user.exists():
            messages.warning(request,'User Does Not Excits')
            return JsonResponse({'status':'Nouser','message':'User Does Not Excits'})
        
        else:
            user = User.objects.get(email = email)
            backend = SettingsBackend()
            user = backend.authenticate(request=request,email=email,password=password)
            if user is not None:
                user.backend = f"{backend.__module__}.{backend.__class__.__name__}"
                login(request,user)
                messages.success(request,'Login Succesfully')
                return JsonResponse({'status':'success','message':'Login Successfully'})
            else:
                messages.warning(request,'Invalid Credientials')
                return JsonResponse({'status':'warning','message':'In Valid Crediential'})        

    def get(self, request, *args, **kwargs):
        return render(request,'accounts/login.html')