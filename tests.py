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
        self.reset_url = reverse('password_reset')  # Update with your actual URL name

    def test_password_reset_valid_email(self):
        response = self.client.post(self.reset_url, {'email': self.email})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'success')

    def test_password_reset_invalid_email(self):
        response = self.client.post(self.reset_url, {'email': 'invalid@example.com'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertContains(response, 'success', 0)  # Expect no success message

class SetNewPasswordTests(TestCase):

    def setUp(self):
        self.email = 'testuser@example.com'
        self.user = HappyLifeUsers.objects.create_user(email=self.email, password='password123')
        self.token = 'valid_token'  # This would be generated as in your view
        self.reset_password_token = ResetPasswordToken.objects.create(user=self.user, token=self.token)
        self.set_password_url = reverse('set_new_password')  # Update with your actual URL name

    def test_set_new_password_valid(self):
        response = self.client.post(self.set_password_url, {
            'email': self.email,
            'token': self.token,
            'new_password': 'newpassword123'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'Password successfully updated!')
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpassword123'))  # Verify the new password

    def test_set_new_password_invalid_token(self):
        response = self.client.post(self.set_password_url, {
            'email': self.email,
            'token': 'invalid_token',
            'new_password': 'newpassword123'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertContains(response, 'Email and/or Token is not valid!')

    def test_set_new_password_expired_token(self):
        self.reset_password_token.created_at = timezone.now() - timedelta(minutes=11)  # Simulate expiry
        self.reset_password_token.save()
        
        response = self.client.post(self.set_password_url, {
            'email': self.email,
            'token': self.token,
            'new_password': 'newpassword123'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertContains(response, 'Token was expired!')
