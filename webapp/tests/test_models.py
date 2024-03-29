# EXTERNAL
from faker import Faker

# INTERNAL 
from django.test import TestCase
from webapp.models import FriendRequest
from django.contrib.auth import get_user_model 

User = get_user_model()
fake = Faker()

class UserModelTest(TestCase):

    def test_create_user(self):
        email    = fake.email() 
        mobile   = fake.phone_number()
        bio      = fake.text()
        password = "@bhinav123456" 
        
        # CREATE 
        user = User.objects.create_user(email=email,
                                        mobile=mobile,
                                        bio=bio,
                                        password=password)

        # VALIDATION 
        self.assertEqual(user.email, email)
        self.assertEqual(user.mobile, mobile)
        self.assertEqual(user.bio, bio)

        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.check_password(password))  # Check if password matches

    def test_create_super_user(self):
        email  = fake.email()
        mobile = fake.phone_number()
        bio    = fake.text()
        password = "@bhinav123456" 

        # CREATE SUPER USER 
        user = User.objects.create_superuser(email       = email,
                                        mobile   = mobile,
                                        bio      = bio,
                                        password = password)
        # VALIDATON 
        self.assertEqual(user.email , email)
        self.assertEqual(user.mobile,mobile)
        self.assertEqual(user.bio, bio)

        self.assertTrue(user.is_active)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.check_password(password))     # Check Password matches 

class FriendRequestTest(TestCase):
        
    def setUp(self):
        self.sender = User.objects.create_user(email=fake.email(), password='@bhinav1234')
        self.receiver = User.objects.create_user(email=fake.email(), password='@bhinav1234')

    def test_create_friend_request(self):
        friend_request = FriendRequest.objects.create(sender=self.sender, receiver=self.receiver)

        # Validate the sender and receiver of the friend request
        self.assertEqual(friend_request.sender, self.sender)
        self.assertEqual(friend_request.receiver, self.receiver)
