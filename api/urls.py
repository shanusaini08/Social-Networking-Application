from django.urls import path
from api import views

urlpatterns = [
    path('auth/signup/', views.SocialMediaUserSignupView.as_view(), name='signup'),
    path('auth/login/', views.LoginView.as_view(), name='login'),
    path('social/users/', views.UserSearchView.as_view(), name='users'),
    path('social/friends/', views.FriendListView.as_view(), name='friends'),
    path('social/pending-requests/', views.PendingFriendRequestsView.as_view(), name='pending-requests'),
    path('social/send-requests/', views.SendFriendRequestView.as_view(), name='send-requests'),
    path('social/accept-requests/', views.AcceptFriendRequestView.as_view(), name='accept-requests'),
    path('social/reject-requests/', views.RejectFriendRequestView.as_view(), name='reject-requests'),

]