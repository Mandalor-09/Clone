from main.models.post import Post,CommentPost,Likes
from accounts.models.profile import Profile
from accounts.models.user import User
from django.shortcuts import render,redirect
from django.contrib import messages 
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

class LikeView(LoginRequiredMixin,View):
   
    def post(self, request, *args, **kwargs):
        print(request.POST)
        user = request.user
        profile = Profile.objects.get(user=user)
        
        post_id = request.POST.get('post_id')
        post = Post.objects.get(id = post_id)

        like = Likes.objects.get(image = post)
        all_liked_user = list(like.user.all())
        print(all_liked_user)
        emails = [ p.email for p in all_liked_user]

        print(emails)

        if profile.email in emails:
            like.user.remove(profile)
            a = post.likes_counts
            post.likes_counts = int(a) - 1
            post.save()
            like.save()
            messages.success(request,'Post Unliked')
            return JsonResponse({'status':'success','message':'Post Unliked'})
        else:
            like.user.add(profile)
            a = post.likes_counts
            post.likes_counts = int(a) + 1
            
            post.save()
            like.save()
            messages.success(request,'Post liked')
            return JsonResponse({'status':'success','message':'Post liked'})
            
        # if like.exists():
        #     like = Likes.objects.get(user = profile,image = post)
        #     like.is_liked = False
        #     like.delete()
        #     messages.success(request,'Post Unliked')
        #     return JsonResponse({'status':'success','message':'Post Unliked'})
        # else: 
        #     like = Likes.objects.create(user = profile,image = post,is_liked = True)
        #     like.save()
        #     messages.success(request,'Post liked')
        #     return JsonResponse({'status':'success','message':'Post liked'})
        