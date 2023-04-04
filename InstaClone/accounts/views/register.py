from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib import messages
from accounts.models.user import User


class RegisterView(View):

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        user = User.objects.filter(email = email)

        if not email or not password1 or not password2 or not (email or password1 or password2 ==""):
            messages.warning(request,'Crediential Required')
            return JsonResponse({'status':'error','message':'Crediential Required'})

        if password1 != password2:
            messages.warning(request,'Password Mismatched')
            return JsonResponse({'status':'error','message':'Password Mismatched'})

        if  user.exists():
            messages.warning(request,'User Already Excits')
            return JsonResponse({'status':'error','message':'User Already Excits'})
        
        else:
            user = User.objects.create_user(email = email ,password=password1)    
            messages.success(request,'User Created Successfully')
            return JsonResponse({'status':'success','message':'User Created Succesfully'})

    def get(self, request, *args, **kwargs):
        return render(request,'accounts/register.html')