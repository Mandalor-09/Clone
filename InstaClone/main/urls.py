from django.urls import path
from main.views.home import HomeView
from main.views.profile import ProfileView,AllProfileView
from main.views.profiledetail import ProfileDetailView,picupdate
from main.views.search import SearchView
from main.views.likes import LikeView
from main.views.comment import CommentView


urlpatterns = [
    path('home/',HomeView.as_view(),name='home'),
    path('profile/',ProfileView.as_view(),name='profile'),
    path('allprofile/<uid>',AllProfileView.as_view(),name='allprofile'),
    path('profiledetail/',ProfileDetailView.as_view(),name='profiledetail'),
    path('search/',SearchView.as_view(),name='search'),
    path('picupdate/',picupdate,name='picupdate'),
    path('liked/',LikeView.as_view(),name='liked'),
    path('comment/',CommentView.as_view(),name='comment'),
    
]
