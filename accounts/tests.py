from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .forms import UserRegistrationForm, UserLoginForm

User = get_user_model()

class UserModelTest(TestCase):
    """
    Tests for the custom User model.
    """
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )

    def test_user_creation(self):
        """Test that a user can be created."""
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertTrue(self.user.check_password('testpassword123'))
        self.assertEqual(self.user.api_usage_count, 0)

    def test_user_string_representation(self):
        """Test the string representation of a user."""
        self.assertEqual(str(self.user), 'testuser')

class UserRegistrationTest(TestCase):
    """
    Tests for user registration.
    """
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('accounts:register')

    def test_registration_view_get(self):
        """Test that the registration page loads correctly."""
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')
        self.assertIsInstance(response.context['form'], UserRegistrationForm)

    def test_registration_view_post_valid(self):
        """Test that a user can register with valid data."""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_registration_view_post_invalid(self):
        """Test that registration fails with invalid data."""
        data = {
            'username': 'newuser',
            'email': 'invalid-email',
            'password1': 'newpassword123',
            'password2': 'differentpassword',
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 200)  # Stay on the same page
        self.assertFalse(User.objects.filter(username='newuser').exists())

class UserLoginTest(TestCase):
    """
    Tests for user login.
    """
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('accounts:login')
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )

    def test_login_view_get(self):
        """Test that the login page loads correctly."""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
        self.assertIsInstance(response.context['form'], UserLoginForm)

    def test_login_view_post_valid(self):
        """Test that a user can login with valid credentials."""
        data = {
            'username': 'testuser',
            'password': 'testpassword123',
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful login
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_view_post_invalid(self):
        """Test that login fails with invalid credentials."""
        data = {
            'username': 'testuser',
            'password': 'wrongpassword',
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 200)  # Stay on the same page
        self.assertFalse(response.wsgi_request.user.is_authenticated)

class UserLogoutTest(TestCase):
    """
    Tests for user logout.
    """
    def setUp(self):
        self.client = Client()
        self.logout_url = reverse('accounts:logout')
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        self.client.login(username='testuser', password='testpassword123')

    def test_logout_view(self):
        """Test that a user can logout."""
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)  # Redirect after logout
        self.assertFalse(response.wsgi_request.user.is_authenticated)
