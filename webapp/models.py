from django.db import models
from .manager import CustomUserManager
from django.contrib.auth.models import AbstractUser

REQUEST_STATUS = (
    ("ACCEPTED","ACCEPTED"),
    ("REJECTED","REJECTED"),
    ("PENDING","PENDING"),
)

# MODELS HERE 
class CustomUserModel(AbstractUser):
    # LETS MAKE SOME CUSTOME ROLES 
    class Types(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        USER = "USER", "User"
    type = models.CharField(max_length=20, choices=Types.choices, default=Types.USER)
    username        = None 
    email           = models.CharField(max_length=100,unique=True)
    mobile          = models.CharField(max_length=20,null=True,blank=True)
    profile_img     = models.ImageField(null=True,blank=True)
    bio             = models.TextField(null=True,blank=True) 
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    # DEFINING OUR NEW MANAGER 
    objects = CustomUserManager()

    def __str__(self):
        return str(self.email) +'||'+ str(self.mobile)
    
class FriendRequest(models.Model):
    sender          = models.ForeignKey(CustomUserModel,on_delete=models.CASCADE,related_name='friend_request_sender')
    receiver        = models.ForeignKey(CustomUserModel,on_delete=models.CASCADE,related_name='friend_request_receiver')
    status          = models.CharField(max_length=100,choices=REQUEST_STATUS,default="PENDING") 
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('sender', 'receiver') 
    def __str__(self):
        return str(self.created_at) +'|'+ str(self.sender) +'|'+ str(self.receiver)

    # # CREATE INSTANCE FOR FRIEND LIST 
    def save(self,*args,**kwargs):
        
        # VALIDATE  ACCEPTED
        if self.status == 'ACCEPTED':            
            # CREATE FRIEND LIST 
            friend_list = FriendList.objects.create(
                user    = self.receiver,
                friend  = self.sender)
            friend_list = FriendList.objects.create(
                user    = self.sender,
                friend  = self.receiver)
            # DELETE REQUEST
            self.delete()

        # VALIDATE  REJECTED
        elif self.status =='REJECTED':
            self.delete()
        else:
            super(FriendRequest, self).save(*args, **kwargs)  # Call the original save method

class FriendList(models.Model):
    user            = models.ForeignKey(CustomUserModel,on_delete=models.CASCADE,related_name='user')
    friend          = models.ForeignKey(CustomUserModel,on_delete=models.CASCADE,related_name='friend')
    is_close_friend = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'friend')

    def __str__(self):
        return str(self.user) +'|'+ str(self.friend) +'|'+ str(self.is_close_friend)

class Messaging(models.Model):
    sender          = models.ForeignKey(CustomUserModel,on_delete=models.CASCADE,related_name='messaging_sender')
    receiver        = models.ForeignKey(CustomUserModel,on_delete=models.CASCADE,related_name='messaging_receiver')
    message_text    = models.TextField()
    send_date       = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return str(self.send_date) +'|'+ str(self.sender) +'|'+ str(self.receiver)

class Post(models.Model):
    created_by      = models.ForeignKey(CustomUserModel,on_delete=models.CASCADE,related_name='send_fiend_request')
    title           = models.CharField(max_length=100,null=True)
    content         = models.TextField()
    created_at      = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return str(self.created_at) +'|'+ str(self.created_by) +'|'+ str(self.title)

class Reactions(models.Model):
    user            = models.ForeignKey(CustomUserModel,on_delete=models.CASCADE,related_name='reactions',)
    post            = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='reactions')
    status          = models.BooleanField(default=True)

    # class Meta:
    #     unique_together = ('user', 'post')

    def __str__(self):
        return str(self.status) +'|'+ str(self.user)

class Comment(models.Model):
    created_by          = models.ForeignKey(CustomUserModel,on_delete=models.CASCADE,)
    post                = models.ForeignKey(Post,on_delete=models.CASCADE)
    comment             = models.CharField(max_length=150,null=True,blank=True)
    comment_reply_to_id = models.ForeignKey('Comment',on_delete=models.CASCADE,related_name='comment_reply_id',null=True,blank=True)
    created_at          = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.created_at) +'|'+ str(self.created_by)



