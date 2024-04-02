# EXTERNAL 
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from faker import Faker

# INTERNAL
from django.contrib.auth import get_user_model
from webapp.models import CustomUserModel 

User = get_user_model()
fake = Faker()


# REGISTER TEST 
class RegisterTestCase(APITestCase):
    def test_register(self):
        data = {
            "email"     : fake.email(),
            "mobile"    : fake.phone_number(),
            "bio"       : fake.text(),
            "password"  : "@bhinav1234"}
        

        response = self.client.post(reverse('registration'),data)
        # VALIDATION 
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

# LOGIN 
class LoginTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='abhi@gmail.com',bio="I am Dev",password="@bhinav1234")

    def test_login(self):
        data = {
            "email"     : "abhi@gmail.com",
            "password"  : "@bhinav1234"}
        
        response = self.client.post(reverse('login'),data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)


# USER DETAILS 
class UserDetails(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='abhi@gmail.com',bio='I am Dev',password="@bhinav1234") 
        self.token = refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' +  str(self.token))

    def test_user_details(self):
        response  = self.client.get(reverse('user_details',args=(self.user.id,)))
        self.assertEqual(response.status_code,status.HTTP_200_OK)