# chatbotapp/models.py
from django.db import models

class ChatMessage(models.Model):
    user_message = models.TextField()
    bot_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    # chatbot/settings.py
import os
GENERATIVE_AI_KEY = os.getenv('GENERATIVE_AI_KEY')   # Add your key to .env or environment

# chatbotapp/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from .models import ChatMessage
import google.generativeai as genai

@api_view(['POST'])
def chat_message(request):
    user_message = request.data.get('message')

    genai.configure(api_key=settings.GENERATIVE_AI_KEY)
    model = genai.GenerativeModel("gemini-pro")
    bot_response = model.generate_content(user_message)

    # Save to database
    ChatMessage.objects.create(user_message=user_message, bot_response=bot_response.text)

    return Response({"reply": bot_response.text})

# chatbotapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('chat/', views.chat_message, name='chat_message'),
]

# chatbot/urls.py
from django.urls import path, include

urlpatterns = [
    path('api/', include('chatbotapp.urls')),
]
