from django.contrib import admin
from .models import SocialMediaUser, FriendRequest, FriendRequestLimit

admin.site.register(SocialMediaUser)
admin.site.register(FriendRequest)
admin.site.register(FriendRequestLimit)