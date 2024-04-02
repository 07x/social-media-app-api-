from django.http import Http404
from django.shortcuts import render

# EXTERNAL
from rest_framework.views import APIView 
from rest_framework import status 
from rest_framework.response import Response 
from rest_framework_simplejwt.tokens import RefreshToken

# AUTH & PERMISSION  
from rest_framework_simplejwt.authentication import JWTAuthentication 
from rest_framework.permissions import IsAuthenticated

# INTERNAL 
from .models import (
    Post ,
    Comment , 
    Messaging ,
    FriendList , 
    Reactions , 
    FriendRequest)

from django.contrib.auth import get_user_model
from .serializers import (
    CustomUserSerializer , 
    FriendRequestSerializer , 
    FriendListSerializer,
    MessagingSerializer,
    PostSerializer,
    ReactionSerializer,
    PostCommentSerializer)

from django.contrib.auth import authenticate 

# EXCEPTIONS 
from .exceptions import ObjectNotFoundException
from .responses import CustomResponse

# CREATE API's HERE 
User = get_user_model()

"""
    1. **User Management APIs:**
"""
class RegistrationView(APIView):
    def post(self,request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # GER CREATED USER DATA 
            serialized_user = CustomUserSerializer(user)  # Serialize the user object
            # GET DATA 
            return CustomResponse(message="user register successfully",data=serializer.data,status=status.HTTP_201_CREATED)
        else:
            return CustomResponse(message=serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    # POST 
    def post(self,request):
        data = request.data 

        # AUTHTICATE       
        user = authenticate(request,email=data.get('email'),password=data.get('password'))
        if user:
            # SIMPLE JWT TOKEN 
            refresh = RefreshToken.for_user(user)
            serializer = CustomUserSerializer(user)         
            response = {
                'message'       : 'login succesfully',
                'response_code' : 200,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'data'          : serializer.data,
            }
            return Response(response,status=status.HTTP_200_OK)        
        else:        
            return CustomResponse(message="'unable to find user with this credintials'",status=status.HTTP_400_BAD_REQUEST)

class UserDetails(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    # JWT AUTH & PERMISSIONS 
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise ObjectNotFoundException
    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = CustomUserSerializer(user)
        return CustomResponse(message="get user data successfully",data=serializer.data,status=status.HTTP_200_OK)
    def put(self,request,pk):
        user = self.get_object(pk)
        serializer = CustomUserSerializer(user,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return CustomResponse(message='data updated succesfully',data=serializer.data,status=status.HTTP_200_OK)
        else:
            return CustomResponse(message=serializer.errors,status=status.HTTP_400_BAD_REQUEST)
"""
    2. **Friendship Management APIs:**
"""
class FriendListView(APIView):

    def get(self,request):
        friends    = FriendList.objects.filter(user=request.user)
        serializer = FriendListSerializer(friends,many=True)
        return CustomResponse(message="get friend list data successfully",data=serializer.data,status=status.HTTP_200_OK)

class FriendRequestListView(APIView):
    def get(self,request):        
        friends    = FriendRequest.objects.filter(receiver=request.user)
        serializer = FriendRequestSerializer(friends,many=True)
        return CustomResponse(message="get friend list data successfully",data=serializer.data,status=status.HTTP_200_OK)

class SendFriendReqestView(APIView):
    # AUTH 
    authentication_classes = [JWTAuthentication]
    permission_classes     = [IsAuthenticated]

    def post(self,request):        
        serializer = FriendRequestSerializer(data=request.data)
        if serializer.is_valid():
            sender   = serializer.validated_data['sender']
            receiver = serializer.validated_data['receiver']
            if  FriendList.objects.filter(user=sender,friend=receiver).exists():
                return Response({'message':'user already in your friend list','response_code':400},status=status.HTTP_400_BAD_REQUEST)
            # UPDATED SENDER DETAILS 
            serializer.validated_data['sender'] = sender
            serializer.save()        
            return CustomResponse(message='your request sent succesfully',data=serializer.data,status=status.HTTP_201_CREATED)
        else:
            return CustomResponse(message=serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class AcceptFriendRequestView(APIView):
    def get_object(self, pk):
        try:
            return FriendRequest.objects.get(pk=pk)
        except FriendRequest.DoesNotExist:
            raise ObjectNotFoundException

    def patch(self,request,pk):
        friend_request = self.get_object(pk=pk)
        serializer  = FriendRequestSerializer(friend_request,data=request.data,partial=True)
        if serializer.is_valid():

            # CREATE TASK INSTANCE
            serializer.validated_data['status'] = 'ACCEPTED'
            serializer.save()
            return CustomResponse(message= 'friend reqest accepted successfully',status=status.HTTP_200_OK)
        else:
            return CustomResponse(message=serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
class RejectFriendRequestView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes     = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return FriendRequest.objects.get(pk=pk)
        except FriendRequest.DoesNotExist:
            raise ObjectNotFoundException

    def patch(self,request,pk):
        friend_request = self.get_object(pk=pk)
        serializer  = FriendRequestSerializer(friend_request,data=request.data,partial=True)
        if serializer.is_valid():
            # CREATE TASK INSTANCE
            serializer.validated_data['status'] = 'REJECTED'
            serializer.save()
            return CustomResponse(message='friend reqest canceled successfully',status=status.HTTP_200_OK)
        else:
            return CustomResponse(message= serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UnfriendView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes     = [IsAuthenticated]

    def get_object(self,pk):
        try:
            return FriendList.objects.get(pk=pk)
        except FriendList.DoesNotExist:
            raise ObjectNotFoundException

    def delete(self,request,pk):
        # GET INSTANCE
        friend = self.get_object(pk=pk)
        friend.delete()
        return CustomResponse(message='user unfriend successfully',status=status.HTTP_204_NO_CONTENT)
"""
    3. **Messaging APIs:**
"""
class ChatView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes     = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise ObjectNotFoundException
        
    def post(self,request,pk):
        user = self.get_object(pk=pk)
        serializer = MessagingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return CustomResponse(message='chat sent successfully',status=status.HTTP_200_OK)
        else:
            return CustomResponse(message=serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class ChatListView(APIView):

    # AUTH & PERMISSION 
    authentication_classes = [JWTAuthentication]
    permission_classes     = [IsAuthenticated]

    # GET USER 
    def get_object(self,pk):
        try:
            return  User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise ObjectNotFoundException
    def get(self,request,pk):
        chat_list = Messaging.objects.all()
        
        # SENDER & RECEIVER 
        owner   = request.user 
        user    = self.get_object(pk=pk) 
        # GET MESSAGE 
        queryset1 = chat_list.filter(sender=owner,receiver=user)
        queryset2 = chat_list.filter(sender=user,receiver=owner)
        queryset  =  queryset1.union(queryset2)
        serializer = MessagingSerializer(queryset,many=True)
        return CustomResponse(message='get all chats data',data=serializer.data,status=status.HTTP_200_OK)
   
class CreateListPostView(APIView):

    # AUTH & PERMISSION 
    authentication_classes = [JWTAuthentication]
    permission_classes     = [IsAuthenticated]

    def post(self,request):
        user_id = request.user.id
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['created_by'] = user_id
            serializer.save()
            return CustomResponse(message='post created successfully',tatus=status.HTTP_201_CREATED)
        else:
            return CustomResponse(message=serializer.errors,tatus=status.HTTP_400_BAD_REQUEST)
    def get(self,request):
        friend_list = list(FriendList.objects.filter(user=request.user).values_list('friend__id',flat=True))
        posts = Post.objects.filter(created_by__id__in=friend_list)
        serializer  = PostSerializer(posts,many=True)
        return CustomResponse(message='get post successfully',data=serializer.data,status=status.HTTP_200_OK)

class PostActivityView(APIView):
    
    # AUTH 
    authentication_classes = [JWTAuthentication]
    permission_classes     = [IsAuthenticated]

    # GET OBJECT 
    def get_obj(self,pk):
        try:
            return Post.objects.get(pk=pk)
        except Exception:
            raise ObjectNotFoundException

    def patch(self,request,pk):
        # POST
        flag = request.data.get('flag')
        if flag =='' or flag is None:
            return Response({'message':'please provide required fields','response_code':400})

        if flag =='1':
            serializer = ReactionSerializer(data=request.data)
            if serializer.is_valid():
                
                # UPDATE 
                serializer.validated_data['user']       = request.user
                serializer.validated_data['post']       =  self.get_obj(pk)
                serializer.save()
                return CustomResponse(message='post responsed successfully',status=status.HTTP_201_CREATED)
            else:   
                return CustomResponse(message=serializer.errors,status=status.HTTP_400_BAD_REQUEST)

        else:
            post_reaction = Reactions.objects.get(user=request.user)
            post_reaction.delete()
            return CustomResponse(message='post responsed successfully',status=status.HTTP_201_CREATED)

class PostCommentView(APIView):
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise ObjectNotFoundException

    def post(self,request,pk):
        serializer = PostCommentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(post=self.get_object(pk))
            return CustomResponse(message='comment done successfully',status=status.HTTP_201_CREATED)
        else:
            return CustomResponse(message=serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    