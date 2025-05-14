from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.conf import settings
import json
import requests
from accounts.models import User

@login_required
@require_POST
def generate_text(request):
    """
    View for generating text using Hugging Face API.
    """
    # Check if the user has reached the API usage limit
    user = request.user
    if user.api_usage_count >= 50:  # Limit to 50 API calls per user
        return JsonResponse({
            'success': False,
            'error': 'You have reached the maximum number of API calls. Please try again later.'
        }, status=429)

    try:
        data = json.loads(request.body)
        prompt = data.get('prompt', '')
        model = data.get('model', 'gpt2')

        if not prompt:
            return JsonResponse({
                'success': False,
                'error': 'Prompt is required.'
            }, status=400)

        # Call Hugging Face API
        # Note: In a real implementation, you would use your Hugging Face API key
        # and make a proper API call. This is a simplified example.
        # response = requests.post(
        #     f"https://api-inference.huggingface.co/models/{model}",
        #     headers={"Authorization": f"Bearer {settings.HUGGING_FACE_API_KEY}"},
        #     json={"inputs": prompt}
        # )

        # For demonstration purposes, we'll return a mock response
        generated_text = f"Generated text based on: {prompt}"

        # Increment the user's API usage count
        user.api_usage_count += 1
        user.save()

        return JsonResponse({
            'success': True,
            'generated_text': generated_text
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@login_required
@require_POST
def generate_image(request):
    """
    View for generating images using Hugging Face API.
    """
    # Check if the user has reached the API usage limit
    user = request.user
    if user.api_usage_count >= 50:  # Limit to 50 API calls per user
        return JsonResponse({
            'success': False,
            'error': 'You have reached the maximum number of API calls. Please try again later.'
        }, status=429)

    try:
        data = json.loads(request.body)
        prompt = data.get('prompt', '')

        if not prompt:
            return JsonResponse({
                'success': False,
                'error': 'Prompt is required.'
            }, status=400)

        # Call Hugging Face API for image generation
        # Note: In a real implementation, you would use your Hugging Face API key
        # and make a proper API call. This is a simplified example.
        # response = requests.post(
        #     "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2",
        #     headers={"Authorization": f"Bearer {settings.HUGGING_FACE_API_KEY}"},
        #     json={"inputs": prompt}
        # )

        # For demonstration purposes, we'll return a mock response
        image_url = f"https://via.placeholder.com/512x512.png?text={prompt.replace(' ', '+')}"

        # Increment the user's API usage count
        user.api_usage_count += 1
        user.save()

        return JsonResponse({
            'success': True,
            'image_url': image_url
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
