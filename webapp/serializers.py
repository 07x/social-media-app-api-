from rest_framework import serializers 
from .models import CustomUserModel  , FriendRequest , FriendList , Messaging , Post , Reactions , Comment
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
        profile_img = validated_data.get('profile_img', None)
        user = User.objects.create(
            email           = validated_data['email'],
            mobile          = validated_data['mobile'],
            bio             = validated_data['bio'],
            profile_img     = profile_img)
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
    
# MESSAGING
class MessagingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messaging
        fields = '__all__' 


# POST
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        

# REACTIONS
class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reactions
        fields = '__all__'
        extra_kwargs = {'user': {'required': False} , 'post':{'required':False}}


# COMMENT  
class PostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Comment 
        fields = '__all__'
        extra_kwargs = {'created_by':{'required':False},'post':{'required':False}, 'comment':{'required':True}}
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)
    