from django.views import View
from accounts.models.profile import Profile
from main.models.post import Post
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from django.db import models
from django.core import serializers
from accounts.models.profile import Follower,Following
from django.contrib import messages


class SearchView(View):

    def get(self, request, *args, **kwargs):
        user = request.user
        profile = Profile.objects.get(user=user)

        alluser = Profile.objects.all()
        alluser_location = list({loc.location for loc in alluser})
        if None in alluser_location:
            alluser_location.remove(None)

        context = {
            'profile': profile,
            'allloc': alluser_location[0:10],
        }

        try:
            location = request.GET.get('location')
            search = request.GET.get('search')

            user = request.user 
            current_profile = Profile.objects.get(user=user)
            following = Following.objects.get(user=current_profile)
            allfollower = following.following_user.all()
            follower_emails = [p.user.email for p in allfollower]

            if profile.email in follower_emails:
                context['present'] = True

            if search and location:
                query = Profile.objects.filter(models.Q(username__icontains=search) | models.Q(location=location))
            elif search:
                query = Profile.objects.filter(models.Q(username__icontains=search))
            else:
                query = Profile.objects.filter(location=location)
            query = query.order_by('-created')
            pagination = Paginator(query, 1)
            pagenumber = request.GET.get('pgnumber')
            final_query = pagination.get_page(pagenumber)
            # Convert the QuerySet into a list of dictionaries
            context['querys'] = final_query
        except (EmptyPage, PageNotAnInteger) as e:
            # Handle invalid page numbers or pages that don't exist
            # pagination = Paginator(query, 1)
            # final_query = pagination.get_page(1)
            # context['querys'] = final_query
            print(e)
        
        return render(request, 'main/search.html', context)

    
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
            
            return HttpResponseRedirect(request.path_info)
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
            return HttpResponseRedirect(request.path_info)

