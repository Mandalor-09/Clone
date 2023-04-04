from django.contrib import messages
from accounts.models.profile import Profile
from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
import os


class ProfileDetailView(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self, request, *args, **kwargs):
        user = request.user
        profile = Profile.objects.get(user = user)
        context = {
            'profile':profile,
        }
        return render(request,'main/profiledetail.html',context)
    
    def post(self, request, *args, **kwargs):
        # print(request.POST,request.FILES,'>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        user = request.user
        profile = Profile.objects.get(user=user)

        username = request.POST.get('username')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        orgname = request.POST.get('orgname')
        phone = request.POST.get('phone')
        bio = request.POST.get('bio')
        dob = request.POST.get('dob')
        location = request.POST.get('location')

        profile.username = username
        profile.firstname = firstname
        profile.lastname = lastname
        profile.organizationName = orgname
        profile.phone = phone
        profile.location = location 
        profile.bio = bio 
        profile.dob = dob
        profile.save()
        print('data saved')
        
        messages.success(request, 'Profile Detail updated successfully')
        return JsonResponse({"status": "success", "message": "Profile Detail updated successfully"})



def picupdate(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    pic = request.FILES['pic']
    print(pic)
    if pic is not None:
        profile.profilePic = pic
        profile.save()
        print('done')
        messages.success(request, 'ProfilePic updated successfully')
        return JsonResponse({"status": "success", "message": "ProfilePic updated successfully"})
    # if pic == profile.profilePic:
    #     profile.profilePic = profile.profilePic
    #     profile.save()
    #     messages.success(request, 'No Change in Profile Pic found')
    #     return JsonResponse({"status": "success", "message": "No Change in Profile Pic Found"})

    