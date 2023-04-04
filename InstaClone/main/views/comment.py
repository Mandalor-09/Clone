from main.models.post import Post,CommentPost,Likes
from accounts.models.profile import Profile
from accounts.models.user import User
from django.shortcuts import render,redirect
from django.contrib import messages 
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

class CommentView(View):
    def post(self, request, *args, **kwargs):
        user = request.user 
        profile = Profile.objects.get(user = user)

        id = request.POST.get('id')
        comment = request.POST.get('comment')

        post = Post.objects.get(id = id)
        ctd = CommentPost.objects.create(post = post,user = profile,comment=comment)
        messages.success(request,' Commented')
        return JsonResponse({'status':'success','message':' Commented'})
    # def post(self, request, *args, **kwargs):
        # return HttpResponse('POST request!')