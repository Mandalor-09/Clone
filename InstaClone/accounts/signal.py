from allauth.account.signals import user_signed_up
from allauth.socialaccount.models import SocialAccount
from accounts.models.user import User
from django.dispatch import receiver

@receiver(user_signed_up)
def creatingUserWhileThiredPartyLogin(sender,user,*args, **kwargs):
    social_accounts = SocialAccount.objects.get(user =user)
    email = social_accounts.extra_data.get('email')
    user = User.objects.filter(email=email).exists()
    if not user:
        user = User.objects.create_user(email=email,password=None)