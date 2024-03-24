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
    CustomUserModel , 
    FriendRequest)

from django.contrib.auth import get_user_model

from .serializers import (
    CustomUserSerializer , 
    FriendRequestSerializer , 
    FriendListSerializer)
from django.contrib.auth import authenticate 

# EXCEPTIONS 
from .exceptions import ObjectNotFoundException


# CREATE API's HERE 
User = get_user_model()


"""
    1. **User Management APIs:**
"""
# REGISTRATION 
class RegistrationView(APIView):
    def post(self,request):
        
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # GER CREATED USER DATA 
            serialized_user = CustomUserSerializer(user)  # Serialize the user object

            # GET DATA 
            response = {
                'message'           : 'user register succesfully',
                'response_code'     : 200, 
                'data'              : serialized_user.data
            }
            return Response(response,status=status.HTTP_200_OK)

        else:
            response = {
                'message'           : serializer.errors,
                'response_code'     : 400, 
            }
            return Response(response,status=status.HTTP_400_BAD_REQUEST)

# LOGIN 
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
            response = {
                'message'       : 'unable to find user with this credintials',
                'response_code' : 400,
            }
            return Response(response,status=status.HTTP_400_BAD_REQUEST)
        
# USER DETAILS 
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
        response = {
                'message'       : 'get user data successfully',
                'response_code' : 200, 
                'data'          : serializer.data}
        return Response(response,status=status.HTTP_200_OK)

    def put(self,request,pk):
        user = self.get_object(pk)
        serialzier = CustomUserSerializer(user,data=request.data)
        if serialzier.is_valid():
            serialzier.save()
            response = {
                'message'       :'data updated succesfully',
                'response_code' : 200,
                'data'          : serialzier.data}
            return Response(response,status=status.HTTP_200_OK)
        else:
            response = {
                'message'       : serialzier.errors,
                'response_code' : 400}
            return Response(response,status=status.HTTP_400_BAD_REQUEST)

"""
    2. **Friendship Management APIs:**
"""
class FriendListView(APIView):

    def get(self,request):
        
        friends    = FriendList.objects.filter(user=request.user)
        serializer = FriendListSerializer(friends,many=True)
        
        response = {
            'message'       : 'get friend list data successfully',
            'response_code' : 200, 
            'data'          : serializer.data
        }
        return Response(response,status=status.HTTP_200_OK)

class FriendRequestListView(APIView):
    def get(self,request):        
        friends    = FriendRequest.objects.filter(receiver=request.user)
        serializer = FriendRequestSerializer(friends,many=True)
        response = {
            'message'       : 'get friend request list data successfully',
            'response_code' : 200, 
            'count'         : friends.count(),
            'data'          : serializer.data
        }
        return Response(response,status=status.HTTP_200_OK)

class SendFriendReqestView(APIView):

    # AUTH 
    # authentication_classes = [JWTAuthentication]
    # permission_classes     = [IsAuthenticated]

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
            response = {
                'message'       : 'your request sent succesfully',
                'response_code' : 201,
                'data'          : serializer.data
            }
            return Response(response,status=status.HTTP_201_CREATED)
        else:
            response = {
                'message'       : serializer.errors,
                'response_code' : 400,
            }
            return Response(response,status=status.HTTP_400_BAD_REQUEST)

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
            response = {
                    'message'       : 'friend reqest accepted successfully',
                    'response_code' : 200}
            return Response(response,status=status.HTTP_200_OK)
        else:
            default_errors = serializer.errors
            new_error = {}
            for field_name, field_errors in default_errors.items():
                new_error[field_name] = field_errors[0]
            return Response(new_error, status=status.HTTP_400_BAD_REQUEST)
        
class RejectFriendRequestView(APIView):
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
            response = {
                    'message'       : 'friend reqest canceled successfully',
                    'response_code' : 200}
            return Response(response,status=status.HTTP_200_OK)
        else:
            default_errors = serializer.errors
            new_error = {}
            for field_name, field_errors in default_errors.items():
                new_error[field_name] = field_errors[0]
            return Response(new_error, status=status.HTTP_400_BAD_REQUEST)

class UnfriendView(APIView):

    def get_object(self,pk):
        try:
            return FriendList.objects.get(pk=pk)
        except FriendList.DoesNotExist:
            raise ObjectNotFoundException

    def delete(self,request,pk):
        # GET INSTANCE
        friend = self.get_object(pk=pk)
        friend.delete()

        resposne = {
            'message'           : 'user unfriend successfully',
            'response_code'     : 204
        }
        return Response(resposne,status=status.HTTP_204_NO_CONTENT)

