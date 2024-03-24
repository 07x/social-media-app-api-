from rest_framework import serializers 
from .models import CustomUserModel  , FriendRequest , FriendList
from django.contrib.auth import get_user_model

# VALIDATORS 
from rest_framework.validators import UniqueValidator


User  = get_user_model()
# USER 
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'password', 'email', 'mobile', 'bio','profile_img')
        read_only_fields = ('id',)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create(
            email           = validated_data['email'],
            mobile          = validated_data['mobile'],
            bio             = validated_data['bio'],
            profile_img     = validated_data['profile_img'])
        user.set_password(validated_data['password'])
        user.save()
        return user

# FRIEND REQUEST
class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model  = FriendRequest 
        fields = ('id','sender','receiver','status')
        extra_kwargs = {'mobile': {'required': True, 'allow_blank': False}}

        """
            def validate(self, data):
                Custom serializer-level validation.
                # Example of validation across multiple fields
                if not data.get('email') and not data.get('mobile'):
                    raise serializers.ValidationError("Either email or mobile number is required.")
                return data
        """
    # CREATE 
    def create(self, validated_data):
        friend_request = FriendRequest.objects.create(
            sender     = validated_data['sender'],
            receiver   = validated_data['receiver'])
        friend_request.save()
        return friend_request
    
# FRIEND LIST 
class FriendListSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendList 
        fields = ('id','user','friend')
    