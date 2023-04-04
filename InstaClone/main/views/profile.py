from accounts.models.profile import Follower, Following
from accounts.models.profile import Profile
from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from main.models.post import Post,CommentPost,PostImages,Likes
from django.contrib.auth.mixins import LoginRequiredMixin

class ProfileView(LoginRequiredMixin,View):
    login_url="login"
    def get(self, request, *args, **kwargs):
        user = request.user
        profile = Profile.objects.get(user = user)
        posts = Post.objects.filter(profile = profile).order_by('-created')
        context={
            'profile':profile,
            'posts':posts,
        }
        
        try:
            post_id = request.GET.get('post_id')
            post = Post.objects.get(id = post_id)
            like = Likes.objects.get(image = post)
            alluser = like.user.all()
            print(alluser,'<>')
            if profile in alluser:
                context['likedpost'] = True  
                print(context['likedpost'])  
            else:
                context['likedpost'] = False 
                print(context['likedpost'])  

        except Exception as e:
            print(e)
        print(context)
        return render(request,'main/profile.html',context)


class AllProfileView(View):
    def get(self,request, uid,*args, **kwargs):
        profile = Profile.objects.get(uid = uid)
        posts = Post.objects.filter(profile = profile).order_by('-created')
        context={
            'profile':profile,
            'posts':posts,
            "request":request,
        }
        user = request.user 
        current_profile = Profile.objects.get(user = user)
        following = Following.objects.get(user = current_profile)
        allfollower = following.following_user.all()
        follower_emails = [p.user.email for p in allfollower]
        if profile.email in follower_emails:
            context['present']=True

        
        return render(request,'main/allprofile.html',context)