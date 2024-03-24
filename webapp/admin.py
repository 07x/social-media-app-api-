from django.contrib import admin
from .models import * 


# Register your models here.
admin.site.register(CustomUserModel)
admin.site.register(FriendRequest)
admin.site.register(FriendList)
admin.site.register(Messaging)
admin.site.register(Post)
admin.site.register(Reactions)
admin.site.register(Comment)
