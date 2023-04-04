
from uuid import uuid4

from django.conf import settings
from base.models.basemodel import BaseModel
from django.db import models
from accounts.models.user import User
from tinymce.models import HTMLField
from django.dispatch import receiver
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.core.mail import send_mail

def sendWelcomeMail(recipient_list,from_email):

    subject =  f'Congratulations on Signing Up with Us, {recipient_list}'
    
    message = 'We are thrilled to welcome you to InstaClone! Thank you for signing up and becoming a part of our community. \n\nAs a member of InstaClone, you will have access to some of the best features and benefits our platform offers. We hope you find these features useful and enjoy using our platform. \n\nIf you have any questions or concerns, please do not hesitate to reach out to our support team at instaclone@gmail.com. We are always happy to help. \n\nThank you again for joining InstaClone! We look forward to seeing you around the site. \n\nBest regards, \n\nTeam InstaClone!'

    from_email= from_email
    recipient_list = [recipient_list]
                
    send_mail(subject=subject,message=message,from_email=from_email,recipient_list=recipient_list,fail_silently=False,)


def sendActivationMail(recipient_list,from_email,email_token):

    subject =  f'Account {recipient_list} Verification Required'
    
    message = f'Click on the link to verify Your Account http://127.0.0.1:8000/activation/{email_token}'

    from_email= from_email
    recipient_list = [recipient_list]
                
    send_mail(subject=subject,message=message,from_email=from_email,recipient_list=recipient_list,fail_silently=False)

class Profile(BaseModel):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')

    username = models.CharField(max_length=100,blank=True, null=True,unique=True)
    firstname = models.CharField(max_length=100,blank=True, null=True)
    lastname = models.CharField(max_length=100,blank=True, null=True)

    slug = models.SlugField(blank=True, null=True)

    organizationName = models.CharField(max_length=500,blank=True, null=True)
    location = models.CharField(max_length=100,blank=True, null=True)

    email = models.EmailField(max_length=150,null=True,blank=True)
    emailVerified = models.BooleanField(default=False)
    email_token = models.CharField(max_length=100)

    phone = models.CharField(max_length=12,blank=True, null=True)
    phoneVerified = models.BooleanField(default=False)
    phone_token = models.CharField(max_length=6)

    dob = models.DateField(blank=True, null=True)

    bio = HTMLField(blank=True, null=True)

    profilePic = models.ImageField(upload_to='uploads/ProfilePic',default='uploads/ProfilePic/profile.jpg')

    reset_password = models.CharField(max_length=100,blank=True, null=True)
    
    def save(self, *args, **kwargs):
       self.slug = str(slugify(self.username))
       super(Profile, self).save(*args, **kwargs) 

    def __str__(self) -> str:
        return self.email
    
    class Meta:
        indexes = [models.Index(fields = ['username','email','firstname','lastname','phone','organizationName']),]
        managed = True
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    @receiver(post_save,sender =User)
    def CreateProfileObj(sender,instance,created,*args, **kwargs):
        if created:
            try:
                email_token = str(uuid4())
                profile = Profile.objects.create(user = instance,email = instance.email,email_token = email_token)

                # Send Welcome EMAIl

                from_email=settings.EMAIL_HOST_USER
                recipient_list = [instance.email]
                
                # Send Welcome Mail
                sendWelcomeMail(recipient_list=instance.email,from_email=from_email)
                
                # Send Activation Mail
                sendActivationMail(recipient_list=instance.email,from_email=from_email,email_token=email_token)
            except Exception as e:
                print(e)


class Follower(BaseModel):
    user = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='followers')
    followers_user = models.ManyToManyField(Profile,related_name='followers_user')
    followers_user_count = models.IntegerField(default=0)


    @receiver(post_save,sender = Profile)
    def CreateFollowerObj(sender,instance,created,*args, **kwargs):
        if created:
            try:
                follower = Follower.objects.create(user = instance,followers_user_count=0)
            except Exception as e:
                print(e)

    def __str__(self) -> str:
        return self.user.email


class Following(BaseModel):
    user = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='following')
    following_user = models.ManyToManyField(Profile,related_name='following_user')
    following_user_count = models.IntegerField(default=0)

    @receiver(post_save,sender = Profile)
    def CreateFollowerObj(sender,instance,created,*args, **kwargs):
        if created:
            try:
                follower = Following.objects.create(user = instance,following_user_count=0)
            except Exception as e:
                print(e)

    
    def __str__(self) -> str:
        return self.user.email

    