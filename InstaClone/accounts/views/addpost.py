from django.contrib import messages
from accounts.models.profile import Profile
from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
import os
from main.models.post import Post,PostImages,CommentPost,Likes

class AddPost(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self,request,*args, **kwargs):
        return render(request,'accounts/addpost.html')

    def post(self, request, *args, **kwargs):
        user = request.user
        profile = Profile.objects.get(user = user)
        post_pics = request.FILES.getlist('post_pics')
        caption = request.POST.get('caption')
        print(caption,post_pics,type(post_pics))
        
        createpost = Post.objects.create(profile=profile,caption=caption)
        for file in post_pics:
            PostImages.objects.create(post_ref=createpost, image=file)
            
        # return a JSON response indicating success
        messages.success(request,'Posted Pic')
        return JsonResponse({'status': 'success', 'message': 'Post added successfully.'})
