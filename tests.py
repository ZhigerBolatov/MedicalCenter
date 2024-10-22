from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .models import HappyLifeUsers, ResetPasswordToken  # Adjust import if necessary
from rest_framework import status

class PasswordResetTests(TestCase):

    def setUp(self):
        self.email = 'testuser@example.com'
        self.user = HappyLifeUsers.objects.create_user(email=self.email, password='password123')
        self.reset_url = '/reset_password/'  # Use the actual URL path
        self.set_password_url = '/set_new_password/'  # Use the actual URL path

    def test_password_reset_valid_email(self):
        """Test that a valid email sends a password reset request."""
        response = self.client.post(self.reset_url, {'email': self.email})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'success')

    def test_password_reset_invalid_email(self):
        """Test that an invalid email returns an error."""
        response = self.client.post(self.reset_url, {'email': 'invalid@example.com'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertContains(response, 'success', 0)

class SetNewPasswordTests(TestCase):

    def setUp(self):
        self.email = 'testuser@example.com'
        self.user = HappyLifeUsers.objects.create_user(email=self.email, password='password123')
        self.token = 'valid_token'  # Simulated token
        ResetPasswordToken.objects.create(user=self.user, token=self.token)
        self.set_password_url = '/set_new_password/'  # Use the actual URL path

    def test_set_new_password_valid(self):
        """Test that a valid token allows the user to set a new password."""
        response = self.client.post(self.set_password_url, {
            'email': self.email,
            'token': self.token,
            'new_password': 'newpassword123'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'Password successfully updated!')
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpassword123'))
