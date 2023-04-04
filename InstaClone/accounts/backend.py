from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from accounts.models.user import User

class SettingsBackend(BaseBackend):

    def authenticate(self, request, email , password=None):
        if not email :
            raise ValueError('Email is None')
        user = User.objects.get(email =email)
        auth = user.check_password(password)
        if auth:
            return user
        return None


    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None