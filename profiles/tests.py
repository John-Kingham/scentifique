from django.contrib.auth.models import User
from django.test import TestCase

from .models import UserProfile


class UserProfileTests(TestCase):

    def test_user_profile_creation(self):
        """Test that the user profile is created at user creation"""
        user = User.objects.create_user(
            username="testuser",
            password="testpass123",
            email="test@email.com",
        )
        user.save()
        self.assertNotEqual(user.userprofile, None)
        self.assertEqual(UserProfile.objects.count(), 1)
