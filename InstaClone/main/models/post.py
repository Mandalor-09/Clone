from django.db import models
from accounts.models.profile import Profile,Follower,Following
from base.models.basemodel import BaseModel
from django.dispatch import receiver
from django.db.models.signals import post_save

class Post(BaseModel):
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='profile')
    caption = models.CharField(max_length=1000,blank=True, null=True)
    likes_counts = models.IntegerField(default = 0)

    def __str__(self) -> str:
        return self.caption


class PostImages(BaseModel):
    post_ref = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='postimages')
    image  = models.ImageField(upload_to='Uploads/Post')


class Likes(BaseModel):
    user = models.ManyToManyField(Profile,related_name='likes_by_users',blank=True) # who is liking
    image = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='postlikes')
    

    @receiver(post_save,sender = Post)
    def CreateLikesObj(sender,instance,created,*args, **kwargs):
        if created:
            try:
                likes = Likes.objects.create(image = instance)
            except Exception as e:
                print(e)


    def __str__(self) -> str:
        return self.image.caption



class CommentPost(BaseModel):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comentpost')
    user = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='profilecommenting')
    comment = models.CharField(max_length=1000,blank=True, null=True)
    # likes_counts = models.IntegerField()

    # @receiver(post_save,sender = Post)
    # def CreateLikesObj(sender,instance,created,*args, **kwargs):
    #     if created:
    #         try:
    #             likes = Likes.objects.create(image = instance ,like_counts=0)
    #         except Exception as e:
    #             print(e)
    

