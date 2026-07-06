from http import HTTPStatus

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import UserProfile


class UserProfileTests(TestCase):

    @classmethod
    def setUp(cls):
        cls.user_password = "testpass123"
        cls.user = User.objects.create_user(
            username="testuser",
            password=cls.user_password,
            email="test@email.com",
        )
        cls.user.save()

    def test_user_profile_creation(self):
        """Test that the user profile is created at user creation"""
        self.assertNotEqual(self.user.userprofile, None)
        self.assertEqual(UserProfile.objects.count(), 1)

    def test_profile_view_get(self):
        """Test that the profile view works correctly for get requests"""
        # Test as a guest
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTemplateNotUsed(response, "profiles/profile.html")
        # Test as a logged in user
        self.client.login(
            username=self.user.username, password=self.user_password
        )
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "profiles/profile.html")
        self.assertContains(response, "User Profile")
        self.assertContains(response, reverse("profile"))

    def test_profile_view_post(self):
        """Test that the profile view works correctly for post requests"""
        # Test as a guest
        form_data = {"default_phone_number": "123123123"}
        response = self.client.post(reverse("profile"), form_data, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateNotUsed(response, "profiles/profile.html")
        self.user.userprofile.refresh_from_db()
        self.assertIsNone(self.user.userprofile.default_phone_number)
        # Test a valid update
        self.client.login(
            username=self.user.username, password=self.user_password
        )
        valid_phone_number = "123123123"
        form_data = {"default_phone_number": valid_phone_number}
        response = self.client.post(reverse("profile"), form_data, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "profiles/profile.html")
        self.assertContains(response, valid_phone_number)
        self.assertContains(response, "success")
        self.user.userprofile.refresh_from_db()
        self.assertEqual(
            self.user.userprofile.default_phone_number, valid_phone_number
        )
        # Test with an invalid update
        invalid_phone_number = "22222222222222222222222222222222222222222222"
        form_data = {"default_phone_number": invalid_phone_number}
        response = self.client.post(reverse("profile"), form_data, follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "profiles/profile.html")
        self.assertContains(response, invalid_phone_number)
        self.assertContains(response, "fail")
        self.user.userprofile.refresh_from_db()
        self.assertEqual(
            self.user.userprofile.default_phone_number, valid_phone_number
        )
