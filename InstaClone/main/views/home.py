from email.mime import image
from django.db.models import Q
from accounts.models.user import User
from accounts.models.profile import Profile,Following,Follower
from django.views import View
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from main.models.post import *

class HomeView(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        user_email_is = user.email
        profile = Profile.objects.get(user = user)
        following = Following.objects.get(user = profile)

        following_profiles = following.following_user.all()
        following_emails = [p.user.email for p in following_profiles]

        all_users = User.objects.filter(email__in=following_emails)

        # alluser = Profile.objects.exclude(user__in = all_users)
        alluser = Profile.objects.exclude(user__in = all_users).order_by('?')[:10]# send random 10 profile

        # following user post
        allunlikedpost = Post.objects.filter(profile__in = following_profiles)
        print(allunlikedpost)
        
        lik = Likes.objects.filter(image__in=allunlikedpost).exclude(Q(user=profile) & Q(image__in=allunlikedpost)).order_by('-created')
        finalpost_ids = lik.values_list('image__id', flat=True)
        print(finalpost_ids)
        finalpost = Post.objects.filter(id__in = finalpost_ids).order_by('-created')

        
        context = {
            'profile':profile,
            'alluser':alluser,
            'allunlikedpost':finalpost,
        }
        return render(request,'main/index.html',context)

    def post(self, request, *args, **kwargs):
        print(request.POST,'<<<<<??????????????????????>>>>>>>>>')
        user = request.user
        current_user = Profile.objects.get(user=user)

        uid = request.POST.get('followinguid')
        thefolloweduser = Profile.objects.get(uid=uid)

        # Following Code
        following_list = Following.objects.get(user=current_user)
        following_users = following_list.following_user.all()

        # Follower Code
        follower_list = Follower.objects.get(user = thefolloweduser)
        followers_of_user = follower_list.followers_user.all()

        if thefolloweduser in following_users:

            # Following Side Code

            following_list.following_user.remove(thefolloweduser)
            following_list.following_user_count -= 1
            following_list.save()

            # Follower Side Code

            follower_list.followers_user.remove(current_user)
            follower_list.followers_user_count -= 1
            follower_list.save()
            
            messages.success(request, f'Unfollowed {thefolloweduser.email}')
            
            return JsonResponse({'status':'success','message':'Unfollowed User'})
        else:

            #Following Side Code

            following_list.following_user.add(thefolloweduser)
            following_list.following_user_count += 1
            following_list.save()

            # Follower Side Code

            follower_list.followers_user.add(current_user)
            follower_list.followers_user_count += 1
            follower_list.save()

            messages.success(request, f'Followed {thefolloweduser.email}')
            return JsonResponse({'status':'success','message':'Followed User'})






# def post(self, request, *args, **kwargs):
#     user = request.user
#     current_user = Profile.objects.get(user=user)

#     uid = request.POST.get('uid')
#     thefolloweduser = Profile.objects.get(uid=uid)

#     following_list = Following.objects.get(user=current_user).following_user.all()
#     following_list1 = Following.objects.get(user=current_user)
#     following_counts = following_list1.following_user_count

#     if thefolloweduser in following_list:
#         following_list = list(following_list)
#         following_list.remove(thefolloweduser)
#         following_list1.following_user_count -= 1
#         following_list1.save()
#         messages.success(request, f'Unfollowed {thefolloweduser.email}')
#         return JsonResponse({'status': 'success', 'message': 'user unfollowed'})
#     else:
#         following_list.add(thefolloweduser)
#         following_list1.following_user_count += 1
#         following_list1.save()
#         messages.success(request, f'Followed {thefolloweduser.email}')
#         return JsonResponse({'status': 'success', 'message': 'user followed'})
