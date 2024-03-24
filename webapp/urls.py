from django.urls import path
from .views import (
    RegistrationView,
    LoginView,
    UserDetails,
    SendFriendReqestView,
    AcceptFriendRequestView,
    RejectFriendRequestView,
    FriendListView,
    FriendRequestListView,
    UnfriendView)

urlpatterns = [
    # 1
    path('registration/',RegistrationView.as_view(),name='registration'),
    path('login/',LoginView.as_view(),name='login'),
    path('user_details/<int:pk>/',UserDetails.as_view(),name='user_details'),
    # 2 
    path('show-friends/',FriendListView.as_view(),name='show_friends'),
    path('unfriend/<int:pk>/',UnfriendView.as_view(),name='unfriend'),
    path('show-friend-requests/',FriendRequestListView.as_view(),name='show_friend_requests'),
    path('sent-friend-request/',SendFriendReqestView.as_view(),name='sent_friend_request'),
    path('accept-friend-request/<int:pk>/',AcceptFriendRequestView.as_view(),name='accept_friend_request'),
    path('reject-friend-request/<int:pk>/',RejectFriendRequestView.as_view(),name='reject_friend_request'),
]
