from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
import json
from unittest.mock import patch

User = get_user_model()

class AIViewsTest(TestCase):
    """
    Tests for the AI views.
    """
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        self.generate_text_url = reverse('ai:generate_text')
        self.generate_image_url = reverse('ai:generate_image')

    def test_generate_text_unauthenticated(self):
        """Test that unauthenticated users cannot access the text generation API."""
        data = {
            'prompt': 'Test prompt',
            'model': 'gpt2'
        }
        response = self.client.post(
            self.generate_text_url,
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 302)  # Redirect to login

    @patch('ai.views.requests.post')
    def test_generate_text_authenticated(self, mock_post):
        """Test that authenticated users can access the text generation API."""
        # Mock the response from the Hugging Face API
        mock_post.return_value.json.return_value = {'generated_text': 'Generated text based on: Test prompt'}

        self.client.login(username='testuser', password='testpassword123')
        data = {
            'prompt': 'Test prompt',
            'model': 'gpt2'
        }
        response = self.client.post(
            self.generate_text_url,
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])
        self.assertIn('generated_text', response_data)

        # Check that the user's API usage count was incremented
        self.user.refresh_from_db()
        self.assertEqual(self.user.api_usage_count, 1)

    def test_generate_text_missing_prompt(self):
        """Test that the text generation API requires a prompt."""
        self.client.login(username='testuser', password='testpassword123')
        data = {
            'model': 'gpt2'
        }
        response = self.client.post(
            self.generate_text_url,
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)
        self.assertFalse(response_data['success'])
        self.assertIn('error', response_data)

    def test_generate_image_unauthenticated(self):
        """Test that unauthenticated users cannot access the image generation API."""
        data = {
            'prompt': 'Test prompt'
        }
        response = self.client.post(
            self.generate_image_url,
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 302)  # Redirect to login

    @patch('ai.views.requests.post')
    def test_generate_image_authenticated(self, mock_post):
        """Test that authenticated users can access the image generation API."""
        # Mock the response from the Hugging Face API
        mock_post.return_value.json.return_value = {'image_url': 'https://example.com/image.png'}

        self.client.login(username='testuser', password='testpassword123')
        data = {
            'prompt': 'Test prompt'
        }
        response = self.client.post(
            self.generate_image_url,
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])
        self.assertIn('image_url', response_data)

        # Check that the user's API usage count was incremented
        self.user.refresh_from_db()
        self.assertEqual(self.user.api_usage_count, 1)

    def test_generate_image_missing_prompt(self):
        """Test that the image generation API requires a prompt."""
        self.client.login(username='testuser', password='testpassword123')
        data = {}
        response = self.client.post(
            self.generate_image_url,
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)
        self.assertFalse(response_data['success'])
        self.assertIn('error', response_data)

class APIUsageLimitTest(TestCase):
    """
    Tests for the API usage limitation.
    """
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        self.generate_text_url = reverse('ai:generate_text')
        self.generate_image_url = reverse('ai:generate_image')
        self.client.login(username='testuser', password='testpassword123')

    def test_api_usage_limit(self):
        """Test that users are limited to 50 API calls."""
        # Set the user's API usage count to the limit
        self.user.api_usage_count = 50
        self.user.save()

        # Try to generate text
        data = {
            'prompt': 'Test prompt',
            'model': 'gpt2'
        }
        response = self.client.post(
            self.generate_text_url,
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 429)  # Too Many Requests
        response_data = json.loads(response.content)
        self.assertFalse(response_data['success'])
        self.assertIn('error', response_data)

        # Try to generate an image
        data = {
            'prompt': 'Test prompt'
        }
        response = self.client.post(
            self.generate_image_url,
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 429)  # Too Many Requests
        response_data = json.loads(response.content)
        self.assertFalse(response_data['success'])
        self.assertIn('error', response_data)
