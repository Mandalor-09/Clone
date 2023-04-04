from django.contrib import admin

# Register your models here.
from accounts.models.profile import *
admin.site.register(Profile)
admin.site.register(Following)
admin.site.register(Follower)