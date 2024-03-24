from django.contrib.auth.base_user import BaseUserManager 
from  django.db import models 

# CUSTOME USER MANAGER
class CustomUserManager(BaseUserManager):
    """
        Here we are going to define how to create create_user 
    """

    def create_user(self,email,password,**extra_fields):
        # EMAIL EXECPTION HANDLE 
        if not email:
            raise ValueError('Please Provide a Valid Email')
        email = self.normalize_email(email)

        # Importing CustomUserModel here to avoid circular import
        from .models import CustomUserModel        
        # Defaulting type to CUSTOMER if not provided
        extra_fields.setdefault('type', CustomUserModel.Types.USER)
        user  = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,email,password,**extra_fields):
        """
            Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff",True)
        extra_fields.setdefault("is_active",True)
        extra_fields.setdefault("is_superuser",True)
        
        from .models import CustomUserModel        
        # Defaulting type to CUSTOMER if not provided
        # Defaulting type to CUSTOMER if not provided
        extra_fields.setdefault('type', CustomUserModel.Types.ADMIN)

        # EXTRA VALIDATION 
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_active") is not True:
            raise ValueError("Superuser must have is_active")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Susperuser must have is_superuser")
        
        return self.create_user(email,password,**extra_fields)